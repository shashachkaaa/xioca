# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import random
import asyncio
import logging
import re

from loguru import logger
from typing import Union

from pyrogram import errors

from .types import Item
from .. import utils, fsm


class TokenManager(Item):
    """Менеджер токенов"""

    async def _create_bot(self, name: str = None) -> Union[str, None]:
        """Создать и настроить бота"""
        logging.info("Начался процесс создания нового бота...")

        async with fsm.Conversation(self._app, "@BotFather", True) as conv:
            try:
                await conv.ask("/cancel")
            except errors.UserIsBlocked:
                await self._app.unblock_user("@BotFather")

            await conv.get_response()
            await asyncio.sleep(5)

            await conv.ask("/newbot")
            response = await conv.get_response()

            if not all(
                phrase not in response.text
                for phrase in ["That I cannot do.", "Sorry"]
            ):
                logging.error("Произошла ошибка при создании бота. Ответ @BotFather:")
                logging.error(response.text)
                return False
            await asyncio.sleep(5)

            await conv.ask(f"Xioca of {utils.get_display_name(self._all_modules.me)[:45]}")
            await conv.get_response()

            bot_username = f"xioca_{utils.random_id(6)}_bot" if name is None else f"{name}"
            await asyncio.sleep(5)
            
            await conv.ask(bot_username)
            response = await conv.get_response()

            search = re.search(r"(?<=<code>)(.*?)(?=</code>)", response.text.html)
            if not search:
                logging.error("Произошла ошибка при создании бота. Ответ @BotFather:")
                return logging.error(response.text)
            await asyncio.sleep(5)

            token = search.group(0)

            await conv.ask("/setuserpic")
            await conv.get_response()
            await asyncio.sleep(5)
            
            await conv.ask("@" + bot_username)
            await conv.get_response()
            await asyncio.sleep(5)

            await conv.ask_media(random.choice(["bot_avatar1.png", "bot_avatar2.png", "bot_avatar3.png"]), media_type="photo")
            await conv.get_response()
            await asyncio.sleep(5)

            await conv.ask("/setinline")
            await conv.get_response()
            await asyncio.sleep(5)

            await conv.ask("@" + bot_username)
            await conv.get_response()
            await asyncio.sleep(5)

            await conv.ask("Xioca command")
            await conv.get_response()

            logger.success("Бот успешно создан")
            return token

    async def _revoke_token(self) -> str:
        """Сбросить токен бота"""
        async with fsm.Conversation(self._app, "@BotFather", True) as conv:
            try:
                await conv.ask("/cancel")
            except errors.UserIsBlocked:
                await self._app.unblock_user("@BotFather")

            await conv.get_response()

            await conv.ask("/revoke")
            response = await conv.get_response()

            if "/newbot" in response.text:
                return logging.error("Нет созданных ботов")

            for row in response.reply_markup.keyboard:
                for button in row:
                    search = re.search(r"@xioca_[0-9a-zA-Z]{6}_bot", button)
                    if search:
                        await conv.ask(button)
                        break
                else:
                    return logging.error("Нет созданного xioca бота")

            response = await conv.get_response()
            search = re.search(r"\d{1,}:[0-9a-zA-Z_-]{35}", response.text)

            logger.success("Бот успешно сброшен")
            return search.group(0)
