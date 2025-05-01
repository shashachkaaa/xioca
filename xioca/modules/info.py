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
import socket
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
    
    return f"""🌙 <b>Xioca UserBot</b> <code>v{__version__}</code>

👑 <b>Владелец</b>: {mention}
⏱️ <b>Аптайм</b>: <code>{uptime_str}</code>
📅 <b>Запущен</b>: <code>{__start_time__.strftime('%d.%m.%Y %H:%M:%S')}</code>

💻 <b>Система</b>: <code>{platform.system()} {platform.release()}</code>
🐍 <b>Python</b>: <code>{platform.python_version()}</code>

⚡ <i>Используйте кнопку ниже для подробной информации о сервере...</i>"""


def get_cpu_info():
    """Возвращает информацию о процессоре"""
    try:
        freq = psutil.cpu_freq()
        freq_current = f"{int(freq.current)} MHz" if freq else "Неизвестно"
        freq_max = f"{int(freq.max)} MHz" if freq and freq.max else "Неизвестно"
        
        return (
            f"    - Использование: <b>{int(psutil.cpu_percent())}%</b>\n"
            f"    - Ядра: <b>{psutil.cpu_count(logical=False)}</b> (<b>{psutil.cpu_count()}</b> потоков)\n"
            f"    - Частота: <b>{freq_current}</b> (макс: <b>{freq_max}</b>)"
        )
    except:
        return "    - Не удалось получить информацию о процессоре"


def get_ram_info():
    """Возвращает информацию о памяти"""
    try:
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory() if hasattr(psutil, 'swap_memory') else None
        
        ram_info = (
            f"    - ОЗУ:\n"
            f"      - Занято: <b>{humanize(ram.used)}</b> (<b>{int(ram.percent)}%</b>)\n"
            f"      - Всего: <b>{humanize(ram.total)}</b>"
        )
        
        if swap:
            ram_info += (
                f"\n    - SWAP:\n"
                f"      - Занято: <b>{humanize(swap.used)}</b> (<b>{int(swap.percent)}%</b>)\n"
                f"      - Всего: <b>{humanize(swap.total)}</b>"
            )
        
        return ram_info
    except:
        return "    - Не удалось получить информацию о памяти"


def get_disk_info():
    """Возвращает информацию о дисках"""
    try:
        disks = []
        for part in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disks.append(
                    f"    - <b>{part.device}</b> ({part.fstype}):\n"
                    f"      - Занято: <b>{humanize(usage.used)}</b> (<b>{int(usage.percent)}%</b>)\n"
                    f"      - Всего: <b>{humanize(usage.total)}</b>"
                )
            except:
                continue
        
        return "\n\n".join(disks) if disks else "    - Нет данных о дисках"
    except:
        return "    - Не удалось получить информацию о дисках"


def get_other_info():
    """Возвращает прочую информацию"""
    try:
        os_name = platform.system()
        kernel = platform.release() or "Неизвестно"
        arch = " ".join(platform.architecture()) if hasattr(platform, 'architecture') else "Неизвестно"

        # Для Termux
        if "ANDROID_ROOT" in os.environ:
            try:
                import subprocess
                android_ver = subprocess.check_output(["getprop", "ro.build.version.release"]).decode().strip()
                return (
                    f"    - ОС: <b>Android (Termux)</b>\n"
                    f"    - Версия Android: <b>{android_ver}</b>\n"
                    f"    - Ядро: <b>{kernel}</b>\n"
                    f"    - Архитектура: <b>{arch}</b>"
                )
            except:
                return (
                    f"    - ОС: <b>Android (Termux)</b>\n"
                    f"    - Ядро: <b>{kernel}</b>\n"
                    f"    - Архитектура: <b>{arch}</b>"
                )

        if os_name == "Linux":
            try:
                with open("/etc/os-release", "r") as file:
                    content = "[linux]\n" + file.read()
                
                config = configparser.ConfigParser()
                config.read_string(content)
                
                distro_name = config["linux"].get("PRETTY_NAME", "") or config["linux"].get("NAME", "")
                distro_name = distro_name.strip('"') if distro_name else "Неизвестно"
                
                return (
                    f"    - ОС: <b>Linux</b>\n"
                    f"    - Дистрибутив: <b>{distro_name}</b>\n"
                    f"    - Ядро: <b>{kernel}</b>\n"
                    f"    - Архитектура: <b>{arch}</b>"
                )
            except:
                return (
                    f"    - ОС: <b>Linux</b>\n"
                    f"    - Ядро: <b>{kernel}</b>\n"
                    f"    - Архитектура: <b>{arch}</b>"
                )
        elif os_name == "Windows":
            try:
                win_ver = platform.win32_ver()[0] if hasattr(platform, 'win32_ver') else "Неизвестно"
                return (
                    f"    - ОС: <b>Windows</b>\n"
                    f"    - Версия: <b>{win_ver}</b>\n"
                    f"    - Ядро: <b>{kernel}</b>\n"
                    f"    - Архитектура: <b>{arch}</b>"
                )
            except:
                return (
                    f"    - ОС: <b>Windows</b>\n"
                    f"    - Ядро: <b>{kernel}</b>\n"
                    f"    - Архитектура: <b>{arch}</b>"
                )
        elif os_name == "Darwin":
            try:
                mac_ver = platform.mac_ver()[0] if hasattr(platform, 'mac_ver') else "Неизвестно"
                return (
                    f"    - ОС: <b>macOS</b>\n"
                    f"    - Версия: <b>{mac_ver}</b>\n"
                    f"    - Ядро: <b>{kernel}</b>\n"
                    f"    - Архитектура: <b>{arch}</b>"
                )
            except:
                return (
                    f"    - ОС: <b>macOS</b>\n"
                    f"    - Ядро: <b>{kernel}</b>\n"
                    f"    - Архитектура: <b>{arch}</b>"
                )
        else:
            return (
                f"    - ОС: <b>{os_name}</b>\n"
                f"    - Ядро: <b>{kernel}</b>\n"
                f"    - Архитектура: <b>{arch}</b>"
            )
    except:
        return "    - Не удалось получить информацию о системе"


@loader.module("sh1tn3t | shashachkaaa")
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
                    reply_markup=INFO_SERVER_MARKUP.as_markup(),
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
            f"<b>🖥️ Подробная информация о сервере</b>\n"
            f"════════════════════\n\n"
            f"<b>🔧 Аппаратная часть</b>:\n"
            f"<b>🧠 Процессор</b>:\n"
            f"{get_cpu_info()}\n\n"
            f"<b>💾 Память</b>:\n"
            f"{get_ram_info()}\n\n"
            f"<b>💿 Диски</b>:\n"
            f"{get_disk_info()}\n\n"
            f"<b>⚙️ Система</b>:\n"
            f"{get_other_info()}\n\n"
            f"<i>Последнее обновление: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>"
        )
        return await self.bot.edit_message_text(
            inline_message_id=call.inline_message_id,
            text=message,
            reply_markup=INFO_MARKUP.as_markup()
        )