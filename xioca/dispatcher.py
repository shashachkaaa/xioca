# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

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
        base_prefixes = self.db.get("xioca.loader", "prefixes", ["."])
        
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
        	is_double = False
        	for p in base_prefixes:
        		if prefix == p * 2:
        			is_double = True
        			break
        	
        	if is_double:
        		return
        	
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
                message, utils.sys_S("error_command", text=message.text, exc=html.escape(traceback.format_exc())))

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
