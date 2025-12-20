#    Sh1t-UB (telegram userbot by sh1tn3t)
#    Copyright (C) 2021-2022 Sh1tN3t

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import html
import logging
import traceback

from inspect import getfullargspec, iscoroutine
from types import FunctionType

from pyrogram import Client, types, filters
from pyrogram.handlers import MessageHandler

from .db import db
from . import loader, utils

async def check_filters(func: FunctionType, app: Client, message: types.Message) -> bool:
       """Проверка фильтров"""
       if (custom_filters := getattr(func, "_filters", None)):
           coro = custom_filters(app, message)
           if iscoroutine(coro):
               coro = await coro

           if not coro:
               return False
       return True


class DispatcherManager:
    """Менеджер диспетчера"""

    def __init__(self, app: Client, modules: "loader.ModulesManager") -> None:
        self.app = app
        self.modules = modules
        self.db = db

    async def load(self) -> bool:
        """Загружает менеджер диспетчера"""
        logging.info("Загрузка диспетчера...")

        self.app.add_handler(
            MessageHandler(
                self._handle_message, filters.all)
        )

        logging.info("Диспетчер успешно загружен")
        return True

    async def _handle_message(self, app: Client, message: types.Message) -> types.Message:
        """Обработчик сообщений"""
        
        await self._handle_watchers(app, message)
        await self._handle_other_handlers(app, message)
        
        ids = self.db.get("xioca.loader", "allow", [])
        
        prefix, command, args = utils.get_full_command(message)
        
        if not message.outgoing:
        	try:
        		if message.from_user.id not in ids:
        			return message
        		
        		if command.endswith("@me"):
        			return
        		
        	except:
        		return message
        else:
        	if command.endswith("@me"):
        		command = command.replace("@me", "")

        if not (command or args):
            return

        command = self.modules.aliases.get(command, command)
        func = self.modules.command_handlers.get(command.lower())
        if not func:
            return

        if not await check_filters(func, app, message):
            return

        try:
            if (
                len(vars_ := getfullargspec(func).args) > 3
                and vars_[3] == "args"
            ):
                await func(app, message, utils.get_full_command(message)[2])
            else:
                await func(app, message)
        except Exception as error:
            logging.exception(error)
            await utils.answer(
                message, f"<emoji id=5210952531676504517>❌</emoji> <b>Произошла ошибка при выполнении команды: </b> <code>{message.text}</code>\n<emoji id=5440660757194744323>‼️</emoji> <b>Ошибка:</b>\n<code>{html.escape(traceback.format_exc())}</code>")

        return message

    async def _handle_watchers(self, app: Client, message: types.Message) -> types.Message:
        """Обработчик вотчеров"""
        for watcher in self.modules.watcher_handlers:
            try:
                if not await check_filters(watcher, app, message):
                    continue

                await watcher(app, message)
            except Exception as error:
                logging.exception(error)

        return message

    async def _handle_other_handlers(self, app: Client, message: types.Message) -> types.Message:
        """Обработчик других хендлеров"""
        for handler in app.dispatcher.groups[0]:
            if getattr(handler.callback, "__func__", None) == DispatcherManager._handle_message:
                continue

            coro = handler.filters(app, message)
            if iscoroutine(coro):
                coro = await coro

            if not coro:
                continue

            try:
                handler = handler.callback(app, message)
                if iscoroutine(handler):
                    await handler
            except Exception as error:
                logging.exception(error)

        return message
