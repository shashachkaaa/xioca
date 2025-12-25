# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

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


@loader.module("Xioca Info")
class InformationMod(loader.Module):
    """Информация о юзерботе"""

    strings = {
        "ru": {
            "info_full": (
                "<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "👤 <b>Владелец:</b> {mention}\n"
                "📦 <b>Модули:</b> <code>{count}</code>\n"
                "🕰 <b>Аптайм:</b> <code>{uptime}</code>\n"
                "🐍 <b>Python:</b> <code>{py_ver}</code>\n"
                "⌨️ <b>Префиксы:</b> <code>{prefixes}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "<i>💭 System active and ready.</i>"
            ),
            "btn_refresh": "🔄 Обновить",
            "btn_close": "🗑️ Закрыть",
            "access_denied": "🚫 Доступ запрещен",
            "dont_touch": "🚫 Не трогай!",
            "refreshed": "✅ Данные обновлены",
            "no_changes": "Ничего не изменилось",
            "closed": "<i>❌ Панель закрыта</i>",
            "no_prefix": "Нет",
            "time_d": "д", "time_h": "ч", "time_m": "м", "time_s": "с"
        },
        "en": {
            "info_full": (
                "<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "👤 <b>Owner:</b> {mention}\n"
                "📦 <b>Modules:</b> <code>{count}</code>\n"
                "🕰 <b>Uptime:</b> <code>{uptime}</code>\n"
                "🐍 <b>Python:</b> <code>{py_ver}</code>\n"
                "⌨️ <b>Prefixes:</b> <code>{prefixes}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "<i>💭 System active and ready.</i>"
            ),
            "btn_refresh": "🔄 Refresh",
            "btn_close": "🗑️ Close",
            "access_denied": "🚫 Access denied",
            "dont_touch": "🚫 Don't touch!",
            "refreshed": "✅ Data updated",
            "no_changes": "Nothing changed",
            "closed": "<i>❌ Panel closed</i>",
            "no_prefix": "None",
            "time_d": "d", "time_h": "h", "time_m": "m", "time_s": "s"
        },
        "be": {
            "info_full": (
                "<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "👤 <b>Уладальнік:</b> {mention}\n"
                "📦 <b>Модулі:</b> <code>{count}</code>\n"
                "🕰 <b>Аптайм:</b> <code>{uptime}</code>\n"
                "🐍 <b>Python:</b> <code>{py_ver}</code>\n"
                "⌨️ <b>Прэфіксы:</b> <code>{prefixes}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "<i>💭 System active and ready.</i>"
            ),
            "btn_refresh": "🔄 Абнавіць",
            "btn_close": "🗑️ Закрыць",
            "access_denied": "🚫 Доступ забаронены",
            "dont_touch": "🚫 Не чапай!",
            "refreshed": "✅ Даныя абноўлены",
            "no_changes": "Нічога не змянілася",
            "closed": "<i>❌ Панэль закрыта</i>",
            "no_prefix": "Няма",
            "time_d": "дз", "time_h": "г", "time_m": "хв", "time_s": "с"
        },
        "de": {
            "info_full": (
                "<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "👤 <b>Besitzer:</b> {mention}\n"
                "📦 <b>Module:</b> <code>{count}</code>\n"
                "🕰 <b>Uptime:</b> <code>{uptime}</code>\n"
                "🐍 <b>Python:</b> <code>{py_ver}</code>\n"
                "⌨️ <b>Präfixe:</b> <code>{prefixes}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "<i>💭 System active and ready.</i>"
            ),
            "btn_refresh": "🔄 Aktualisieren",
            "btn_close": "🗑️ Schließen",
            "access_denied": "🚫 Zugriff verweigert",
            "dont_touch": "🚫 Nicht berühren!",
            "refreshed": "✅ Daten aktualisiert",
            "no_changes": "Nichts geändert",
            "closed": "<i>❌ Panel geschlossen</i>",
            "no_prefix": "Keine",
            "time_d": "t", "time_h": "st", "time_m": "m", "time_s": "s"
        },
        "es": {
            "info_full": (
                "<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "👤 <b>Propietario:</b> {mention}\n"
                "📦 <b>Módulos:</b> <code>{count}</code>\n"
                "🕰 <b>Uptime:</b> <code>{uptime}</code>\n"
                "🐍 <b>Python:</b> <code>{py_ver}</code>\n"
                "⌨️ <b>Prefixes:</b> <code>{prefixes}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "<i>💭 System active and ready.</i>"
            ),
            "btn_refresh": "🔄 Actualizar",
            "btn_close": "🗑️ Cerrar",
            "access_denied": "🚫 Acceso denegado",
            "dont_touch": "🚫 ¡No tocar!",
            "refreshed": "✅ Datos actualizados",
            "no_changes": "Nada ha cambiado",
            "closed": "<i>❌ Panel cerrado</i>",
            "no_prefix": "Ninguno",
            "time_d": "d", "time_h": "h", "time_m": "m", "time_s": "s"
        },
        "fr": {
            "info_full": (
                "<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "👤 <b>Propriétaire:</b> {mention}\n"
                "📦 <b>Modules:</b> <code>{count}</code>\n"
                "🕰 <b>Uptime:</b> <code>{uptime}</code>\n"
                "🐍 <b>Python:</b> <code>{py_ver}</code>\n"
                "⌨️ <b>Préfixes:</b> <code>{prefixes}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "<i>💭 System active and ready.</i>"
            ),
            "btn_refresh": "🔄 Actualiser",
            "btn_close": "🗑️ Fermer",
            "access_denied": "🚫 Accès refusé",
            "dont_touch": "🚫 Ne pas toucher !",
            "refreshed": "✅ Données mises à jour",
            "no_changes": "Rien n'a changé",
            "closed": "<i>❌ Panneau fermé</i>",
            "no_prefix": "Aucun",
            "time_d": "j", "time_h": "h", "time_m": "m", "time_s": "s"
        },
        "it": {
            "info_full": (
                "<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "👤 <b>Proprietario:</b> {mention}\n"
                "📦 <b>Moduli:</b> <code>{count}</code>\n"
                "🕰 <b>Uptime:</b> <code>{uptime}</code>\n"
                "🐍 <b>Python:</b> <code>{py_ver}</code>\n"
                "⌨️ <b>Prefissi:</b> <code>{prefixes}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "<i>💭 System active and ready.</i>"
            ),
            "btn_refresh": "🔄 Aggiorna",
            "btn_close": "🗑️ Chiudi",
            "access_denied": "🚫 Accesso negato",
            "dont_touch": "🚫 Non toccare!",
            "refreshed": "✅ Dati aggiornati",
            "no_changes": "Nulla è cambiato",
            "closed": "<i>❌ Pannello chiuso</i>",
            "no_prefix": "Nessuno",
            "time_d": "g", "time_h": "h", "time_m": "m", "time_s": "s"
        },
        "kk": {
            "info_full": (
                "<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "👤 <b>Иесі:</b> {mention}\n"
                "📦 <b>Модульдер:</b> <code>{count}</code>\n"
                "🕰 <b>Аптайм:</b> <code>{uptime}</code>\n"
                "🐍 <b>Python:</b> <code>{py_ver}</code>\n"
                "⌨️ <b>Префикстер:</b> <code>{prefixes}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "<i>💭 System active and ready.</i>"
            ),
            "btn_refresh": "🔄 Жаңарту",
            "btn_close": "🗑️ Жабу",
            "access_denied": "🚫 Рұқсат етілмеген",
            "dont_touch": "🚫 Тіпті тиіспе!",
            "refreshed": "✅ Мәліметтер жаңартылды",
            "no_changes": "Өзгеріс жоқ",
            "closed": "<i>❌ Панель жабылды</i>",
            "no_prefix": "Жоқ",
            "time_d": "к", "time_h": "с", "time_m": "м", "time_s": "с"
        },
        "uz": {
            "info_full": (
                "<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "👤 <b>Ega:</b> {mention}\n"
                "📦 <b>Modullar:</b> <code>{count}</code>\n"
                "🕰 <b>Uptime:</b> <code>{uptime}</code>\n"
                "🐍 <b>Python:</b> <code>{py_ver}</code>\n"
                "⌨️ <b>Prefixlar:</b> <code>{prefixes}</code>\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
                "<i>💭 System active and ready.</i>"
            ),
            "btn_refresh": "🔄 Yangilash",
            "btn_close": "🗑️ Yopish",
            "access_denied": "🚫 Kirish taqiqlangan",
            "dont_touch": "🚫 Tegmang!",
            "refreshed": "✅ Ma'lumotlar yangilandi",
            "no_changes": "Hech narsa o'zgarmadi",
            "closed": "<i>❌ Panel yopildi</i>",
            "no_prefix": "Yo'q",
            "time_d": "k", "time_h": "s", "time_m": "m", "time_s": "s"
        }
    }

    def _get_uptime_str(self) -> str:
        """Формирует красивую строку аптайма"""
        uptime = datetime.now() - __start_time__
        seconds = int(uptime.total_seconds())
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        
        parts = []
        if days > 0: parts.append(f"{days}{self.S('time_d')}")
        if hours > 0: parts.append(f"{hours}{self.S('time_h')}")
        if minutes > 0: parts.append(f"{minutes}{self.S('time_m')}")
        if not parts: parts.append(f"{seconds}{self.S('time_s')}")
        
        return " ".join(parts[:2])

    def _get_info_text(self, me: types.User, modules_count: int, prefixes: list) -> str:
        """Генерирует основной текст сообщения"""
        mention = f"<a href='tg://user?id={me.id}'>{utils.get_display_name(me)}</a>"
        prefix_str = " | ".join(prefixes) if prefixes else self.S("no_prefix")
        
        return self.S(
            "info_full",
            ver=__version__,
            mention=mention,
            count=modules_count,
            uptime=self._get_uptime_str(),
            py_ver=platform.python_version(),
            prefixes=prefix_str
        )

    def _get_keyboard(self):
        """Клавиатура"""
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text=self.S("btn_refresh"), callback_data="refresh"),
            InlineKeyboardButton(text=self.S("btn_close"), callback_data="close")
        )
        return builder.as_markup()

    async def info_cmd(self, app: Client, message: types.Message):
        """Показать инфо-панель. Использование: .info"""
        await utils.inline(self, message, "info")

    @loader.on_bot(lambda self, app, inline_query: True)
    async def info_inline_handler(self, app: Client, inline_query: InlineQuery):
        """Инлайн обработчик"""
        me = self.all_modules.me
        modules_count = len(self.all_modules.modules)
        prefixes = self.db.get("xioca.loader", "prefixes", ["."]) 
        
        text = self._get_info_text(me, modules_count, prefixes)
        keyboard = self._get_keyboard()
        
        await utils.answer_inline(inline_query, text, "Xioca Info", keyboard)

    async def refresh_callback_handler(self, app: Client, call: CallbackQuery):
        """Обработчик кнопки 'Обновить'"""
        if call.data != "refresh":
            return

        allowed_ids = self.db.get("xioca.loader", "allow", [])
        owner_id = self.all_modules.me.id
        
        if call.from_user.id != owner_id and call.from_user.id not in allowed_ids:
            return await call.answer(self.S("access_denied"), show_alert=True)

        modules_count = len(self.all_modules.modules)
        prefixes = self.db.get("xioca.loader", "prefixes", ["."])
        
        text = self._get_info_text(self.all_modules.me, modules_count, prefixes)
        keyboard = self._get_keyboard()

        try:
            await self.bot.edit_message_text(
                inline_message_id=call.inline_message_id,
                text=text,
                reply_markup=keyboard
            )
            await call.answer(self.S("refreshed"))
        except Exception:
            await call.answer(self.S("no_changes"))

    async def close_callback_handler(self, app: Client, call: CallbackQuery):
        """Обработчик кнопки 'Закрыть'"""
        if call.data != "close":
            return

        allowed_ids = self.db.get("xioca.loader", "allow", [])
        owner_id = self.all_modules.me.id

        if call.from_user.id != owner_id and call.from_user.id not in allowed_ids:
            return await call.answer(self.S("dont_touch"), show_alert=True)
            
        try:
             await self.bot.edit_message_text(
                inline_message_id=call.inline_message_id,
                text=self.S("closed"),
                reply_markup=None
            )
        except Exception:
            pass
