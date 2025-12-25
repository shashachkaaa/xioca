# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import logging

from asyncio import sleep
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from pyrogram import Client, types
from .. import loader, utils  # ".." - т.к. модули находятся в папке sh1t-ub/modules, то нам нужно на уровень выше
                              # loader, modules, bot - файлы из папки sh1t-ub


@loader.module(author="shashachkaaa", version=1) #author - автор, version - версия
class ExampleMod(loader.Module):  # Example - название модуля и его класса
                                  # Mod в конце названия обязательно
    """Описание модуля"""

    def __init__(self):
        self.test_attribute = "Это атрибут модуля"

    async def on_load(self, app: Client):  # Можно считать что это асинхронный __init__
        """Вызывается когда модуль загружен"""
        logging.info(f"Модуль {self.name} загружен")

    # Если написать в лс/чате где есть бот "ты дурак?", то он ответит
    @loader.on_bot(lambda self, app, message: message.text and message.text.lower() == "ты дурак?")  # Сработает только если текст сообщения равняется "ты дурак?"
    async def example_message_handler(self, app: Client, message: Message):  # _message_handler на конце функции чтобы обозначить что это хендлер сообщения
        """Пример хендлера сообщения"""
        return await message.reply(
            "Сам такой!")

    async def example_inline_handler(self, app: Client, inline_query: InlineQuery, args: str):  # _inline_handler на конце функции чтобы обозначить что это инлайн-команда
                                                                                                # args - аргументы после команды. необязательный аргумент
        """Пример инлайн-команды. Использование: @bot example [аргументы]"""
        
        await utils.answer_inline(
        	InlineQuery,
        	"Текст сообщения",
        	"Тайтл"
        	reply_markup=kb #кнопки по желанию
        )

    @loader.on_bot(lambda self, app, call: call.data == "example_button_callback")  # Сработает только если каллбек дата равняется "example_button_callback"
    async def example_callback_handler(self, app: Client, call: CallbackQuery):  # _callback_handler на конце функции чтобы обозначить что это каллбек-хендлер
        """Пример каллбека"""
        return await call.answer(
            "Ого пример каллбека", show_alert=True)

    async def example_cmd(self, app: Client, message: types.Message, args: str):  # _cmd на конце функции чтобы обозначить что это команда
                                                                                  # args - аргументы после команды. необязательный аргумент
        """Описание команды. Использование: example [аргументы]"""
        await utils.answer(  # utils.answer - это круто
            message, "Ого пример команды" + (
                f"\nАргументы: {args}" if args
                else ""
            )
        )

        await sleep(2.5)  # никогда не используй time.sleep, потому что это не асинхронная функция, она остановит весь юзербот
        return await utils.answer(
            message, "Прошло 2.5 секунды!")

    @loader.on(lambda _, __, m: "тест" in getattr(m, "text", ""))  # Сработает только если есть "тест" в сообщении с командой
    async def example2_cmd(self, app: Client, message: types.Message):
        """Описание для второй команды с фильтрами"""
        return await utils.answer(
            message, f"Да, {self.test_attribute = }")

    @loader.on(lambda _, __, m: m and m.text == "Привет, это проверка вотчера Xioca")
    async def watcher(self, app: Client, message: types.Message):  # watcher - функция которая работает при получении нового сообщения
        return await message.reply(
            "Привет, все работает отлично")

    # Можно добавлять несколько вотчеров, главное чтобы функция начиналась с "watcher"
    async def watcher_(self, app: Client, message: types.Message):
        if message.text == "Привет, это проверка второго вотчера хиока-юб":
            return await message.reply(
                "И тебе привет!")
