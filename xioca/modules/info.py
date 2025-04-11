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

import configparser

import time
import psutil
import platform
from datetime import datetime

from aiogram.types import (
    InlineQuery,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from pyrogram import Client, types
from .. import loader, utils, __version__, __start_time__


INFO_MARKUP = InlineKeyboardBuilder()
bback = InlineKeyboardButton(text="◀️ Назад", callback_data="info")
INFO_MARKUP.row(bback)

INFO_SERVER_MARKUP = InlineKeyboardBuilder()
binfo = InlineKeyboardButton(text="ℹ️ Информация о сервере", callback_data="info_server")
INFO_SERVER_MARKUP.row(binfo)


def humanize(num: float, suffix: str = "B") -> str:
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1000.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1000.0

    return "%.1f%s%s" % (num, "Y", suffix)


def get_info_message(me: types.User):
    mention = f"<a href=\"tg://user?id={me.id}\">{utils.get_display_name(me)}</a>"
    uptime = datetime.now() - __start_time__
    uptime_str = str(uptime).split('.')[0]
    return f"""🌙 <b>Xioca</b>

👤 <b>Владелец</b>: {mention}
⚡️ <b>Прошло времени с момента запуска:</b> <code>{uptime_str}</code>
🔢 <b>Версия</b>: v{__version__}"""


def get_cpu_info():
    """Возвращает информацию о процессоре"""
    return (
        f"    - Использование: <b>{int(psutil.cpu_percent())}</b>%\n"
        f"    - Ядра: <b>{psutil.cpu_count()}</b>"
    )


def get_ram_info():
    """Возвращает информацию о памяти"""
    ram = psutil.virtual_memory()
    return (
        f"    - Занято: <b>{humanize(ram.used)}</b> (<b>{int(ram.percent)}</b>%)\n"
        f"    - Всего: <b>{humanize(ram.total)}</b>"
    )


def get_disk_info():
    """Возвращает информацию о дисках"""
    disk = psutil.disk_usage("/")
    return (
        f"    - Занято: <b>{humanize(disk.used)}</b> (<b>{int(disk.percent)}</b>%)\n"
        f"    - Всего: <b>{humanize(disk.total)}</b>"
    )


def get_other_info():
    """Возвращает прочую информацию"""
    if not platform.system() == "Linux":
        return "❗ Не Linux"

    with open("/etc/os-release", "r") as file:
        content = "[linux]\n" + file.read()

    config = configparser.ConfigParser()
    config.read_string(content)
    distro = config["linux"]["PRETTY_NAME"].strip('"')

    os = platform.system()
    kernel = platform.release()
    arch = " ".join(platform.architecture())

    return (
        f"    - ОС: <b>{os}</b>\n"
        f"    - Дистрибутив: <b>{distro}</b>\n"
        f"    - Ядро: <b>{kernel}</b>\n"
        f"    - Архитектура: <b>{arch}</b>"
    )


@loader.module("Information", "sh1tn3t | shashachkaaa")
class InformationMod(loader.Module):
    """Информация о юзерботе"""

    async def info_cmd(self, app: Client, message: types.Message):
        """Вызывает инлайн-команду info. Использование: info"""
        bot_results = await app.get_inline_bot_results(
            (await self.bot.me()).username, "info")

        await app.send_inline_bot_result(
            message.chat.id, bot_results.query_id,
            bot_results.results[0].id
        )
        return await message.delete()

    @loader.on_bot(lambda self, app, inline_query: True)
    async def info_inline_handler(self, app: Client, inline_query: InlineQuery):
        """Информация о юзерботе. Использование: @bot info"""
        message = InputTextMessageContent(message_text=get_info_message(self.all_modules.me))

        return await inline_query.answer(
            [
                InlineQueryResultArticle(
                    id=utils.random_id(),
                    title="Информация",
                    input_message_content=message,
                    reply_markup=(
                        INFO_SERVER_MARKUP.as_markup()),
                    thumb_url="https://api.fl1yd.su/emoji/2139-fe0f.png",
                )
            ], cache_time=0
        )

    @loader.on_bot(lambda self, app, call: call.data == "info")
    async def info_callback_handler(self, app: Client, call: CallbackQuery):
        """Информация о юзерботе"""
        
        ids = self.db.get("xioca.loader", "allow", [])
        if call.from_user.id != self.all_modules.me.id:
            if call.from_user.id not in ids:
                return await call.answer("❗ А эта кнопочка не для тебя!", True)

        await call.answer()

        return await self.bot.edit_message_text(
            inline_message_id=call.inline_message_id,
            text=get_info_message(self.all_modules.me),
            reply_markup=INFO_SERVER_MARKUP.as_markup()
        )

    @loader.on_bot(lambda self, app, call: call.data == "info_server")
    async def info_server_callback_handler(self, app: Client, call: CallbackQuery):
        """Информация о сервере"""
        
        ids = self.db.get("xioca.loader", "allow", [])
        if call.from_user.id != self.all_modules.me.id:
            if call.from_user.id not in ids:
                return await call.answer("❗ А эта кнопочка не для тебя!", True)

        await call.answer()

        message = (
            f"<b>ℹ️ Информация о системе</b>:\n"
            f"---------------\n\n"
            f"🧠 <b>Процессор</b>:\n"
            f"{get_cpu_info()}\n\n"
            f"🗄️ <b>ОЗУ</b>:\n"
            f"{get_ram_info()}\n\n"
            f"💿 <b>Физ. память</b>:\n"
            f"{get_disk_info()}\n\n"
            f"🗃 <b>Прочее</b>:\n"
            f"{get_other_info()}"
        )
        return await self.bot.edit_message_text(
            inline_message_id=call.inline_message_id,
            text=message,
            reply_markup=INFO_MARKUP.as_markup()
        )