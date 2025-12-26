# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import asyncio
import logging
import os
import re
import atexit
import platform

class Tunnel:
    def __init__(self, port: int, event: asyncio.Event):
        self.logger = logging.getLogger("Tunnel")
        self.port = port
        self.event = event
        self.process = None

    def terminate(self):
        if self.process:
            try:
                self.process.terminate()
            except Exception as e:
                self.logger.error(f"Error terminating tunnel: {e}")

    async def start(self):
        system = platform.system().lower()
        if "windows" in system:
            self.logger.warning("SSH Tunneling is unstable on Windows without WSL. Trying anyway...")

        command = (
            f"ssh -o StrictHostKeyChecking=no -R 80:localhost:{self.port} nokey@localhost.run"
        )
        
        self.process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE
        )

        url = None
        
        async def read_stream():
            nonlocal url
            while True:
                line = await self.process.stdout.readline()
                if not line:
                    break
                
                line_str = line.decode().strip()
                if "tunneled with tls" in line_str.lower() or "https://" in line_str:
                     match = re.search(r"(https://[a-zA-Z0-9-]+\.lhr\.life|https://[a-zA-Z0-9-]+\.localhost\.run)", line_str)
                     if match:
                         url = match.group(1)
                         self.event.set()
                         
        asyncio.create_task(read_stream())

        try:
            await asyncio.wait_for(self.event.wait(), timeout=30)
        except asyncio.TimeoutError:
            self.logger.error("Tunnel creation timed out.")
            self.terminate()
            return None

        if url:
            atexit.register(self.terminate)
            print(f"\n\033[92m[WEB AUTH]\033[0m Visit the web panel via the link for authorization: {url}\n")
            return url
        return None