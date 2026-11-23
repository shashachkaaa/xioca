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
import base64
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
        
        self.server = None
        self.tunnel_event = asyncio.Event()
        self.tunnel = Tunnel(port, self.tunnel_event)
        
        api.add_route("/", self.index, methods=["GET"])
        api.add_route("/tokens", self.init_client, methods=["POST"])
        api.add_route("/phone_request", self.send_code, methods=["POST"])
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

    async def get_qr(self, request: Request):
        if not self.client or not self.client.is_connected:
             await self.client.connect()
        
        try:
            result = await self.client.invoke(
                raw.functions.auth.ExportLoginToken(
                    api_id=self.client.api_id,
                    api_hash=self.client.api_hash,
                    except_ids=[]
                )
            )
            
            if isinstance(result, raw.types.auth.LoginToken):
                token_base64 = base64.urlsafe_b64encode(result.token).decode('utf-8').rstrip('=')
                url = f"tg://login?token={token_base64}"
                return Response(url)
            
        except Exception as e:
            return Response(f"QR Error: {e}")

    async def check_qr(self, request: Request):
        try:
            result = await self.client.invoke(
                raw.functions.auth.ExportLoginToken(
                    api_id=self.client.api_id,
                    api_hash=self.client.api_hash,
                    except_ids=[]
                )
            )

            if isinstance(result, raw.types.auth.LoginTokenSuccess):
                await self.finalize_auth()
                return Response("success")
            elif isinstance(result, raw.types.auth.LoginToken):
                 return Response("waiting")
                 
        except errors.SessionPasswordNeeded:
            return Response("password")
        except Exception as e:
            return Response(str(e))
        
        return Response("waiting")

    async def send_code(self, request: Request):
        data = await request.json()
        self.phone_number = data.get("phone")
        
        try:
            sent_code = await self.client.send_code(self.phone_number)
            self.phone_code_hash = sent_code.phone_code_hash
            return Response("enter_code")
        except Exception as e:
            return Response(f"Error: {e}")

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
