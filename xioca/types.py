# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

from pyrogram import Client, types

from types import FunctionType
from typing import Union, List, Dict, Any

from .db import db


class Module:
    """Описание модуля"""
    name: str
    author: str
    version: Union[int, float]

    async def on_load(self, app: Client) -> Any:
        """Вызывается при загрузке модуля"""


class ModulesManager:
    """Менеджер модулей"""

    modules: List[Module]
    watcher_handlers: List[FunctionType]

    command_handlers: Dict[str, FunctionType]
    message_handlers: Dict[str, FunctionType]
    inline_handlers: Dict[str, FunctionType]
    callback_handlers: Dict[str, FunctionType]

    _local_modules_path: str

    me: types.User
    _db: db

    aliases: Dict[str, str]

    dp: Any
    bot_manager: Any
