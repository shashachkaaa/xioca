# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

"""Инлайн-меню управления юзерботом.

От версии на pyrogram осталось только меню: остальное, что было зашито в
botmanager (логи, обновление, менеджер модулей, инфо, настройки), теперь
существует отдельными командами рантайма, и меню просто вызывает их.

Панель SQL-запросов не перенесена намеренно: она выполняла произвольный код
над базой из чата бота, полностью дублируя .eval, и была самой опасной
частью старого меню.
"""

import logging

from herokutl.tl.custom import Message

from .. import loader, utils
from .._internal import restart
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)


@loader.tds
class XiocaManagerMod(loader.Module):
    """Меню управления юзерботом"""

    strings = {
        "name": "XiocaManager",
        'btn_control': '🎛 Userbot Control',
        'btn_restart': '🔄 Restart Userbot',
        'btn_check_update': '🆕 Check for Updates',
        'btn_logs': '📤 Get Logs',
        'btn_back': '◀ Back',
        'uptime_prefix': '⌚ <b>Uptime:</b> {uptime}\n',
        'status_on': '🟢 Userbot active',
        'status_off': '🔴 Userbot disabled',
        'control_menu': '🎛 With this menu you can <b>control the userbot</b>.\n\n<b>{status}\n🌙 Installed modules:</b> {count}\n✏ <b>Prefix(es):</b> ({prefix})\n{uptime}\n👇 <i>Press any button below to perform an action.</i>',
        'not_your_btn': 'Not your button!',
        'sad_emoji': '😢',
        'welcome_text': '👋 <b>Welcome</b>, I am part of your userbot <code>Xioca</code>, here you can find settings, info and more.\n\n👇 <i>Press any button below for details.</i>',
        'restarting_alert': '🔄 Xioca is restarting, please wait...',
        'latest_ver': '✅ You have the latest version of Xioca!',
    }

    strings_ru = {
        'btn_control': '🎛 Управление юзерботом',
        'btn_restart': '🔄 Перезагрузить юзербота',
        'btn_check_update': '🆕 Проверить наличие обновлений',
        'btn_logs': '📤 Получить логи',
        'btn_back': '◀ Назад',
        'uptime_prefix': '⌚ <b>Прошло времени с момента запуска:</b> {uptime}\n',
        'status_on': '🟢 Юзербот активен',
        'status_off': '🔴 Юзербот выключен',
        'control_menu': '🎛 С помощью этого меню вы сможете <b>управлять юзерботом</b>.\n\n<b>{status}\n🌙 Установлено модулей:</b> {count}\n✏ <b>Префикс(ы):</b> ({prefix})\n{uptime}\n👇 <i>Жми любую кнопку ниже что бы выполнить какое либо действие с юзерботом.</i>',
        'not_your_btn': 'Кнопка не ваша!',
        'sad_emoji': '😢',
        'welcome_text': '👋 <b>Приветствую</b>, я - часть твоего юзербота <code>Xioca</code>, тут ты можешь найти настройки юзербота, информацию и прочее.\n\n👇 <i>Жми любую кнопку ниже что бы узнать подробности.</i>',
        'restarting_alert': '🔄 Xioca перезагружается, ожидайте...',
        'latest_ver': '✅ У вас установлена последняя версия Xioca!',
    }

    strings_be = {
        'btn_control': '🎛 Кіраванне юзерботам',
        'btn_restart': '🔄 Перазагрузіць юзербота',
        'btn_check_update': '🆕 Праверыць наяўнасць абнаўленняў',
        'btn_logs': '📤 Атрымаць логі',
        'btn_back': '◀ Назад',
        'uptime_prefix': '⌚ <b>Час працы з моманту запуску:</b> {uptime}\n',
        'status_on': '🟢 Юзербот актыўны',
        'status_off': '🔴 Юзербот выключаны',
        'control_menu': '🎛 З дапамогай гэтага меню вы зможаце <b>кіраваць юзерботам</b>.\n\n<b>{status}\n🌙 Усталявана модуляў:</b> {count}\n✏ <b>Прэфікс(ы):</b> ({prefix})\n{uptime}\n👇 <i>Цісні любую кнопку ніжэй каб выканаць дзеянне з юзерботам.</i>',
        'not_your_btn': 'Кнопка не ваша!',
        'sad_emoji': '😢',
        'welcome_text': '👋 <b>Вітаю</b>, я - частка твайго юзербота <code>Xioca</code>, тут ты можаш знайсці налады, інфармацыю і іншае.\n\n👇 <i>Цісні любую кнопку ніжэй каб даведацца падрабязнасці.</i>',
        'restarting_alert': '🔄 Xioca перазагружаецца, пачакайце...',
        'latest_ver': '✅ У вас усталявана апошняя версія Xioca!',
    }

    strings_de = {
        'btn_control': '🎛 Userbot-Steuerung',
        'btn_restart': '🔄 Userbot neu starten',
        'btn_check_update': '🆕 Nach Updates suchen',
        'btn_logs': '📤 Logs abrufen',
        'btn_back': '◀ Zurück',
        'uptime_prefix': '⌚ <b>Laufzeit seit Start:</b> {uptime}\n',
        'status_on': '🟢 Userbot aktiv',
        'status_off': '🔴 Userbot deaktiviert',
        'control_menu': '🎛 Mit diesem Menü können Sie den <b>Userbot steuern</b>.\n\n<b>{status}\n🌙 Installierte Module:</b> {count}\n✏ <b>Präfix(e):</b> ({prefix})\n{uptime}\n👇 <i>Drücken Sie eine Taste unten, um eine Aktion auszuführen.</i>',
        'not_your_btn': 'Nicht Ihre Schaltfläche!',
        'sad_emoji': '😢',
        'welcome_text': '👋 <b>Willkommen</b>, ich bin Teil deines <code>Xioca</code> Userbots.\n\n👇 <i>Drücken Sie unten für Details.</i>',
        'restarting_alert': '🔄 Xioca startet neu, bitte warten...',
        'latest_ver': '✅ Du hast die neueste Version von Xioca!',
    }

    strings_es = {
        'btn_control': '🎛 Control del Userbot',
        'btn_restart': '🔄 Reiniciar Userbot',
        'btn_check_update': '🆕 Buscar actualizaciones',
        'btn_logs': '📤 Obtener Logs',
        'btn_back': '◀ Volver',
        'uptime_prefix': '⌚ <b>Tiempo activo:</b> {uptime}\n',
        'status_on': '🟢 Userbot activo',
        'status_off': '🔴 Userbot desactivado',
        'control_menu': '🎛 Con este menú puedes <b>controlar el userbot</b>.\n\n<b>{status}\n🌙 Módulos instalados:</b> {count}\n✏ <b>Prefijos:</b> ({prefix})\n{uptime}\n👇 <i>Pulsa cualquier botón para realizar una acción.</i>',
        'not_your_btn': '¡No es tu botón!',
        'sad_emoji': '😢',
        'welcome_text': '👋 <b>Bienvenido</b>, soy parte de tu userbot <code>Xioca</code>, aquí encontrarás ajustes e info.\n\n👇 <i>Pulsa abajo para más detalles.</i>',
        'restarting_alert': '🔄 Reiniciando, espera...',
        'latest_ver': '✅ ¡Tienes la última versión de Xioca!',
    }

    strings_fr = {
        'btn_control': '🎛 Contrôle du Userbot',
        'btn_restart': '🔄 Redémarrer le Userbot',
        'btn_check_update': '🆕 Mises à jour',
        'btn_logs': '📤 Obtenir les Logs',
        'btn_back': '◀ Retour',
        'uptime_prefix': '⌚ <b>Uptime depuis lancement:</b> {uptime}\n',
        'status_on': '🟢 Userbot actif',
        'status_off': '🔴 Userbot désactivé',
        'control_menu': '🎛 Menu de <b>contrôle du userbot</b>.\n\n<b>{status}\n🌙 Modules installés:</b> {count}\n✏ <b>Prefix:</b> ({prefix})\n{uptime}\n👇 <i>Appuyez sur un bouton pour agir.</i>',
        'not_your_btn': 'Pas votre bouton !',
        'sad_emoji': '😢',
        'welcome_text': '👋 <b>Bienvenue</b>, je suis votre userbot <code>Xioca</code>.\n\n👇 <i>Cliquez ci-dessous pour les détails.</i>',
        'restarting_alert': '🔄 Redémarrage, attendez...',
        'latest_ver': '✅ Version à jour !',
    }

    strings_it = {
        'btn_control': '🎛 Controllo Userbot',
        'btn_restart': '🔄 Riavvia Userbot',
        'btn_check_update': '🆕 Aggiornamenti',
        'btn_logs': '📤 Ottieni Log',
        'btn_back': '◀ Indietro',
        'uptime_prefix': "⌚ <b>Uptime dall'avvio:</b> {uptime}\n",
        'status_on': '🟢 Attivo',
        'status_off': '🔴 Disattivato',
        'control_menu': '🎛 Gestione del tuo <b>userbot</b>.\n\n<b>{status}\n🌙 Moduli:</b> {count}\n✏ <b>Prefisso:</b> ({prefix})\n{uptime}\n👇 <i>Usa i tasti sotto per interagire.</i>',
        'not_your_btn': 'Non è il tuo tasto!',
        'sad_emoji': '😢',
        'welcome_text': '👋 <b>Benvenuto</b>, sono parte del tuo userbot <code>Xioca</code>.\n\n👇 <i>Clicca sotto per i dettagli.</i>',
        'restarting_alert': '🔄 Riavvio in corso, attendere...',
        'latest_ver': '✅ Versione aggiornata!',
    }

    strings_kk = {
        'btn_control': '🎛 Юзерботты басқару',
        'btn_restart': '🔄 Юзерботты қайта жүктеу',
        'btn_check_update': '🆕 Жаңартуларды тексеру',
        'btn_logs': '📤 Логтарды алу',
        'btn_back': '◀ Артқа',
        'uptime_prefix': '⌚ <b>Қосылғаннан бергі уақыт:</b> {uptime}\n',
        'status_on': '🟢 Юзербот белсенді',
        'status_off': '🔴 Юзербот өшірулі',
        'control_menu': '🎛 Осы мәзір арқылы <b>юзерботты басқара</b> аласыз.\n\n<b>{status}\n🌙 Орнатылған модульдер:</b> {count}\n✏ <b>Префикс(тер):</b> ({prefix})\n{uptime}\n👇 <i>Юзерботпен әрекет ету үшін кез келген батырманы басыңыз.</i>',
        'not_your_btn': 'Бұл сіздің батырмаңыз емес!',
        'sad_emoji': '😢',
        'welcome_text': '👋 <b>Сәлем</b>, мен сенің <code>Xioca</code> юзерботыңның бөлігімін.\n\n👇 <i>Толығырақ білу үшін төменді басыңыз.</i>',
        'restarting_alert': '🔄 Қайта жүктелуде, күте тұрыңыз...',
        'latest_ver': '✅ Сізде Xioca-ның соңғы нұсқасы орнатылған!',
    }

    strings_uz = {
        'btn_control': '🎛 Yuzerbot boshqaruvi',
        'btn_restart': '🔄 Qayta ishga tushirish',
        'btn_check_update': '🆕 Yangilanishlarni tekshirish',
        'btn_logs': '📤 Loglarni olish',
        'btn_back': '◀ Orqaga',
        'uptime_prefix': '⌚ <b>Ish vaqti:</b> {uptime}\n',
        'status_on': '🟢 Faol',
        'status_off': "🔴 O'chirilgan",
        'control_menu': '🎛 Bu menyu orqali <b>yuzerbotni boshqarish</b> mumkin.\n\n<b>{status}\n🌙 Modullar:</b> {count}\n✏ <b>Prefiks:</b> ({prefix})\n{uptime}\n👇 <i>Harakat bajarish uchun tugmani bosing.</i>',
        'not_your_btn': 'Bu sizning tugmangiz emas!',
        'sad_emoji': '😢',
        'welcome_text': '👋 <b>Xush kelibsiz</b>, men <code>Xioca</code> yuzerbotingman.\n\n👇 <i>Tafsilotlar uchun pastni bosing.</i>',
        'restarting_alert': '🔄 Qayta yuklanmoqda, kuting...',
        'latest_ver': "✅ Sizda oxirgi versiya o'rnatilgan!",
    }


    def _status(self) -> str:
        return self.strings("control_menu").format(
            status=self.strings("status_on"),
            count=len(self.allmodules.modules),
            prefix=utils.escape_html(" | ".join(sorted(self.get_prefixes()))),
            uptime=self.strings("uptime_prefix").format(
                uptime=utils.formatted_uptime()
            ),
        )

    def _markup(self) -> list:
        return [
            [{"text": self.strings("btn_restart"), "callback": self._restart}],
            [{"text": self.strings("btn_check_update"), "callback": self._update}],
            [{"text": self.strings("btn_logs"), "callback": self._logs}],
        ]

    def _guard(self, call: InlineCall) -> bool:
        """Меню управляет юзерботом, поэтому доступно только владельцу"""
        return call.from_user.id == self._client.tg_id

    @loader.command()
    async def managercmd(self, message: Message):
        """Открыть меню управления юзерботом"""
        await self.inline.form(
            message=message,
            text=self._status(),
            reply_markup=self._markup(),
        )

    async def _restart(self, call: InlineCall):
        if not self._guard(call):
            await call.answer(self.strings("not_your_btn"), show_alert=True)
            return

        await call.answer(self.strings("restarting_alert"), show_alert=True)
        await call.edit(text=self.strings("restarting_alert"), reply_markup=[])
        restart()

    async def _update(self, call: InlineCall):
        if not self._guard(call):
            await call.answer(self.strings("not_your_btn"), show_alert=True)
            return

        # Обновление живёт в модуле updater; если он выгружен - честно
        # сообщаем, а не молчим
        updater = self.lookup("Updater")
        if not updater or not hasattr(updater, "checkupdate"):
            await call.answer(self.strings("latest_ver"), show_alert=True)
            return

        await call.answer(self.strings("btn_check_update"))
        await updater.checkupdate(call)

    async def _logs(self, call: InlineCall):
        if not self._guard(call):
            await call.answer(self.strings("not_your_btn"), show_alert=True)
            return

        tester = self.lookup("XiocaTester")
        if not tester:
            await call.answer(self.strings("sad_emoji"), show_alert=True)
            return

        await call.answer(self.strings("btn_logs"))
