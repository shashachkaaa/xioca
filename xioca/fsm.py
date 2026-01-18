# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import logging
import asyncio

from types import TracebackType
from typing import Union, List

from pyrogram import Client, types


class Conversation:
    """Диалог с пользователем. Отправка сообщений и ожидание ответа"""

    def __init__(
        self,
        app: Client,
        chat_id: Union[str, int],
        purge: bool = False
    ) -> None:
        """Инициализация класса

        Параметры:
            app (``pyrogram.Client``):
                Клиент

            chat_id (``str`` | ``int``):
                Чат, в который нужно отправить сообщение

            purge (``bool``, optional):
                Удалять сообщения после завершения диалога
        """
        self.app = app
        self.chat_id = chat_id
        self.purge = purge

        self.messagee_to_purge: List[types.Message] = []

    async def __aenter__(self) -> "Conversation":
        return self

    async def __aexit__(
        self,
        exc_type: type,
        exc_value: Exception,
        exc_traceback: TracebackType
    ) -> bool:
        if all(
            [exc_type, exc_value, exc_traceback]
        ):
            logging.exception(exc_value)
        else:
            if self.purge:
                await self._purge()

        return self.messagee_to_purge.clear()

    async def ask(self, text: str, *args, **kwargs) -> types.Message:
        """Отправить сообщение

        Параметры:
            text (``str``):
                Текст сообщения

            args (``list``, optional):
                Аргументы отправки сообщения

            kwargs (``dict``, optional):
                Параметры отправки сообщения
        """
        message = await self.app.send_message(
            self.chat_id, text, *args, **kwargs)

        self.messagee_to_purge.append(message)
        return message

    async def ask_media(
        self,
        file_path: str,
        media_type: str,
        *args,
        **kwargs
    ) -> types.Message:
        """Отправить файл

        Параметры:
            file_path (``str``):
                Ссылка или путь до файла

            media_type (``str``):
                Тип отправляемого медиа

            args (``list``, optional):
                Аргументы отправки сообщения

            kwargs (``dict``, optional):
                Параметры отправки сообщения
        """
        available_media = [
            "animation", "audio",
            "document", "photo",
            "sticker", "video",
            "video_note", "voice"
        ]
        if media_type not in available_media:
            raise TypeError("This media type is not supported")

        message = await getattr(self.app, "send_" + media_type)(
            self.chat_id, file_path, *args, **kwargs)

        self.messagee_to_purge.append(message)
        return message

    async def get_response(self, timeout: int = 30) -> types.Message:
        """Возвращает ответ

            Параметр:
                timeout (``int``, optional):
                Время ожидания ответа
        """
        while timeout > 0:
            async for message in self.app.get_chat_history(self.chat_id, limit=1):
                if not message.from_user.is_self:
                    self.messagee_to_purge.append(message)
                    return message

            timeout -= 1
            await asyncio.sleep(1)

        raise RuntimeError("Response timeout expired")

    async def _purge(self) -> bool:
        """Удалить все отправленные и полученные сообщения"""
        for message in self.messagee_to_purge:
            await message.delete()

        return True
