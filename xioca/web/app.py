# 📦 Xioca UserBot
# 👤 Copyright (C) 2025+2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import os
import sys
import asyncio
import logging
import re
import time
import base64
import io
import qrcode
import configparser
import uvicorn

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from pyrogram import Client, errors, raw

from .tunnel import Tunnel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

_DELIVERY_HINTS = {
    "APP": "Check the verified Telegram service chat in another logged-in Telegram app.",
    "SMS": "Telegram selected SMS delivery. Check SMS on the phone with this number.",
    "SMS_WORD": "Telegram selected an SMS containing a word. Check your SMS inbox.",
    "SMS_PHRASE": "Telegram selected an SMS containing a phrase. Check your SMS inbox.",
    "CALL": "Telegram selected a phone call. Check incoming calls on this number.",
    "FLASH_CALL": "Telegram selected a short phone call. Check incoming calls.",
    "MISSED_CALL": "Telegram selected a missed call. Check incoming calls.",
    "FRAGMENT_SMS": "Telegram selected Fragment SMS. Check the Fragment account for this number.",
    "EMAIL_CODE": "Telegram selected email delivery. Check your Telegram login email.",
    "FIREBASE_SMS": "Telegram requested device verification for SMS; this web client cannot complete that flow. Try console login or an official Telegram app.",
    "SETUP_EMAIL_REQUIRED": "Telegram requires email setup before login. Complete it in an official Telegram app.",
}


def describe_code_delivery(code_type):
    """Describe Telegram's chosen delivery method without exposing private codes."""
    name = getattr(code_type, "name", None) or getattr(code_type, "__name__", None) or str(code_type)
    kind = str(name).rsplit(".", 1)[-1].upper().removeprefix("SENTCODETYPE")
    return _DELIVERY_HINTS.get(
        kind, "Telegram accepted the request; check other signed-in devices and your phone."
    )


api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

