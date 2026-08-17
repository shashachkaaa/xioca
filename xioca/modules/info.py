# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import platform
from datetime import datetime

from herokutl.tl.custom import Message
from herokutl.utils import get_display_name

from .. import loader, utils
from ..inline.types import InlineCall
from ..version import __version__

__start_time__ = datetime.now()


@loader.tds
class XiocaInfoMod(loader.Module):
    """Информация о юзерботе"""

    strings = {
        "name": 'XiocaInfo',
        'info_full': '<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n➖➖➖➖➖➖➖➖➖➖\n👤 <b>Owner:</b> {mention}\n📦 <b>Modules:</b> <code>{count}</code>\n🕰 <b>Uptime:</b> <code>{uptime}</code>\n🐍 <b>Python:</b> <code>{py_ver}</code>\n⌨️ <b>Prefixes:</b> <code>{prefixes}</code>\n➖➖➖➖➖➖➖➖➖➖\n<i>💭 System active and ready.</i>',
        'btn_refresh': '🔄 Refresh',
        'btn_close': '🗑️ Close',
        'access_denied': '🚫 Access denied',
        'dont_touch': "🚫 Don't touch!",
        'refreshed': '✅ Data updated',
        'no_changes': 'Nothing changed',
        'closed': '<i>❌ Panel closed</i>',
        'no_prefix': 'None',
        'time_d': 'd',
        'time_h': 'h',
        'time_m': 'm',
        'time_s': 's',
    }

    strings_ru = {
        'info_full': '<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n➖➖➖➖➖➖➖➖➖➖\n👤 <b>Владелец:</b> {mention}\n📦 <b>Модули:</b> <code>{count}</code>\n🕰 <b>Аптайм:</b> <code>{uptime}</code>\n🐍 <b>Python:</b> <code>{py_ver}</code>\n⌨️ <b>Префиксы:</b> <code>{prefixes}</code>\n➖➖➖➖➖➖➖➖➖➖\n<i>💭 System active and ready.</i>',
        'btn_refresh': '🔄 Обновить',
        'btn_close': '🗑️ Закрыть',
        'access_denied': '🚫 Доступ запрещен',
        'dont_touch': '🚫 Не трогай!',
        'refreshed': '✅ Данные обновлены',
        'no_changes': 'Ничего не изменилось',
        'closed': '<i>❌ Панель закрыта</i>',
        'no_prefix': 'Нет',
        'time_d': 'д',
        'time_h': 'ч',
        'time_m': 'м',
        'time_s': 'с',
    }

    strings_be = {
        'info_full': '<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n➖➖➖➖➖➖➖➖➖➖\n👤 <b>Уладальнік:</b> {mention}\n📦 <b>Модулі:</b> <code>{count}</code>\n🕰 <b>Аптайм:</b> <code>{uptime}</code>\n🐍 <b>Python:</b> <code>{py_ver}</code>\n⌨️ <b>Прэфіксы:</b> <code>{prefixes}</code>\n➖➖➖➖➖➖➖➖➖➖\n<i>💭 System active and ready.</i>',
        'btn_refresh': '🔄 Абнавіць',
        'btn_close': '🗑️ Закрыць',
        'access_denied': '🚫 Доступ забаронены',
        'dont_touch': '🚫 Не чапай!',
        'refreshed': '✅ Даныя абноўлены',
        'no_changes': 'Нічога не змянілася',
        'closed': '<i>❌ Панэль закрыта</i>',
        'no_prefix': 'Няма',
        'time_d': 'дз',
        'time_h': 'г',
        'time_m': 'хв',
        'time_s': 'с',
    }

    strings_de = {
        'info_full': '<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n➖➖➖➖➖➖➖➖➖➖\n👤 <b>Besitzer:</b> {mention}\n📦 <b>Module:</b> <code>{count}</code>\n🕰 <b>Uptime:</b> <code>{uptime}</code>\n🐍 <b>Python:</b> <code>{py_ver}</code>\n⌨️ <b>Präfixe:</b> <code>{prefixes}</code>\n➖➖➖➖➖➖➖➖➖➖\n<i>💭 System active and ready.</i>',
        'btn_refresh': '🔄 Aktualisieren',
        'btn_close': '🗑️ Schließen',
        'access_denied': '🚫 Zugriff verweigert',
        'dont_touch': '🚫 Nicht berühren!',
        'refreshed': '✅ Daten aktualisiert',
        'no_changes': 'Nichts geändert',
        'closed': '<i>❌ Panel geschlossen</i>',
        'no_prefix': 'Keine',
        'time_d': 't',
        'time_h': 'st',
        'time_m': 'm',
        'time_s': 's',
    }

    strings_es = {
        'info_full': '<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n➖➖➖➖➖➖➖➖➖➖\n👤 <b>Propietario:</b> {mention}\n📦 <b>Módulos:</b> <code>{count}</code>\n🕰 <b>Uptime:</b> <code>{uptime}</code>\n🐍 <b>Python:</b> <code>{py_ver}</code>\n⌨️ <b>Prefixes:</b> <code>{prefixes}</code>\n➖➖➖➖➖➖➖➖➖➖\n<i>💭 System active and ready.</i>',
        'btn_refresh': '🔄 Actualizar',
        'btn_close': '🗑️ Cerrar',
        'access_denied': '🚫 Acceso denegado',
        'dont_touch': '🚫 ¡No tocar!',
        'refreshed': '✅ Datos actualizados',
        'no_changes': 'Nada ha cambiado',
        'closed': '<i>❌ Panel cerrado</i>',
        'no_prefix': 'Ninguno',
        'time_d': 'd',
        'time_h': 'h',
        'time_m': 'm',
        'time_s': 's',
    }

    strings_fr = {
        'info_full': '<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n➖➖➖➖➖➖➖➖➖➖\n👤 <b>Propriétaire:</b> {mention}\n📦 <b>Modules:</b> <code>{count}</code>\n🕰 <b>Uptime:</b> <code>{uptime}</code>\n🐍 <b>Python:</b> <code>{py_ver}</code>\n⌨️ <b>Préfixes:</b> <code>{prefixes}</code>\n➖➖➖➖➖➖➖➖➖➖\n<i>💭 System active and ready.</i>',
        'btn_refresh': '🔄 Actualiser',
        'btn_close': '🗑️ Fermer',
        'access_denied': '🚫 Accès refusé',
        'dont_touch': '🚫 Ne pas toucher !',
        'refreshed': '✅ Données mises à jour',
        'no_changes': "Rien n'a changé",
        'closed': '<i>❌ Panneau fermé</i>',
        'no_prefix': 'Aucun',
        'time_d': 'j',
        'time_h': 'h',
        'time_m': 'm',
        'time_s': 's',
    }

    strings_it = {
        'info_full': '<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n➖➖➖➖➖➖➖➖➖➖\n👤 <b>Proprietario:</b> {mention}\n📦 <b>Moduli:</b> <code>{count}</code>\n🕰 <b>Uptime:</b> <code>{uptime}</code>\n🐍 <b>Python:</b> <code>{py_ver}</code>\n⌨️ <b>Prefissi:</b> <code>{prefixes}</code>\n➖➖➖➖➖➖➖➖➖➖\n<i>💭 System active and ready.</i>',
        'btn_refresh': '🔄 Aggiorna',
        'btn_close': '🗑️ Chiudi',
        'access_denied': '🚫 Accesso negato',
        'dont_touch': '🚫 Non toccare!',
        'refreshed': '✅ Dati aggiornati',
        'no_changes': 'Nulla è cambiato',
        'closed': '<i>❌ Pannello chiuso</i>',
        'no_prefix': 'Nessuno',
        'time_d': 'g',
        'time_h': 'h',
        'time_m': 'm',
        'time_s': 's',
    }

    strings_kk = {
        'info_full': '<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n➖➖➖➖➖➖➖➖➖➖\n👤 <b>Иесі:</b> {mention}\n📦 <b>Модульдер:</b> <code>{count}</code>\n🕰 <b>Аптайм:</b> <code>{uptime}</code>\n🐍 <b>Python:</b> <code>{py_ver}</code>\n⌨️ <b>Префикстер:</b> <code>{prefixes}</code>\n➖➖➖➖➖➖➖➖➖➖\n<i>💭 System active and ready.</i>',
        'btn_refresh': '🔄 Жаңарту',
        'btn_close': '🗑️ Жабу',
        'access_denied': '🚫 Рұқсат етілмеген',
        'dont_touch': '🚫 Тіпті тиіспе!',
        'refreshed': '✅ Мәліметтер жаңартылды',
        'no_changes': 'Өзгеріс жоқ',
        'closed': '<i>❌ Панель жабылды</i>',
        'no_prefix': 'Жоқ',
        'time_d': 'к',
        'time_h': 'с',
        'time_m': 'м',
        'time_s': 'с',
    }

    strings_uz = {
        'info_full': '<b>👾 Xioca UserBot</b> <code>v{ver}</code>\n➖➖➖➖➖➖➖➖➖➖\n👤 <b>Ega:</b> {mention}\n📦 <b>Modullar:</b> <code>{count}</code>\n🕰 <b>Uptime:</b> <code>{uptime}</code>\n🐍 <b>Python:</b> <code>{py_ver}</code>\n⌨️ <b>Prefixlar:</b> <code>{prefixes}</code>\n➖➖➖➖➖➖➖➖➖➖\n<i>💭 System active and ready.</i>',
        'btn_refresh': '🔄 Yangilash',
        'btn_close': '🗑️ Yopish',
        'access_denied': '🚫 Kirish taqiqlangan',
        'dont_touch': '🚫 Tegmang!',
        'refreshed': "✅ Ma'lumotlar yangilandi",
        'no_changes': "Hech narsa o'zgarmadi",
        'closed': '<i>❌ Panel yopildi</i>',
        'no_prefix': "Yo'q",
        'time_d': 'k',
        'time_h': 's',
        'time_m': 'm',
        'time_s': 's',
    }


    def _uptime(self) -> str:
        """Формирует строку аптайма"""
        seconds = int((datetime.now() - __start_time__).total_seconds())
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        parts = []
        if days:
            parts.append(f"{days}{self.strings('time_d')}")
        if hours:
            parts.append(f"{hours}{self.strings('time_h')}")
        if minutes:
            parts.append(f"{minutes}{self.strings('time_m')}")
        if not parts:
            parts.append(f"{seconds}{self.strings('time_s')}")

        return " ".join(parts[:2])

    def _text(self) -> str:
        """Собирает текст инфо-панели"""
        me = self._client.heroku_me
        mention = (
            f"<a href='tg://user?id={me.id}'>"
            f"{utils.escape_html(get_display_name(me))}</a>"
        )

        prefixes = sorted(self.get_prefixes())

        return self.strings("info_full").format(
            ver=".".join(map(str, __version__)),
            mention=mention,
            count=len(self.allmodules.modules),
            uptime=self._uptime(),
            py_ver=platform.python_version(),
            prefixes=(
                " | ".join(map(utils.escape_html, prefixes))
                if prefixes
                else self.strings("no_prefix")
            ),
        )

    def _markup(self) -> list:
        return [
            {"text": self.strings("btn_refresh"), "callback": self._refresh},
            {"text": self.strings("btn_close"), "action": "close"},
        ]

    @loader.command()
    async def infocmd(self, message: Message):
        """Показать инфо-панель"""
        await self.inline.form(
            message=message,
            text=self._text(),
            reply_markup=self._markup(),
        )

    async def _refresh(self, call: InlineCall):
        """Обработчик кнопки «Обновить»"""
        await call.edit(text=self._text(), reply_markup=self._markup())
        await call.answer(self.strings("refreshed"))
