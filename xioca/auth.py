# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import logging
import random
import os
import sys
import configparser
import asyncio
import base64
import qrcode

from datetime import datetime
from getpass import getpass
from typing import Union, Tuple, NoReturn

from pyrogram import Client, types, errors, raw
from pyrogram.session.session import Session

try:
    from .web.app import WebApp
except ImportError:
    WebApp = None

from . import __version__

devices = [
    "Samsung Galaxy S24 Ultra",
    "Google Pixel 8 Pro",
    "OnePlus 12R",
    "Samsung Galaxy Z Fold 6",
    "Sony Xperia 1 VI",
    "OPPO Find X7 Ultra",
    "Xiaomi 14 Ultra",
    "Xiaomi Redmi Note 14 SE 5G",
    "Realme 15T",
    "Samsung Galaxy A17 5G"
]

Session.notice_displayed = True

def colored_input(prompt: str = "", hide: bool = False) -> str:
    """Цветной инпут"""
    frame = sys._getframe(1)
    return (input if not hide else getpass)(
        "\x1b[32m{time:%Y-%m-%d %H:%M:%S}\x1b[0m | "
        "\x1b[1m{level: <8}\x1b[0m | "
        "\x1b[36m{name}\x1b[0m:\x1b[36m{function}\x1b[0m:\x1b[36m{line}\x1b[0m - \x1b[1m{prompt}\x1b[0m".format(
            time=datetime.now(), level="INPUT", name=frame.f_globals["__name__"],
            function=frame.f_code.co_name, line=frame.f_lineno, prompt=prompt
        )
    )


