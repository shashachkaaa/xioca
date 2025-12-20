import platform
from datetime import datetime
from aiogram.types import (
    InlineQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pyrogram import Client, types
from .. import loader, utils, __version__, __start_time__

def get_uptime_str() -> str:
    """Формирует красивую строку аптайма"""
    uptime = datetime.now() - __start_time__
    seconds = int(uptime.total_seconds())
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    
    parts = []
    if days > 0: parts.append(f"{days}d")
    if hours > 0: parts.append(f"{hours}h")
    if minutes > 0: parts.append(f"{minutes}m")
    if not parts: parts.append(f"{seconds}s")
    
    return " ".join(parts[:2])

def get_info_text(me: types.User, modules_count: int, prefixes: list) -> str:
    """Генерирует основной текст сообщения"""
    mention = f"<a href='tg://user?id={me.id}'>{utils.get_display_name(me)}</a>"
    prefix_str = " | ".join(prefixes) if prefixes else "Нет"
    
    return (
        f"<b>👾 Xioca UserBot</b> <code>v{__version__}</code>\n"
        f"➖➖➖➖➖➖➖➖➖➖\n"
        f"👤 <b>Владелец:</b> {mention}\n"
        f"📦 <b>Модули:</b> <code>{modules_count}</code>\n"
        f"🕰 <b>Аптайм:</b> <code>{get_uptime_str()}</code>\n"
        f"🐍 <b>Python:</b> <code>{platform.python_version()}</code>\n"
        f"⌨️ <b>Префиксы:</b> <code>{prefix_str}</code>\n"
        f"➖➖➖➖➖➖➖➖➖➖\n"
        f"<i>💭 System active and ready.</i>"
    )

def get_keyboard():
    """Клавиатура"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh"),
        InlineKeyboardButton(text="🗑️ Закрыть", callback_data="close")
    )
    return builder.as_markup()


@loader.module("Xioca Info")
class InformationMod(loader.Module):
    """Информация о юзерботе"""

    async def info_cmd(self, app: Client, message: types.Message):
        """Показать инфо-панель. Использование: .info"""
        await utils.inline(self, message, "info")

    @loader.on_bot(lambda self, app, inline_query: True)
    async def info_inline_handler(self, app: Client, inline_query: InlineQuery):
        """Инлайн обработчик"""
        me = self.all_modules.me
        modules_count = len(self.all_modules.modules)
        prefixes = self.db.get("xioca.loader", "prefixes", ["."]) 
        
        text = get_info_text(me, modules_count, prefixes)
        keyboard = get_keyboard()
        
        await utils.answer_inline(inline_query, text, "Xioca Info", keyboard)

    async def refresh_callback_handler(self, app: Client, call: CallbackQuery):
        """Обработчик кнопки 'Обновить'"""
        if call.data != "refresh":
            return

        allowed_ids = self.db.get("xioca.loader", "allow", [])
        owner_id = self.all_modules.me.id
        
        if call.from_user.id != owner_id and call.from_user.id not in allowed_ids:
            return await call.answer("🚫 Доступ запрещен", show_alert=True)

        modules_count = len(self.all_modules.modules)
        prefixes = self.db.get("xioca.loader", "prefixes", ["."])
        
        text = get_info_text(self.all_modules.me, modules_count, prefixes)
        keyboard = get_keyboard()

        try:
            await self.bot.edit_message_text(
                inline_message_id=call.inline_message_id,
                text=text,
                reply_markup=keyboard
            )
            await call.answer("✅ Данные обновлены")
        except Exception:
            await call.answer("Ничего не изменилось")

    async def close_callback_handler(self, app: Client, call: CallbackQuery):
        """Обработчик кнопки 'Закрыть'"""
        if call.data != "close":
            return

        allowed_ids = self.db.get("xioca.loader", "allow", [])
        owner_id = self.all_modules.me.id

        if call.from_user.id != owner_id and call.from_user.id not in allowed_ids:
            return await call.answer("🚫 Не трогай!", show_alert=True)
            
        try:
             await self.bot.edit_message_text(
                inline_message_id=call.inline_message_id,
                text="<i>❌ Панель закрыта</i>",
                reply_markup=None
            )
        except Exception:
            pass
