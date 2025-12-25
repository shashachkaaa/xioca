# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import inspect

from pyrogram import Client
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineQuery
)

from types import FunctionType
from typing import Union
from ..db import db
from .. import types


class Item:
    """Элемент"""

    def __init__(self) -> None:
        """Инициализация класса"""
        self._all_modules: types.ModulesManager = None
        self._db: db = None
        self._app: Client = None

    async def _check_filters(
        self,
        func: FunctionType,
        module: types.Module,
        update_type: Union[Message, InlineQuery, CallbackQuery],
    ) -> bool:
        """Проверка фильтров"""
        if (custom_filters := getattr(func, "_filters", None)):
            coro = custom_filters(module, self._app, update_type)
            if inspect.iscoroutine(coro):
                coro = await coro

            if not coro:
                return False
        else:
            if update_type.from_user.id != self._all_modules.me.id:
                return False

        return True