class Auth:
    """Авторизация в аккаунт"""

    def __init__(self, session_name: str = "../xioca") -> None:
        self.session_name = session_name
        self.config_path = "./config.ini"
        self.api_id = None
        self.api_hash = None
        self.device_model = None

    def _load_config(self) -> tuple:
        """Загружает конфигурацию из config.ini или создает новую"""
        config = configparser.ConfigParser()
        config.read(self.config_path)
        
        if not config.has_section("pyrogram"):
            config.add_section("pyrogram")
        
        if config.has_option("pyrogram", "api_id"):
            api_id = config["pyrogram"]["api_id"]
        else:
            api_id = colored_input("Enter API ID: ")
            config.set("pyrogram", "api_id", api_id)
        
        if config.has_option("pyrogram", "api_hash"):
            api_hash = config["pyrogram"]["api_hash"]
        else:
            api_hash = colored_input("Enter API hash: ")
            config.set("pyrogram", "api_hash", api_hash)
        
        if config.has_option("pyrogram", "device_model"):
            device_model = config["pyrogram"]["device_model"]
            if device_model not in devices:
                device_model = random.choice(devices)
                config.set("pyrogram", "device_model", device_model)
        else:
            device_model = random.choice(devices)
            config.set("pyrogram", "device_model", device_model)
        
        with open(self.config_path, "w") as config_file:
            config.write(config_file)
        
        return api_id, api_hash, device_model

    async def send_code(self) -> Tuple[str, str]:
        """Отправить код подтверждения"""
        while True:
            error_text: str = None
            try:
                phone = colored_input("Enter phone number: ")
                return phone, (await self.app.send_code(phone)).phone_code_hash
            except errors.PhoneNumberInvalid:
                error_text = "Invalid phone number, please try again."
            except errors.PhoneNumberBanned:
                error_text = "Phone number is banned."
            except errors.PhoneNumberFlood:
                error_text = "The phone number is under a flood wait."
            except errors.PhoneNumberUnoccupied:
                error_text = "Number is not registered."
            except errors.BadRequest as error:
                error_text = f"An unknown error occurred: {error}"

            if error_text:
                logging.error(error_text)

    async def enter_code(self, phone: str, phone_code_hash: str) -> Union[types.User, bool]:
        """Ввести код подтверждения"""
        try:
            code = colored_input("Enter verification code: ")
            return await self.app.sign_in(phone, phone_code_hash, code)
        except errors.SessionPasswordNeeded:
            return False

    async def enter_2fa(self) -> types.User:
        """Ввести код двухфакторной аутентификации"""
        while True:
            try:
                passwd = colored_input("Enter 2FA password: ", True)
                return await self.app.check_password(passwd)
            except errors.BadRequest:
                logging.error("Wrong password. Try again.")

    async def authorize_via_qr(self) -> types.User:
        """Авторизация через QR код в консоли"""
        last_token = None
        print("Authorization token request...")

        while True:
            try:
                result = await self.app.invoke(
                    raw.functions.auth.ExportLoginToken(
                        api_id=int(self.api_id),
                        api_hash=self.api_hash,
                        except_ids=[]
                    )
                )
            except Exception as e:
                logging.error(f"Token acquisition error: {e}")
                await asyncio.sleep(5)
                continue

            if isinstance(result, raw.types.auth.LoginToken):
                if result.token != last_token:
                    last_token = result.token
                    token_base64 = base64.urlsafe_b64encode(result.token).decode('utf-8').rstrip('=')
                    url = f"tg://login?token={token_base64}"
                    
                    os.system('cls' if os.name == 'nt' else 'clear')
                    qr = qrcode.QRCode(border=2)
                    qr.add_data(url)
                    qr.make(fit=True)
                    
                    print("\n\x1b[1;37mPlease scan the QR code within Telegram:\x1b[0m")
                    print("\x1b[32m​(Settings -> Devices -> Link Desktop Device)\x1b[0m\n")
                    qr.print_ascii(invert=True)
                
                await asyncio.sleep(5)
                
            elif isinstance(result, raw.types.auth.LoginTokenSuccess):
                print("\nQR code has been successfully scanned.")
                return await self.app.get_me()
            
            elif isinstance(result, raw.types.auth.LoginTokenMigrateTo):
                await self.app.disconnect()
                await self.app.set_dc(result.dc_id)
                await self.app.connect()
                last_token = None
                continue

    async def _start_web_auth(self):
        """Логика запуска веб-туннеля"""
        if not WebApp:
            logging.error("The WebApp module was not found. Please verify the xioca/web/ directory.")
            return None
            
        print("\n\x1b[33m[WEB] Starting authorization web UI...\x1b[0m")
        web_handler = WebApp(session_name=self.session_name, port=8080)
        
        try:
            await web_handler.run()
        except SystemExit:
            pass
            
        self.api_id, self.api_hash, self.device_model = self._load_config()
        self.app = Client(
            name=self.session_name,
            api_id=self.api_id,
            api_hash=self.api_hash
        )
        await self.app.connect()
        return await self.app.get_me()

    async def authorize(self) -> Union[Tuple[types.User, Client], NoReturn]:
        """Процесс авторизации с выбором метода"""

        if os.path.exists(f"xioca.session"):
            self.api_id, self.api_hash, self.device_model = self._load_config()
            self.app = Client(self.session_name, self.api_id, self.api_hash)
            await self.app.connect()
            try:
                me = await self.app.get_me()
                return me, self.app
            except Exception:
                await self.app.disconnect()
                logging.warning("Invalid session. Please log in again.")
                
        print("\n\x1b[1mAUTHORIZATION METHOD:\x1b[0m")
        print("1. Console (Phone / QR)")
        print("2. Web panel (lhr.life Tunnel)")
        
        choice = colored_input("Choose an option (1/2): ").strip()

        if choice == "2":
            me = await self._start_web_auth()
            if me:
                return me, self.app

        self.api_id, self.api_hash, self.device_model = self._load_config()
        self.app = Client(
            name=self.session_name,
            api_id=self.api_id,
            api_hash=self.api_hash,
            app_version=f"Xioca {__version__}",
            device_model=self.device_model
        )
        
        await self.app.connect()

        try:
            me = await self.app.get_me()
        except errors.AuthKeyUnregistered:
            use_qr = colored_input("Do you want to authorize by QR code? (y/n): ").strip().lower()
            
            if use_qr == 'y':
                me = await self.authorize_via_qr()
            else:
                phone, phone_code_hash = await self.send_code()
                logged = await self.enter_code(phone, phone_code_hash)
                if not logged:
                    me = await self.enter_2fa()
                else:
                    me = logged
        except errors.SessionRevoked:
            logging.error("The session was revoked.")
            await self.app.disconnect()
            sys.exit(64)

        return me, self.app