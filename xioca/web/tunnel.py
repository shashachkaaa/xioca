# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import asyncio
import atexit
import json
import logging
import platform
import re


_PUBLIC_HOST_RE = re.compile(
    # Free tunnel hosts may contain multiple labels, e.g. abc123.app.lhr.life.
    r"^(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:lhr\.life|localhost\.run)$",
    re.IGNORECASE,
)


def extract_tunnel_url(line: str):
    """Extract a public HTTPS address from a confirmed localhost.run event.

    Current localhost.run sends CloudEvents with type
    "run.localhost.tunnel.registered" and the public hostname in "subject".
    Older servers may emit a "tcpip-forward" JSON event instead.

    Never extract URLs from the SSH banner (e.g. admin.localhost.run).
    """
    try:
        event = json.loads(line)
    except (TypeError, ValueError):
        return None

    if not isinstance(event, dict):
        return None

    if event.get("type") == "run.localhost.tunnel.registered":
        # CloudEvents 1.0: "subject" is the tunnel's assigned hostname.
        hostname = event.get("subject")
        if not hostname and isinstance(event.get("data"), dict):
            hostname = event["data"].get("address")
    elif event.get("event") == "tcpip-forward":
        # Compatibility with an older localhost.run JSON event format.
        if event.get("status") not in (None, "success"):
            return None
        if event.get("tls_termination") is False:
            return None
        hostname = event.get("address") or event.get("listen_host")
    else:
        return None

    if not isinstance(hostname, str):
        return None

    hostname = hostname.strip().lower()
    if hostname == "admin.localhost.run" or not _PUBLIC_HOST_RE.fullmatch(hostname):
        return None

    return f"https://{hostname}"


class Tunnel:
    def __init__(self, port: int, event: asyncio.Event):
        self.logger = logging.getLogger("Tunnel")
        self.port = port
        self.event = event
        self.process = None
        self.url = None
        self._reader_tasks = []
        self._diagnostics = []

    def terminate(self):
        if self.process and self.process.returncode is None:
            try:
                self.process.terminate()
            except ProcessLookupError:
                pass
            except Exception as exc:
                self.logger.error("Failed to stop SSH tunnel: %s", exc)

    async def _read_stream(self, stream):
        while True:
            raw_line = await stream.readline()
            if not raw_line:
                break

            line = raw_line.decode("utf-8", errors="replace").strip()
            if not line:
                continue

            url = extract_tunnel_url(line)
            if url and not self.url:
                self.url = url
                self.event.set()
                continue

            # Keep only a bounded tail to explain connection failures. Do not
            # print the SSH welcome banner or its unrelated administrator URL.
            self._diagnostics.append(line[:300])
            if len(self._diagnostics) > 16:
                self._diagnostics.pop(0)
            self.logger.debug("localhost.run: %s", line)

    async def _cleanup_failed_tunnel(self):
        self.terminate()
        if self.process and self.process.returncode is None:
            try:
                await asyncio.wait_for(self.process.wait(), timeout=3)
            except asyncio.TimeoutError:
                self.process.kill()
                await self.process.wait()

        for task in self._reader_tasks:
            if not task.done():
                task.cancel()
        if self._reader_tasks:
            await asyncio.gather(*self._reader_tasks, return_exceptions=True)

    async def start(self):
        if "windows" in platform.system().lower():
            self.logger.warning("SSH tunneling may require OpenSSH or WSL on Windows.")

        self.url = None
        self.event.clear()
        self._diagnostics.clear()
        print("[WEB AUTH] Connecting to localhost.run (up to 25 seconds)...", flush=True)

        try:
            self.process = await asyncio.create_subprocess_exec(
                "ssh",
                "-n",
                "-T",
                "-o", "BatchMode=yes",
                "-o", "ConnectTimeout=10",
                "-o", "ConnectionAttempts=1",
                "-o", "ExitOnForwardFailure=yes",
                "-o", "ServerAliveInterval=30",
                "-o", "ServerAliveCountMax=3",
                "-o", "StrictHostKeyChecking=accept-new",
                "-R", f"80:127.0.0.1:{self.port}",
                "nokey@localhost.run",
                "--", "--output", "json",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except (FileNotFoundError, OSError) as exc:
            self.logger.error("Could not launch SSH (is openssh-client installed?): %s", exc)
            return None

        self._reader_tasks = [
            asyncio.create_task(self._read_stream(self.process.stdout)),
            asyncio.create_task(self._read_stream(self.process.stderr)),
        ]
        url_ready = asyncio.create_task(self.event.wait())
        process_exit = asyncio.create_task(self.process.wait())

        try:
            done, _ = await asyncio.wait(
                {url_ready, process_exit},
                timeout=25,
                return_when=asyncio.FIRST_COMPLETED,
            )

            if url_ready in done and self.url and self.process.returncode is None:
                atexit.register(self.terminate)
                print(
                    "\n\033[92m[WEB AUTH]\033[0m "
                    f"Visit the web panel via the link for authorization: {self.url}\n",
                    flush=True,
                )
                return self.url

            if process_exit in done:
                self.logger.error(
                    "localhost.run SSH closed before providing a tunnel URL (exit code %s).",
                    self.process.returncode,
                )
            else:
                self.logger.error("No valid localhost.run tunnel URL received within 25 seconds.")

            if self._diagnostics:
                self.logger.error("Recent SSH output (for diagnostics):")
                for entry in self._diagnostics[-6:]:
                    self.logger.error("  %s", entry)
            else:
                self.logger.error(
                    "SSH gave no output. Check DNS, TCP port 22, and the SSH host key."
                )
            return None
        finally:
            for task in (url_ready, process_exit):
                if not task.done():
                    task.cancel()

            if not self.url or self.process.returncode is not None:
                await self._cleanup_failed_tunnel()
