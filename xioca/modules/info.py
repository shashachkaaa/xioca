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


# Клавиатуры
def get_main_keyboard():
    """Клавиатура для основной информации"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🖥️ Сервер", callback_data="info_server"))
    return builder.as_markup()

def get_back_keyboard():
    """Клавиатура для возврата"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="◀️ Назад", callback_data="info"))
    return builder.as_markup()


def humanize_bytes(num: float) -> str:
    """Конвертирует байты в читаемый формат"""
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}B"
        num /= 1024.0
    return f"{num:.1f}YB"


def get_basic_info(me: types.User) -> str:
    """Основная информация о юзерботе"""
    mention = f"<a href=\"tg://user?id={me.id}\">{utils.get_display_name(me)}</a>"
    uptime = datetime.now() - __start_time__
    uptime_str = str(uptime).split('.')[0]
    
    return f"""🌙 <b>Xioca UserBot</b> <code>v{__version__}</code>

👑 <b>Владелец</b>: {mention}
⏱️ <b>Аптайм</b>: <code>{uptime_str}</code>
📅 <b>Запущен</b>: <code>{__start_time__.strftime('%d.%m.%Y %H:%M:%S')}</code>

💻 <b>Система</b>: <code>{platform.system()} {platform.release()}</code>
🐍 <b>Python</b>: <code>{platform.python_version()}</code>

⚡ <i>Используйте кнопку ниже для информации о сервере...</i>"""


def get_system_info() -> dict:
    """Получает информацию о системе"""
    info = {
        "os": platform.system(),
        "release": platform.release(),
        "arch": " ".join(platform.architecture()),
        "python": platform.python_version()
    }
    
    # Детальная информация об ОС
    if info["os"] == "Linux":
        try:
            with open("/etc/os-release", "r") as f:
                content = "[os]\n" + f.read()
            config = configparser.ConfigParser()
            config.read_string(content)
            info["distro"] = config["os"].get("PRETTY_NAME", "").strip('"') or "Linux"
        except:
            info["distro"] = "Linux"
    elif info["os"] == "Windows":
        info["distro"] = f"Windows {platform.win32_ver()[0]}"
    elif info["os"] == "Darwin":
        info["distro"] = f"macOS {platform.mac_ver()[0]}"
    else:
        info["distro"] = info["os"]
    
    return info


def get_hardware_info() -> dict:
    """Получает информацию об аппаратной части"""
    try:
        # CPU
        cpu_freq = psutil.cpu_freq()
        cpu_info = {
            "usage": psutil.cpu_percent(),
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(),
            "freq": f"{int(cpu_freq.current)}MHz" if cpu_freq else "N/A",
            "max_freq": f"{int(cpu_freq.max)}MHz" if cpu_freq and cpu_freq.max else "N/A"
        }
        
        # RAM
        ram = psutil.virtual_memory()
        ram_info = {
            "used": humanize_bytes(ram.used),
            "total": humanize_bytes(ram.total),
            "percent": ram.percent
        }
        
        # Диски (только корневой раздел)
        disk_info = {}
        try:
            root_disk = psutil.disk_usage('/')
            disk_info = {
                "used": humanize_bytes(root_disk.used),
                "total": humanize_bytes(root_disk.total),
                "percent": root_disk.percent
            }
        except:
            disk_info = {"error": "Не удалось получить информацию"}
        
        return {
            "cpu": cpu_info,
            "ram": ram_info,
            "disk": disk_info
        }
    except Exception as e:
        return {"error": f"Ошибка получения данных: {e}"}


def get_server_info_message() -> str:
    """Формирует сообщение с информацией о сервере"""
    system = get_system_info()
    hardware = get_hardware_info()
    
    if "error" in hardware:
        return f"❌ <b>Ошибка получения информации о сервере:</b>\n<code>{hardware['error']}</code>"
    
    message = [
        "🖥️ <b>Информация о сервере</b>",
        "════════════════════",
        "",
        "<b>⚙️ Система</b>:",
        f"• ОС: <code>{system['distro']}</code>",
        f"• Ядро: <code>{system['release']}</code>",
        f"• Архитектура: <code>{system['arch']}</code>",
        f"• Python: <code>{system['python']}</code>",
        "",
        "<b>🔧 Аппаратная часть</b>:",
        f"• CPU: <code>{hardware['cpu']['cores']}c/{hardware['cpu']['threads']}t</code>",
        f"• Загрузка CPU: <code>{hardware['cpu']['usage']}%</code>",
        f"• Частота: <code>{hardware['cpu']['freq']}</code>",
        f"• RAM: <code>{hardware['ram']['used']}/{hardware['ram']['total']}</code> (<code>{hardware['ram']['percent']}%</code>)",
    ]
    
    # Добавляем информацию о диске, если доступна
    if "error" not in hardware['disk']:
        message.extend([
            f"• Диск: <code>{hardware['disk']['used']}/{hardware['disk']['total']}</code> (<code>{hardware['disk']['percent']}%</code>)"
        ])
    
    message.extend([
        "",
        f"<i>Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>"
    ])
    
    return "\n".join(message)


def is_user_allowed(user_id: int, allowed_ids: list, owner_id: int) -> bool:
    """Проверяет доступ пользователя"""
    return user_id == owner_id or user_id in allowed_ids


@loader.module("sh1tn3t | shashachkaaa")
class InformationMod(loader.Module):
    """Информация о юзерботе"""

    async def info_cmd(self, app: Client, message: types.Message):
        """Вызывает инлайн-команду info. Использование: info"""
        await utils.inline(self, message, "info")

    @loader.on_bot(lambda self, app, inline_query: True)
    async def info_inline_handler(self, app: Client, inline_query: InlineQuery):
        """Информация о юзерботе. Использование: @bot info"""
        message = get_basic_info(self.all_modules.me)
        await utils.answer_inline(inline_query, message, "Информация", get_main_keyboard())

    @loader.on_bot(lambda self, app, call: call.data == "info")
    async def info_callback_handler(self, app: Client, call: CallbackQuery):
        """Обработчик основной информации"""
        allowed_ids = self.db.get("xioca.loader", "allow", [])
        if not is_user_allowed(call.from_user.id, allowed_ids, self.all_modules.me.id):
            return await call.answer("❗ Эта кнопка не для вас!", True)

        await call.answer()
        await self.bot.edit_message_text(
            inline_message_id=call.inline_message_id,
            text=get_basic_info(self.all_modules.me),
            reply_markup=get_main_keyboard()
        )

    @loader.on_bot(lambda self, app, call: call.data == "info_server")
    async def info_server_callback_handler(self, app: Client, call: CallbackQuery):
        """Обработчик информации о сервере"""
        allowed_ids = self.db.get("xioca.loader", "allow", [])
        if not is_user_allowed(call.from_user.id, allowed_ids, self.all_modules.me.id):
            return await call.answer("❗ Эта кнопка не для вас!", True)

        await call.answer()
        await self.bot.edit_message_text(
            inline_message_id=call.inline_message_id,
            text=get_server_info_message(),
            reply_markup=get_back_keyboard()
        )