class WebApp:
    def __init__(self, session_name: str, port: int = 8080):
        self.port = port
        self.session_name = session_name
        self.client: Client = None
        self.phone_code_hash = None
        self.phone_number = None
        self.next_code_type = None
        self.resend_available_at = 0.0
        self.qr_status = "idle"
        self.qr_image = None
        self.qr_link = None
        self.qr_expires = 0.0
        self.qr_error = None
        self.qr_task = None

        self.server = None
        self.tunnel_event = asyncio.Event()
        self.tunnel = Tunnel(port, self.tunnel_event)
        
        api.add_route("/", self.index, methods=["GET"])
        api.add_route("/tokens", self.init_client, methods=["POST"])
        api.add_route("/phone_request", self.send_code, methods=["POST"])
        api.add_route("/resend_code", self.resend_code, methods=["POST"])
        api.add_route("/enter_code", self.sign_in, methods=["POST"])
        api.add_route("/qrcode", self.get_qr, methods=["GET"])
        api.add_route("/checkqr", self.check_qr, methods=["GET"])
        api.add_route("/twofa", self.check_password, methods=["POST"])

    async def run(self):
        # The authentication UI must only be accessible through the SSH tunnel,
        # not through an open VPS port.
        config = uvicorn.Config(api, host="127.0.0.1", port=self.port, log_level="warning", access_log=False)
        self.server = uvicorn.Server(config)
        api.state.web_app = self
        server_task = asyncio.create_task(self.server.serve())

        try:
            # Avoid presenting a public URL before the web server is ready.
            for _ in range(100):
                if self.server.started or server_task.done():
                    break
                await asyncio.sleep(0.1)

            if not self.server.started:
                if server_task.done():
                    await server_task
                raise RuntimeError("The web authorization server could not start.")

            url = await self.tunnel.start()
            if not url:
                raise RuntimeError("Failed to establish a localhost.run tunnel.")
            await server_task
        finally:
            self.tunnel.terminate()
            if not server_task.done():
                self.server.should_exit = True
                await server_task

    async def stop(self):
        self.tunnel.terminate()
        
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            
        if self.server:
            self.server.should_exit = True

    async def index(self, request: Request):
        return templates.TemplateResponse(request, "index.html")

    async def init_client(self, request: Request):
        """Validate Telegram API credentials and report connection failures."""
        headers = request.headers
        api_id_raw = (headers.get("id") or "").strip()
        api_hash = (headers.get("hash") or "").strip()

        if not api_id_raw.isdecimal() or int(api_id_raw) <= 0:
            return Response("API ID must be a positive number.", status_code=400)
        if not re.fullmatch(r"[0-9a-fA-F]{32}", api_hash):
            return Response("API Hash must contain exactly 32 hexadecimal characters.", status_code=400)

        # Do not overwrite config.ini until Telegram actually connects.
        # Old sessions may also be present when a user retries web login.
        try:
            if self.client is not None and self.client.is_connected:
                await self.client.disconnect()

            client = Client(
                name=self.session_name,
                api_id=int(api_id_raw),
                api_hash=api_hash,
                in_memory=False,
            )
            self.client = client
            await asyncio.wait_for(client.connect(), timeout=35)
        except Exception as exc:
            logging.exception("Web auth: Telegram client connection failed")
            self.client = None
            return Response(
                f"Telegram connection failed ({type(exc).__name__}). "
                "See the VPS terminal for details.",
                status_code=502,
            )

        try:
            config = configparser.ConfigParser()
            config.read("config.ini")
            if not config.has_section("pyrogram"):
                config.add_section("pyrogram")
            config.set("pyrogram", "api_id", api_id_raw)
            config.set("pyrogram", "api_hash", api_hash)
            with open("config.ini", "w") as config_file:
                config.write(config_file)
        except OSError:
            logging.exception("Web auth: unable to save config.ini")
            return Response(
                "Connected to Telegram, but could not save config.ini. "
                "Check directory permissions.",
                status_code=500,
            )

        return Response("dialog")

    async def _monitor_qr_login(self):
        """Rotate short-lived QR tokens; finish login after Telegram approves one.

        Telegram sends UpdateLoginToken when the code is approved, but this
        unauthenticated client is only connected, not initialized. Periodic
        exportLoginToken also completes the handshake without an update handler.
        """
        try:
            while self.qr_status == "waiting":
                result = await asyncio.wait_for(
                    self.client.invoke(
                        raw.functions.auth.ExportLoginToken(
                            api_id=int(self.client.api_id),
                            api_hash=self.client.api_hash,
                            except_ids=[],
                        )
                    ),
                    timeout=20,
                )

                if isinstance(result, raw.types.auth.LoginTokenMigrateTo):
                    await self.client.disconnect()
                    await self.client.set_dc(result.dc_id)
                    await self.client.connect()
                    result = await asyncio.wait_for(
                        self.client.invoke(
                            raw.functions.auth.ImportLoginToken(token=result.token)
                        ),
                        timeout=20,
                    )

                if isinstance(result, raw.types.auth.LoginTokenSuccess):
                    # The same session file is used by normal Xioca startup.
                    await self.client.get_me()
                    self.qr_status = "success"
                    self.qr_image = None
                    self.qr_link = None
                    # Allow the browser polling loop to see the successful state.
                    await asyncio.sleep(5)
                    await self.finalize_auth()
                    return

                if isinstance(result, raw.types.auth.LoginToken):
                    token = base64.urlsafe_b64encode(result.token).decode("ascii").rstrip("=")
                    login_url = f"tg://login?token={token}"
                    image = qrcode.QRCode(box_size=7, border=2)
                    image.add_data(login_url)
                    image.make(fit=True)
                    stream = io.BytesIO()
                    image.make_image(fill_color="black", back_color="white").save(
                        stream, format="PNG"
                    )
                    # QR tokens are private; deliver only in a no-store response.
                    self.qr_link = login_url
                    self.qr_image = "data:image/png;base64," + base64.b64encode(
                        stream.getvalue()
                    ).decode("ascii")
                    expires = getattr(result, "expires", None)
                    now = time.time()
                    self.qr_expires = float(expires) if expires else now + 30
                    delay = min(20, max(3, self.qr_expires - now - 4))
                    await asyncio.sleep(delay)
                    continue

                raise RuntimeError("Unknown Telegram QR login response.")
        except asyncio.CancelledError:
            raise
        except errors.SessionPasswordNeeded:
            self.qr_status = "password"
            self.qr_image = None
            self.qr_link = None
        except Exception as exc:
            logging.exception("Web QR authorization failed")
            self.qr_status = "error"
            self.qr_image = None
            self.qr_link = None
            self.qr_error = type(exc).__name__

    def _qr_response(self):
        response = JSONResponse({
            "status": self.qr_status,
            "image": self.qr_image if self.qr_status == "waiting" else None,
            "link": self.qr_link if self.qr_status == "waiting" else None,
            "expires_in": max(0, int(self.qr_expires - time.time())),
            "error": self.qr_error if self.qr_status == "error" else None,
        })
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
        return response

    async def get_qr(self, request: Request):
        if self.client is None or not self.client.is_connected:
            return JSONResponse(
                {"status": "error", "error": "Connect using API ID and API Hash first."},
                status_code=409,
            )

        if self.qr_task is None or self.qr_task.done():
            if self.qr_status != "success":
                self.qr_status = "waiting"
                self.qr_image = None
                self.qr_link = None
                self.qr_error = None
                self.qr_task = asyncio.create_task(self._monitor_qr_login())
        return self._qr_response()

    async def check_qr(self, request: Request):
        return self._qr_response()

    def _code_delivery_response(self, sent_code):
        """Preserve Telegram's code hash and report the actual delivery channel.

        Both the first code request and a permitted resend use this method.
        Never put the code hash or other credentials in an HTTP response.
        """
        code_hash = getattr(sent_code, "phone_code_hash", None)
        if not code_hash:
            logging.error("Web auth: Telegram response did not contain a phone code hash")
            return JSONResponse(
                {"status": "error", "message": "Telegram did not provide a confirmation-code reference."},
                status_code=502,
            )

        self.phone_code_hash = code_hash
        self.next_code_type = getattr(sent_code, "next_type", None)

        raw_timeout = getattr(sent_code, "timeout", None)
        try:
            timeout = max(0, min(600, int(raw_timeout))) if raw_timeout is not None else 60
        except (TypeError, ValueError):
            timeout = 60
        self.resend_available_at = time.monotonic() + timeout

        code_type = getattr(sent_code, "type", None)
        delivery = describe_code_delivery(code_type)
        logging.info(
            "Web auth code request accepted by Telegram; delivery=%s; alternative=%s; retry_after=%ss",
            getattr(code_type, "name", type(code_type).__name__),
            self.next_code_type is not None,
            timeout,
        )
        return JSONResponse({
            "status": "enter_code",
            "delivery": delivery,
            "can_resend": self.next_code_type is not None,
            "retry_after": timeout,
        })

    async def send_code(self, request: Request):
        if self.client is None or not self.client.is_connected:
            return JSONResponse(
                {"status": "error", "message": "Telegram is not connected. Return to API configuration."},
                status_code=409,
            )

        try:
            data = await request.json()
        except (ValueError, TypeError):
            return JSONResponse({"status": "error", "message": "Invalid request body."}, status_code=400)

        phone = str(data.get("phone") or "").strip()
        if not re.fullmatch(r"\+?[1-9]\d{6,14}", phone):
            return JSONResponse(
                {"status": "error", "message": "Enter a phone number with country code, for example +12345678901."},
                status_code=400,
            )

        # A failed request must not keep a stale code hash.
        self.phone_number = None
        self.phone_code_hash = None
        self.next_code_type = None
        self.resend_available_at = 0.0

        try:
            sent_code = await self.client.send_code(phone)
        except errors.FloodWait as exc:
            return JSONResponse(
                {"status": "error", "message": f"Telegram rate limit. Try again in {exc.value} seconds."},
                status_code=429,
            )
        except Exception as exc:
            logging.error("Telegram rejected web login code request: %s", type(exc).__name__)
            return JSONResponse(
                {"status": "error", "message": f"Telegram could not request a code ({type(exc).__name__})."},
                status_code=502,
            )

        self.phone_number = phone
        return self._code_delivery_response(sent_code)

    async def resend_code(self, request: Request):
        if not self.client or not self.client.is_connected or not self.phone_code_hash or not self.phone_number:
            return JSONResponse(
                {"status": "error", "message": "Request the first code before trying again."},
                status_code=409,
            )
        if self.next_code_type is None:
            return JSONResponse(
                {"status": "error", "message": "Telegram has not offered an alternative delivery method."},
                status_code=409,
            )
        remaining = max(0, int(self.resend_available_at - time.monotonic() + 0.999))
        if remaining:
            return JSONResponse(
                {"status": "error", "message": f"Telegram requires waiting {remaining} seconds before retrying."},
                status_code=429,
            )

        try:
            sent_code = await self.client.resend_code(self.phone_number, self.phone_code_hash)
        except errors.FloodWait as exc:
            return JSONResponse(
                {"status": "error", "message": f"Telegram rate limit. Try again in {exc.value} seconds."},
                status_code=429,
            )
        except Exception as exc:
            logging.error("Telegram rejected code resend: %s", type(exc).__name__)
            return JSONResponse(
                {"status": "error", "message": f"Telegram could not resend the code ({type(exc).__name__})."},
                status_code=502,
            )
        return self._code_delivery_response(sent_code)

    async def sign_in(self, request: Request):
        data = await request.json()
        code = data.get("code")
        password = data.get("twofa")
        
        try:
            await self.client.sign_in(
                self.phone_number,
                self.phone_code_hash,
                code
            )
            await self.finalize_auth()
            return Response("success")
        except errors.SessionPasswordNeeded:
            if password:
                return await self.check_password(request)
            return Response("no_twofa")
        except errors.PhoneCodeInvalid:
            return Response("invalid_phone_code")
        except Exception as e:
            return Response(f"Error: {e}")

    async def check_password(self, request: Request):
        if request.headers.get("2fa"):
            pwd = request.headers.get("2fa")
        else:
            data = await request.json()
            pwd = data.get("twofa")

        try:
            await self.client.check_password(pwd)
            if self.qr_status == "password":
                self.qr_status = "success"
            await self.finalize_auth()
            return Response("success")
        except errors.PasswordHashInvalid:
            return Response("invalid_twofa")
        except Exception as e:
             return Response(f"Error: {e}")

    async def finalize_auth(self):
        """Завершение авторизации и остановка сервера"""
        user = await self.client.get_me()
        print(f"\n\033[92mSuccessfully logged in as: {user.first_name}\033[0m")
        await self.client.disconnect()
        await self.stop()
