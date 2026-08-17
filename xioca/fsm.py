# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import logging

from types import TracebackType
from typing import List, Optional, Union

from herokutl import TelegramClient
from herokutl.tl.custom.message import Message


class Conversation:
    """Диалог с пользователем. Отправка сообщений и ожидание ответа.

    Обёртка над нативным ``client.conversation()`` из herokutl: он сам
    отслеживает входящие сообщения через апдейты, поэтому опроса истории
    чата, как было на pyrogram, больше нет - ответ приходит сразу, а не с
    задержкой до секунды.

    Интерфейс намеренно сохранён от версии на pyrogram (``ask``,
    ``ask_media``, ``get_response``, ``purge``), чтобы вызывающий код
    не переписывать.
    """

    def __init__(
        self,
        app: TelegramClient,
        chat_id: Union[str, int],
        purge: bool = False,
        timeout: int = 30,
    ) -> None:
        """Инициализация класса

        Параметры:
            app (``herokutl.TelegramClient``):
                Клиент

            chat_id (``str`` | ``int``):
                Чат, в который нужно отправить сообщение

            purge (``bool``, optional):
                Удалять сообщения после завершения диалога

            timeout (``int``, optional):
                Сколько секунд ждать каждый ответ
        """
        self.app = app
        self.chat_id = chat_id
        self.purge = purge
        self.timeout = timeout

        self._conv = None
        self.messages_to_purge: List[Message] = []

    # Историческая опечатка в имени атрибута: часть модулей могла на неё
    # опираться, поэтому оставляем рабочий псевдоним
    @property
    def messagee_to_purge(self) -> List[Message]:
        return self.messages_to_purge

    async def __aenter__(self) -> "Conversation":
        self._conv = self.app.conversation(
            self.chat_id,
            timeout=self.timeout,
            total_timeout=None,
            exclusive=True,
        )
        await self._conv.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ) -> bool:
        try:
            if exc_type is not None:
                logging.exception(
                    "Error inside conversation with %s", self.chat_id,
                    exc_info=(exc_type, exc_value, exc_traceback),
                )
            elif self.purge:
                await self._purge()
        finally:
            self.messages_to_purge.clear()

            if self._conv is not None:
                await self._conv.__aexit__(exc_type, exc_value, exc_traceback)
                self._conv = None

        # Исключения наружу не глотаем
        return False

    async def ask(self, text: str, *args, **kwargs) -> Message:
        """Отправить сообщение

        Параметры:
            text (``str``):
                Текст сообщения
        """
        message = await self._conv.send_message(text, *args, **kwargs)
        self.messages_to_purge.append(message)
        return message

    async def ask_media(
        self,
        file_path: str,
        media_type: str = None,
        *args,
        **kwargs,
    ) -> Message:
        """Отправить файл

        Параметры:
            file_path (``str``):
                Ссылка или путь до файла

            media_type (``str``, optional):
                Тип медиа. В herokutl тип определяется автоматически,
                параметр оставлен для совместимости; ``document``
                отправляет файл без сжатия.
        """
        kwargs.setdefault("force_document", media_type == "document")

        message = await self._conv.send_file(file_path, *args, **kwargs)
        self.messages_to_purge.append(message)
        return message

    async def get_response(self, timeout: int = None) -> Message:
        """Возвращает ответ собеседника

        Параметры:
            timeout (``int``, optional):
                Время ожидания ответа
        """
        message = await self._conv.get_response(
            timeout=timeout if timeout is not None else self.timeout
        )
        self.messages_to_purge.append(message)
        return message

    async def _purge(self) -> bool:
        """Удалить все отправленные и полученные сообщения"""
        if not self.messages_to_purge:
            return True

        try:
            await self.app.delete_messages(
                self.chat_id,
                [message.id for message in self.messages_to_purge],
            )
        except Exception as error:
            logging.warning("Failed to purge conversation messages: %s", error)

        return True
