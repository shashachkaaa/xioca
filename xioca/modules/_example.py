# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

# Имя файла начинается с подчёркивания, поэтому загрузчик его пропускает:
# это образец формата, а не рабочий модуль.
#
# Xioca 3.x исполняет модули на рантайме Heroku, поэтому формат совпадает с
# Hikka и Heroku - модуль, написанный для них, работает здесь без правок,
# и наоборот.

import logging

# Тип сообщения приходит из herokutl (форк Telethon), а не из pyrogram
from herokutl.tl.custom import Message

# `..` внутри модуля указывает на рантайм: загрузчик регистрирует модуль под
# именем xioca.runtime.modules.<имя>, независимо от того, где лежит файл.
# Чтобы обратиться к самой Xioca, нужен абсолютный импорт: from xioca import ...
from .. import loader, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)


@loader.tds  # обязателен: связывает класс с системой переводов
class ExampleMod(loader.Module):
    """Описание модуля - попадёт в .help"""

    # Ключ "name" обязателен, остальные - произвольные.
    strings = {
        "name": "Example",
        "hello": "👋 <b>Hello, {}!</b>",
        "no_args": "❌ <b>Specify some text</b>",
        "btn": "🔄 Press me",
        "pressed": "✅ Pressed",
    }

    # Перевод: strings_<код языка>. Отсутствующие ключи берутся из strings.
    strings_ru = {
        "hello": "👋 <b>Привет, {}!</b>",
        "no_args": "❌ <b>Укажите текст</b>",
        "btn": "🔄 Нажми меня",
        "pressed": "✅ Нажато",
    }

    def __init__(self):
        # Конфиг доступен пользователю через .config
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "greeting",
                "world",
                lambda: "Кого приветствовать по умолчанию",
                validator=loader.validators.String(max_len=64),
            ),
        )

    async def client_ready(self):
        """Вызывается один раз, когда клиент готов - аналог async __init__"""
        logger.info("Модуль %s загружен", self.strings("name"))

    @loader.command()
    async def examplecmd(self, message: Message):
        """[текст] - пример команды"""
        # Аргументы не приходят отдельным параметром, как было в Xioca 2.x
        args = utils.get_args_raw(message) or self.config["greeting"]

        # utils.answer сам решает, отредактировать сообщение или ответить
        await utils.answer(
            message,
            self.strings("hello").format(utils.escape_html(args)),
        )

    @loader.command()
    async def exampleformcmd(self, message: Message):
        """Пример инлайн-формы с кнопкой"""
        await self.inline.form(
            message=message,
            text=self.strings("hello").format("inline"),
            reply_markup=[{"text": self.strings("btn"), "callback": self._pressed}],
        )

    async def _pressed(self, call: InlineCall):
        """Обработчик нажатия: коллбек передаётся прямо в кнопку"""
        await call.answer(self.strings("pressed"))

    @loader.watcher()
    async def watcher(self, message: Message):
        """Вызывается на каждом сообщении - держите его дешёвым"""
