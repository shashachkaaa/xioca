# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import logging
import asyncio
import sys
from typing import Union, NoReturn

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramAPIError, TelegramUnauthorizedError
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pyrogram import Client

from .events import Events
from .token_manager import TokenManager
from ..db import db
from .. import types, __version__, __get_version_url__, __get_commits_url__


class BotManager(Events, TokenManager):
    """Менеджер бота"""

    def __init__(self, app: Client, db: db, all_modules: types.ModulesManager) -> None:
        self._app = app
        self._db = db
        self._all_modules = all_modules
        self._token = self._db.get("xioca.bot", "token", None)

    async def load(self) -> Union[bool, NoReturn]:
        """Загружает менеджер бота"""
        logging.info("Loading bot manager...")
        error_text = "Userbot requires a bot. Please create a bot and restart the userbot."

        if not self._token:
            self._token = await self._create_bot()
            if self._token is False:
                logging.error(error_text)
                return sys.exit(1)
            self._db.set("xioca.bot", "token", self._token)

        try:
            self.bot = Bot(token=self._token, default=DefaultBotProperties(parse_mode='html'))
        except (TelegramAPIError, TelegramUnauthorizedError):
            logging.error("Invalid token. Attempting to create a new token...")
            result = await self._revoke_token()
            if not result:
                self._token = await self._create_bot()
                if not self._token:
                    logging.error(error_text)
                    return sys.exit(1)
                self._db.set("xioca.bot", "token", self._token)
                return await self.load()

        self._dp = Dispatcher()
        self._dp.message.register(self._message_handler)
        self._dp.inline_query.register(self._inline_handler)
        self._dp.callback_query.register(self._callback_handler)
        asyncio.create_task(self._dp.start_polling(self.bot))
        self.bot.manager = self
        
        bot_info = await self.bot.get_me()
        await self._app.unblock_user(bot_info.username)
        m = await self._app.send_message(bot_info.id, "/start")
        await m.delete()
        
        user_info = await self._app.get_me()
        user_first_name = user_info.first_name
        
        bot_first_name = (bot_info.first_name).replace("Xioca of ", "")
        
        if user_first_name != bot_first_name:
        	await self.bot.set_my_name(f"Xioca of {user_first_name}")
        	logging.warning(f"Inline bot name updated to «Xioca of {user_first_name}» following your profile change.")
        
        logging.info("Bot manager successfully loaded")
        return True