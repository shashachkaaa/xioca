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

from datetime import datetime
from getpass import getpass

from typing import Union, Tuple, NoReturn

from pyrogram import Client, types, errors
from pyrogram.session.session import Session

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
        self.api_id, self.api_hash, self.device_model = self._load_config()
        
        self.app = Client(
            name=session_name,
            api_id=self.api_id,
            api_hash=self.api_hash,
            app_version=f"Xioca {__version__}",
            device_model=self.device_model,
            system_version="Android 14",
            lang_pack="ru"
        )

    def _load_config(self) -> tuple:
        """Загружает конфигурацию из config.ini или создает новую"""
        config = configparser.ConfigParser()
        
        config.read(self.config_path)
        
        if not config.has_section("pyrogram"):
            config.add_section("pyrogram")
        
        if config.has_option("pyrogram", "api_id"):
            api_id = config["pyrogram"]["api_id"]
        else:
            api_id = colored_input("Введи API ID: ")
            config.set("pyrogram", "api_id", api_id)
        
        if config.has_option("pyrogram", "api_hash"):
            api_hash = config["pyrogram"]["api_hash"]
        else:
            api_hash = colored_input("Введите API hash: ")
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

    def _save_device_model(self, device_model: str) -> None:
        """Сохраняет модель устройства в config.ini"""
        config = configparser.ConfigParser()
        config.read(self.config_path)
        
        if not config.has_section("pyrogram"):
            config.add_section("pyrogram")
        
        config.set("pyrogram", "device_model", device_model)
        
        with open(self.config_path, "w") as config_file:
            config.write(config_file)

    async def send_code(self) -> Tuple[str, str]:
        """Отправить код подтверждения"""
        while True:
            error_text: str = None

            try:
                phone = colored_input("Введите номер телефона: ")
                return phone, (await self.app.send_code(phone)).phone_code_hash
            except errors.PhoneNumberInvalid:
                error_text = "Неверный номер телефона, попробуй ещё раз"
            except errors.PhoneNumberBanned:
                error_text = "Номер телефона заблокирован"
            except errors.PhoneNumberFlood:
                error_text = "На номере телефона флудвейт"
            except errors.PhoneNumberUnoccupied:
                error_text = "Номер не зарегистрирован"
            except errors.BadRequest as error:
                error_text = f"Произошла неизвестная ошибка: {error}"

            if error_text:
                logging.error(error_text)

    async def enter_code(self, phone: str, phone_code_hash: str) -> Union[types.User, bool]:
        """Ввести код подтверждения"""
        try:
            code = colored_input("Введи код подтверждения: ")
            return await self.app.sign_in(phone, phone_code_hash, code)
        except errors.SessionPasswordNeeded:
            return False

    async def enter_2fa(self) -> types.User:
        """Ввести код двухфакторной аутентификации"""
        while True:
            try:
                passwd = colored_input("Введите пароль двухфакторной аутентификации: ", True)
                return await self.app.check_password(passwd)
            except errors.BadRequest:
                logging.error("Неверный пароль, попробуй снова")

    async def authorize(self) -> Union[Tuple[types.User, Client], NoReturn]:
        """Процесс авторизации в аккаунт"""
        await self.app.connect()

        try:
            me = await self.app.get_me()
        except errors.AuthKeyUnregistered:
            phone, phone_code_hash = await self.send_code()
            logged = await self.enter_code(phone, phone_code_hash)
            if not logged:
                me = await self.enter_2fa()
        except errors.SessionRevoked:
            logging.error("Сессия была сброшена, введи rm xioca.session и заново введи команду запуска")
            await self.app.disconnect()
            return sys.exit(64)

        return me, self.app