# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import json
import logging
import math

from aiogram.types import (
    InlineQuery,
    CallbackQuery,
    InlineKeyboardButton,
    Message as AioMessage,
    InlineQueryResultArticle,
    InputTextMessageContent,
    ChosenInlineResult,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pyrogram import Client

from .. import loader, utils


@loader.module(author="ConfigUI", version=1.4)
class ConfiguratorMod(loader.Module):
    """
    Конфигуратор для Xioca ModuleConfig:
    - .config открывает inline UI
    - список модулей с пагинацией
    - скрытые параметры (toggle show/hide)
    - авто-рендер по типу:
        * bool -> Toggle
        * Choice -> кнопки вариантов
        * int/float -> +/- step
        * остальное -> Set через inline ввод (switch_inline_query_current_chat)
    - Reset
    """

    strings = {
        "ru": {
            "choose_mod": "⚙️ <b>Конфигуратор</b>\nВыбери модуль:",
            "choose_key": "⚙️ <b>Конфиг:</b> <code>{mod}</code>\nВыбери параметр:",
            "view": (
                "⚙️ <b>Конфиг:</b> <code>{mod}</code>\n"
                "<b>Параметр:</b> <code>{opt}</code>{hidden}\n"
                "<b>Тип:</b> <code>{typ}</code>\n"
                "<b>Описание:</b> {desc}\n\n"
                "<b>Значение:</b>\n<pre>{val}</pre>"
            ),
            "hidden_mark": " <emoji id=5210952531676504517>🙈</emoji>",
            "btn_back": "⬅️ Назад",
            "btn_close": "✖️ Закрыть",
            "btn_toggle": "🔁 Toggle",
            "btn_set": "✏️ Set",
            "btn_reset": "♻️ Reset",
            "btn_show_hidden": "👁 Показать скрытые",
            "btn_hide_hidden": "🙈 Скрыть скрытые",

            "set_inline_title": "✏️ Установка значения",
            "set_inline_text": (
                "✏️ <b>Установка значения</b>\n"
                "<b>Модуль:</b> <code>{mod}</code>\n"
                "<b>Параметр:</b> <code>{opt}</code>\n\n"
                "Нажми кнопку ниже — откроется inline-ввод.\n"
                "Допиши значение в конце строки и выбери <b>Apply</b>."
            ),
            "btn_set_inline": "✍️ Ввести значение",
            "saved": "✅ Сохранено: <code>{mod}.{opt}</code> = <code>{val}</code>",
            "bad_value": "❌ Некорректное значение: {err}",
            "not_your": "❗ Эта кнопка не твоя!",
            "no_cfg": "🤷‍♂️ Модулей с конфигом не найдено.",

            "token_expired": "⏳ Токен устарел. Открой Set заново.",
            "inline_hint_title": "Введите значение",
            "inline_hint_desc": "Допиши значение после токена и выбери Apply",
            "apply_title": "✅ Apply",
            "apply_desc": "{mod}.{opt} = {val}",
        },

        "en": {
            "choose_mod": "⚙️ <b>Configurator</b>\nChoose module:",
            "choose_key": "⚙️ <b>Config:</b> <code>{mod}</code>\nChoose option:",
            "view": (
                "⚙️ <b>Config:</b> <code>{mod}</code>\n"
                "<b>Option:</b> <code>{opt}</code>{hidden}\n"
                "<b>Type:</b> <code>{typ}</code>\n"
                "<b>Description:</b> {desc}\n\n"
                "<b>Value:</b>\n<pre>{val}</pre>"
            ),
            "hidden_mark": " 🙈",
            "btn_back": "⬅️ Back",
            "btn_close": "✖️ Close",
            "btn_toggle": "🔁 Toggle",
            "btn_set": "✏️ Set",
            "btn_reset": "♻️ Reset",
            "btn_show_hidden": "👁 Show hidden",
            "btn_hide_hidden": "🙈 Hide hidden",

            "set_inline_title": "✏️ Set value",
            "set_inline_text": (
                "✏️ <b>Set value</b>\n"
                "<b>Module:</b> <code>{mod}</code>\n"
                "<b>Option:</b> <code>{opt}</code>\n\n"
                "Press the button below to open inline input.\n"
                "Append value to the end of the line and choose <b>Apply</b>."
            ),
            "btn_set_inline": "✍️ Enter value",
            "saved": "✅ Saved: <code>{mod}.{opt}</code> = <code>{val}</code>",
            "bad_value": "❌ Invalid value: {err}",
            "not_your": "❗ Not your button!",
            "no_cfg": "🤷‍♂️ No modules with config.",

            "token_expired": "⏳ Token expired. Open Set again.",
            "inline_hint_title": "Type value",
            "inline_hint_desc": "Append value after token and choose Apply",
            "apply_title": "✅ Apply",
            "apply_desc": "{mod}.{opt} = {val}",
        },

        "be": {
            "choose_mod": "⚙️ <b>Канфігуратар</b>\nАбяры модуль:",
            "choose_key": "⚙️ <b>Канфіг:</b> <code>{mod}</code>\nАбяры параметр:",
            "view": (
                "⚙️ <b>Канфіг:</b> <code>{mod}</code>\n"
                "<b>Параметр:</b> <code>{opt}</code>{hidden}\n"
                "<b>Тып:</b> <code>{typ}</code>\n"
                "<b>Апісанне:</b> {desc}\n\n"
                "<b>Значэнне:</b>\n<pre>{val}</pre>"
            ),
            "hidden_mark": " 🙈",
            "btn_back": "⬅️ Назад",
            "btn_close": "✖️ Закрыць",
            "btn_toggle": "🔁 Пераключыць",
            "btn_set": "✏️ Усталяваць",
            "btn_reset": "♻️ Скінуць",
            "btn_show_hidden": "👁 Паказаць схаваныя",
            "btn_hide_hidden": "🙈 Схаваць схаваныя",

            "set_inline_title": "✏️ Усталяванне значэння",
            "set_inline_text": (
                "✏️ <b>Усталяванне значэння</b>\n"
                "<b>Модуль:</b> <code>{mod}</code>\n"
                "<b>Параметр:</b> <code>{opt}</code>\n\n"
                "Націсні кнопку ніжэй — адкрыецца inline-ўвод.\n"
                "Дапішы значэнне і абяры <b>Apply</b>."
            ),
            "btn_set_inline": "✍️ Увесці значэнне",
            "saved": "✅ Захавана: <code>{mod}.{opt}</code> = <code>{val}</code>",
            "bad_value": "❌ Няправільнае значэнне: {err}",
            "not_your": "❗ Гэта не твая кнопка!",
            "no_cfg": "🤷‍♂️ Няма модуляў з канфігам.",

            "token_expired": "⏳ Токен састарэў. Адкрый Set нанова.",
            "inline_hint_title": "Увядзі значэнне",
            "inline_hint_desc": "Дапішы значэнне і абяры Apply",
            "apply_title": "✅ Apply",
            "apply_desc": "{mod}.{opt} = {val}",
        },

        "de": {
            "choose_mod": "⚙️ <b>Konfigurator</b>\nModul auswählen:",
            "choose_key": "⚙️ <b>Konfiguration:</b> <code>{mod}</code>\nOption auswählen:",
            "view": (
                "⚙️ <b>Konfiguration:</b> <code>{mod}</code>\n"
                "<b>Option:</b> <code>{opt}</code>{hidden}\n"
                "<b>Typ:</b> <code>{typ}</code>\n"
                "<b>Beschreibung:</b> {desc}\n\n"
                "<b>Wert:</b>\n<pre>{val}</pre>"
            ),
            "hidden_mark": " 🙈",
            "btn_back": "⬅️ Zurück",
            "btn_close": "✖️ Schließen",
            "btn_toggle": "🔁 Umschalten",
            "btn_set": "✏️ Setzen",
            "btn_reset": "♻️ Zurücksetzen",
            "btn_show_hidden": "👁 Versteckte anzeigen",
            "btn_hide_hidden": "🙈 Versteckte ausblenden",

            "set_inline_title": "✏️ Wert setzen",
            "set_inline_text": (
                "✏️ <b>Wert setzen</b>\n"
                "<b>Modul:</b> <code>{mod}</code>\n"
                "<b>Option:</b> <code>{opt}</code>\n\n"
                "Drücke den Button unten für Inline-Eingabe.\n"
                "Wert anhängen und <b>Apply</b> wählen."
            ),
            "btn_set_inline": "✍️ Wert eingeben",
            "saved": "✅ Gespeichert: <code>{mod}.{opt}</code> = <code>{val}</code>",
            "bad_value": "❌ Ungültiger Wert: {err}",
            "not_your": "❗ Nicht dein Button!",
            "no_cfg": "🤷‍♂️ Keine Module mit Konfiguration.",

            "token_expired": "⏳ Token abgelaufen. Öffne Set erneut.",
            "inline_hint_title": "Wert eingeben",
            "inline_hint_desc": "Wert anhängen und Apply wählen",
            "apply_title": "✅ Apply",
            "apply_desc": "{mod}.{opt} = {val}",
        },

        "es": {
            "choose_mod": "⚙️ <b>Configurador</b>\nElige un módulo:",
            "choose_key": "⚙️ <b>Configuración:</b> <code>{mod}</code>\nElige una opción:",
            "view": (
                "⚙️ <b>Configuración:</b> <code>{mod}</code>\n"
                "<b>Opción:</b> <code>{opt}</code>{hidden}\n"
                "<b>Tipo:</b> <code>{typ}</code>\n"
                "<b>Descripción:</b> {desc}\n\n"
                "<b>Valor:</b>\n<pre>{val}</pre>"
            ),
            "hidden_mark": " 🙈",
            "btn_back": "⬅️ Atrás",
            "btn_close": "✖️ Cerrar",
            "btn_toggle": "🔁 Alternar",
            "btn_set": "✏️ Establecer",
            "btn_reset": "♻️ Restablecer",
            "btn_show_hidden": "👁 Mostrar ocultos",
            "btn_hide_hidden": "🙈 Ocultar ocultos",

            "set_inline_title": "✏️ Establecer valor",
            "set_inline_text": (
                "✏️ <b>Establecer valor</b>\n"
                "<b>Módulo:</b> <code>{mod}</code>\n"
                "<b>Opción:</b> <code>{opt}</code>\n\n"
                "Pulsa el botón para abrir entrada inline.\n"
                "Añade el valor y elige <b>Apply</b>."
            ),
            "btn_set_inline": "✍️ Introducir valor",
            "saved": "✅ Guardado: <code>{mod}.{opt}</code> = <code>{val}</code>",
            "bad_value": "❌ Valor inválido: {err}",
            "not_your": "❗ ¡Este botón no es tuyo!",
            "no_cfg": "🤷‍♂️ No hay módulos con configuración.",

            "token_expired": "⏳ Token expirado. Abre Set de nuevo.",
            "inline_hint_title": "Introduce un valor",
            "inline_hint_desc": "Añade el valor y elige Apply",
            "apply_title": "✅ Apply",
            "apply_desc": "{mod}.{opt} = {val}",
        },

        "fr": {
            "choose_mod": "⚙️ <b>Configurateur</b>\nChoisissez un module :",
            "choose_key": "⚙️ <b>Configuration :</b> <code>{mod}</code>\nChoisissez une option :",
            "view": (
                "⚙️ <b>Configuration :</b> <code>{mod}</code>\n"
                "<b>Option :</b> <code>{opt}</code>{hidden}\n"
                "<b>Type :</b> <code>{typ}</code>\n"
                "<b>Description :</b> {desc}\n\n"
                "<b>Valeur :</b>\n<pre>{val}</pre>"
            ),
            "hidden_mark": " 🙈",
            "btn_back": "⬅️ Retour",
            "btn_close": "✖️ Fermer",
            "btn_toggle": "🔁 Basculer",
            "btn_set": "✏️ Définir",
            "btn_reset": "♻️ Réinitialiser",
            "btn_show_hidden": "👁 Afficher masqués",
            "btn_hide_hidden": "🙈 Masquer masqués",

            "set_inline_title": "✏️ Définir la valeur",
            "set_inline_text": (
                "✏️ <b>Définir la valeur</b>\n"
                "<b>Module :</b> <code>{mod}</code>\n"
                "<b>Option :</b> <code>{opt}</code>\n\n"
                "Appuyez sur le bouton pour l’entrée inline.\n"
                "Ajoutez la valeur puis choisissez <b>Apply</b>."
            ),
            "btn_set_inline": "✍️ Entrer la valeur",
            "saved": "✅ Enregistré : <code>{mod}.{opt}</code> = <code>{val}</code>",
            "bad_value": "❌ Valeur invalide : {err}",
            "not_your": "❗ Ce bouton n’est pas le vôtre !",
            "no_cfg": "🤷‍♂️ Aucun module configurable.",

            "token_expired": "⏳ Jeton expiré. Rouvrez Set.",
            "inline_hint_title": "Entrez une valeur",
            "inline_hint_desc": "Ajoutez la valeur et choisissez Apply",
            "apply_title": "✅ Apply",
            "apply_desc": "{mod}.{opt} = {val}",
        },

        "it": {
            "choose_mod": "⚙️ <b>Configuratore</b>\nScegli un modulo:",
            "choose_key": "⚙️ <b>Configurazione:</b> <code>{mod}</code>\nScegli un’opzione:",
            "view": (
                "⚙️ <b>Configurazione:</b> <code>{mod}</code>\n"
                "<b>Opzione:</b> <code>{opt}</code>{hidden}\n"
                "<b>Tipo:</b> <code>{typ}</code>\n"
                "<b>Descrizione:</b> {desc}\n\n"
                "<b>Valore:</b>\n<pre>{val}</pre>"
            ),
            "hidden_mark": " 🙈",
            "btn_back": "⬅️ Indietro",
            "btn_close": "✖️ Chiudi",
            "btn_toggle": "🔁 Attiva/disattiva",
            "btn_set": "✏️ Imposta",
            "btn_reset": "♻️ Ripristina",
            "btn_show_hidden": "👁 Mostra nascosti",
            "btn_hide_hidden": "🙈 Nascondi nascosti",

            "set_inline_title": "✏️ Imposta valore",
            "set_inline_text": (
                "✏️ <b>Imposta valore</b>\n"
                "<b>Modulo:</b> <code>{mod}</code>\n"
                "<b>Opzione:</b> <code>{opt}</code>\n\n"
                "Premi il pulsante per l’input inline.\n"
                "Aggiungi il valore e scegli <b>Apply</b>."
            ),
            "btn_set_inline": "✍️ Inserisci valore",
            "saved": "✅ Salvato: <code>{mod}.{opt}</code> = <code>{val}</code>",
            "bad_value": "❌ Valore non valido: {err}",
            "not_your": "❗ Questo pulsante non è tuo!",
            "no_cfg": "🤷‍♂️ Nessun modulo configurabile.",

            "token_expired": "⏳ Token scaduto. Apri Set di nuovo.",
            "inline_hint_title": "Inserisci un valore",
            "inline_hint_desc": "Aggiungi il valore e scegli Apply",
            "apply_title": "✅ Apply",
            "apply_desc": "{mod}.{opt} = {val}",
        },

        "kk": {
            "choose_mod": "⚙️ <b>Конфигуратор</b>\nМодульді таңдаңыз:",
            "choose_key": "⚙️ <b>Конфиг:</b> <code>{mod}</code>\nПараметрді таңдаңыз:",
            "view": (
                "⚙️ <b>Конфиг:</b> <code>{mod}</code>\n"
                "<b>Параметр:</b> <code>{opt}</code>{hidden}\n"
                "<b>Түрі:</b> <code>{typ}</code>\n"
                "<b>Сипаттама:</b> {desc}\n\n"
                "<b>Мәні:</b>\n<pre>{val}</pre>"
            ),
            "hidden_mark": " 🙈",
            "btn_back": "⬅️ Артқа",
            "btn_close": "✖️ Жабу",
            "btn_toggle": "🔁 Ауыстыру",
            "btn_set": "✏️ Орнату",
            "btn_reset": "♻️ Қалпына келтіру",
            "btn_show_hidden": "👁 Жасырындарды көрсету",
            "btn_hide_hidden": "🙈 Жасырындарды жасыру",

            "set_inline_title": "✏️ Мән орнату",
            "set_inline_text": (
                "✏️ <b>Мән орнату</b>\n"
                "<b>Модуль:</b> <code>{mod}</code>\n"
                "<b>Параметр:</b> <code>{opt}</code>\n\n"
                "Төмендегі батырманы басыңыз — inline енгізу ашылады.\n"
                "Мәнді енгізіп, <b>Apply</b> таңдаңыз."
            ),
            "btn_set_inline": "✍️ Мән енгізу",
            "saved": "✅ Сақталды: <code>{mod}.{opt}</code> = <code>{val}</code>",
            "bad_value": "❌ Қате мән: {err}",
            "not_your": "❗ Бұл сіздің батырмаңыз емес!",
            "no_cfg": "🤷‍♂️ Конфигі бар модульдер жоқ.",

            "token_expired": "⏳ Токен ескірді. Set қайта ашыңыз.",
            "inline_hint_title": "Мән енгізіңіз",
            "inline_hint_desc": "Мәнді енгізіп, Apply таңдаңыз",
            "apply_title": "✅ Apply",
            "apply_desc": "{mod}.{opt} = {val}",
        },

        "uz": {
            "choose_mod": "⚙️ <b>Konfigurator</b>\nModulni tanlang:",
            "choose_key": "⚙️ <b>Konfig:</b> <code>{mod}</code>\nParametrni tanlang:",
            "view": (
                "⚙️ <b>Konfig:</b> <code>{mod}</code>\n"
                "<b>Parametr:</b> <code>{opt}</code>{hidden}\n"
                "<b>Turi:</b> <code>{typ}</code>\n"
                "<b>Tavsif:</b> {desc}\n\n"
                "<b>Qiymat:</b>\n<pre>{val}</pre>"
            ),
            "hidden_mark": " 🙈",
            "btn_back": "⬅️ Orqaga",
            "btn_close": "✖️ Yopish",
            "btn_toggle": "🔁 O‘zgartirish",
            "btn_set": "✏️ O‘rnatish",
            "btn_reset": "♻️ Tiklash",
            "btn_show_hidden": "👁 Yashirinlarni ko‘rsatish",
            "btn_hide_hidden": "🙈 Yashirinlarni yashirish",

            "set_inline_title": "✏️ Qiymat o‘rnatish",
            "set_inline_text": (
                "✏️ <b>Qiymat o‘rnatish</b>\n"
                "<b>Modul:</b> <code>{mod}</code>\n"
                "<b>Parametr:</b> <code>{opt}</code>\n\n"
                "Quyidagi tugmani bosing — inline kiritish ochiladi.\n"
                "Qiymatni kiriting va <b>Apply</b> ni tanlang."
            ),
            "btn_set_inline": "✍️ Qiymat kiritish",
            "saved": "✅ Saqlandi: <code>{mod}.{opt}</code> = <code>{val}</code>",
            "bad_value": "❌ Noto‘g‘ri qiymat: {err}",
            "not_your": "❗ Bu sizning tugmangiz emas!",
            "no_cfg": "🤷‍♂️ Konfigli modullar topilmadi.",

            "token_expired": "⏳ Token eskirgan. Set ni qayta oching.",
            "inline_hint_title": "Qiymat kiriting",
            "inline_hint_desc": "Qiymatni kiriting va Apply ni tanlang",
            "apply_title": "✅ Apply",
            "apply_desc": "{mod}.{opt} = {val}",
        },
    }

    _UI = "xioca.configurator.ui"
    _PENDING = "xioca.configurator.pending"

    _SETINLINE = "xioca.configurator.setinline"

    _PER_PAGE = 8
    
    @loader.command("cfg")
    async def config_cmd(self, app: Client, message):
        await utils.inline(self, message, "config")

    @loader.inline("config")
    async def config_inline_handler(self, app: Client, inline_query: InlineQuery):
        mods = self._get_cfg_modules()
        if not mods:
            return await utils.answer_inline(inline_query, self.S("no_cfg"), "Config", None)

        kb = self._kb_modules(mods, page=0)
        await utils.answer_inline(inline_query, self.S("choose_mod"), "Config", kb)

    @loader.inline("cfgset", hide=True)
    async def cfgset_inline_handler(self, app: Client, inline_query: InlineQuery):
        q = (inline_query.query or "").strip()
        parts = q.split(maxsplit=2)

        if len(parts) < 2:
            res = InlineQueryResultArticle(
                id="hint",
                title=self.S("inline_hint_title"),
                description=self.S("inline_hint_desc"),
                input_message_content=InputTextMessageContent(
                    message_text=self.S("inline_hint_desc")
                ),
            )
            return await inline_query.answer([res], cache_time=0, is_personal=True)

        token = parts[1]
        value = parts[2] if len(parts) >= 3 else ""

        ctx = self.db.get(self._SETINLINE, token, None)
        if not ctx:
            res = InlineQueryResultArticle(
                id="expired",
                title=self.S("token_expired"),
                description=self.S("token_expired"),
                input_message_content=InputTextMessageContent(
                    message_text=self.S("token_expired")
                ),
            )
            return await inline_query.answer([res], cache_time=0, is_personal=True)

        mod, opt = ctx["mod"], ctx["opt"]

        desc_val = (value[:64] + "…") if len(value) > 64 else (value if value else "∅")

        res = InlineQueryResultArticle(
            id=f"cfgapply:{token}",
            title=self.S("apply_title"),
            description=self.S("apply_desc", mod=mod, opt=opt, val=desc_val),
            input_message_content=InputTextMessageContent(
                message_text=f"✅ {mod}.{opt} = {desc_val}"
            ),
        )
        return await inline_query.answer([res], cache_time=0, is_personal=True)

    @loader.callback("cfgui")
    async def cfgui_callback(self, app: Client, call: CallbackQuery):
        if call.from_user.id != self.all_modules.me.id:
            return await call.answer(self.S("not_your"), True)

        parts = (call.data or "").split("_", 2)
        if len(parts) < 2:
            return await call.answer("ERR", True)

        action = parts[1]
        token = parts[2] if len(parts) > 2 else None

        try:
            if action == "close":
                return await self._edit_inline(call, "✅", None)

            if action == "mods":
                mods = self._get_cfg_modules()
                page = self._load(token).get("page", 0) if token else 0
                page = int(page)
                kb = self._kb_modules(mods, page=page)
                return await self._edit_inline(call, self.S("choose_mod"), kb)

            if action == "mods_page":
                st = self._load(token)
                page = int(st.get("page", 0))
                mods = self._get_cfg_modules()
                kb = self._kb_modules(mods, page=page)
                return await self._edit_inline(call, self.S("choose_mod"), kb)

            if action == "mod":
                st = self._load(token)
                mod = st["mod"]
                page = int(st.get("page", 0))
                show_hidden = bool(st.get("show_hidden", False))
                kb = self._kb_options(mod, page=page, show_hidden=show_hidden)
                return await self._edit_inline(call, self.S("choose_key", mod=mod), kb)

            if action == "mod_page":
                st = self._load(token)
                mod = st["mod"]
                page = int(st.get("page", 0))
                show_hidden = bool(st.get("show_hidden", False))
                kb = self._kb_options(mod, page=page, show_hidden=show_hidden)
                return await self._edit_inline(call, self.S("choose_key", mod=mod), kb)

            if action == "hidden":
                st = self._load(token)
                mod = st["mod"]
                st["show_hidden"] = not bool(st.get("show_hidden", False))
                kb = self._kb_options(mod, page=int(st.get("page", 0)), show_hidden=bool(st["show_hidden"]))
                return await self._edit_inline(call, self.S("choose_key", mod=mod), kb)

            if action == "view":
                st = self._load(token)
                mod = st["mod"]
                opt = st["opt"]
                back_page = int(st.get("page", 0))
                show_hidden = bool(st.get("show_hidden", False))
                text, kb = self._render_view(mod, opt, back_page=back_page, show_hidden=show_hidden)
                return await self._edit_inline(call, text, kb)

            if action == "toggle":
                st = self._load(token)
                mod, opt = st["mod"], st["opt"]
                m = self._find_mod(mod)
                cur = m.config.get(opt)
                if isinstance(cur, bool):
                    m.config.set(opt, not cur)
                    await call.answer("✅")
                back_page = int(st.get("page", 0))
                show_hidden = bool(st.get("show_hidden", False))
                text, kb = self._render_view(mod, opt, back_page=back_page, show_hidden=show_hidden)
                return await self._edit_inline(call, text, kb)

            if action == "reset":
                st = self._load(token)
                mod, opt = st["mod"], st["opt"]
                m = self._find_mod(mod)
                m.config.reset(opt)
                await call.answer("♻️")
                back_page = int(st.get("page", 0))
                show_hidden = bool(st.get("show_hidden", False))
                text, kb = self._render_view(mod, opt, back_page=back_page, show_hidden=show_hidden)
                return await self._edit_inline(call, text, kb)

            if action == "setinline":
                st = self._load(token)
                mod, opt = st["mod"], st["opt"]

                set_token = utils.random_id()
                self.db.set(self._SETINLINE, set_token, {
                    "mod": mod,
                    "opt": opt,
                    "inline_id": call.inline_message_id,
                    "back": {"page": int(st.get("page", 0)), "show_hidden": bool(st.get("show_hidden", False))}
                })

                kb = InlineKeyboardBuilder()
                kb.row(
                    InlineKeyboardButton(
                        text=self.S("btn_set_inline"),
                        switch_inline_query_current_chat=f"cfgset {set_token} "
                    )
                )

                kb.row(InlineKeyboardButton(text=self.S("btn_back"), callback_data=f"cfgui_view_{token}"))
                kb.row(InlineKeyboardButton(text=self.S("btn_close"), callback_data="cfgui_close_0"))

                await call.answer("✏️", False)
                return await self._edit_inline(call, self.S("set_inline_text", mod=mod, opt=opt), kb.as_markup())

            if action == "choice":
                st = self._load(token)
                mod, opt, val = st["mod"], st["opt"], st["val"]
                m = self._find_mod(mod)
                m.config.set(opt, val)
                await call.answer("✅")
                back_page = int(st.get("page", 0))
                show_hidden = bool(st.get("show_hidden", False))
                text, kb = self._render_view(mod, opt, back_page=back_page, show_hidden=show_hidden)
                return await self._edit_inline(call, text, kb)

            if action in ("inc", "dec"):
                st = self._load(token)
                mod, opt = st["mod"], st["opt"]
                m = self._find_mod(mod)
                meta = m.config.meta(opt)
                cur = m.config.get(opt)

                step = meta.step
                if step is None:
                    step = 1 if isinstance(cur, int) and not isinstance(cur, bool) else 0.1
                step = float(step)

                if isinstance(cur, bool):
                    return await call.answer("Not numeric", True)

                try:
                    cur_f = float(cur)
                except Exception:
                    return await call.answer("Not numeric", True)

                new_val = cur_f + step if action == "inc" else cur_f - step
                if isinstance(cur, int) and not isinstance(cur, bool) and float(step).is_integer() and float(new_val).is_integer():
                    new_val = int(new_val)

                if isinstance(new_val, float):
                    new_val = float(f"{new_val:.10g}")

                m.config.set(opt, new_val)
                await call.answer("✅")

                back_page = int(st.get("page", 0))
                show_hidden = bool(st.get("show_hidden", False))
                text, kb = self._render_view(mod, opt, back_page=back_page, show_hidden=show_hidden)
                return await self._edit_inline(call, text, kb)

        except Exception as e:
            logging.exception(e)
            return await call.answer("ERR", True)

    async def chosen_inline_result_message_handler(self, app: Client, chosen: ChosenInlineResult):
        try:
            rid = str(getattr(chosen, "result_id", "") or "")
            if not rid.startswith("cfgapply:"):
                return

            token = rid.split(":", 1)[1]
            ctx = self.db.get(self._SETINLINE, token, None)
            if not ctx:
                return

            q = (getattr(chosen, "query", "") or "").strip()
            parts = q.split(maxsplit=2)
            if len(parts) < 3:
                value_text = ""
            else:
                value_text = parts[2]

            mod, opt = ctx["mod"], ctx["opt"]
            inline_id = ctx.get("inline_id")
            back = ctx.get("back", {"page": 0, "show_hidden": False})

            m = self._find_mod(mod)
            m.config.parse_and_set(opt, value_text)
            val = m.config.get(opt)

            if inline_id:
                text, kb = self._render_view(
                    mod, opt,
                    back_page=int(back.get("page", 0)),
                    show_hidden=bool(back.get("show_hidden", False))
                )
                await self.bot.edit_message_text(
                    inline_message_id=inline_id,
                    text=text,
                    reply_markup=kb,
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )

            try:
                await self.bot.send_message(
                    chosen.from_user.id,
                    self.S("saved", mod=mod, opt=opt, val=self._pretty(val)),
                    disable_web_page_preview=True
                )
            except Exception:
                pass

        except Exception as e:
            logging.exception(e)
            try:
                await self.bot.send_message(chosen.from_user.id, self.S("bad_value", err=str(e)))
            except Exception:
                pass
        finally:
            try:
                self.db.remove(self._SETINLINE, token)
            except Exception:
                pass

    async def config_message_handler(self, app: Client, message: AioMessage):
        if not message.reply_to_message:
            return

        pending = self.db.get(self._PENDING, str(message.reply_to_message.message_id), None)
        if not pending:
            return

        mod = pending["mod"]
        opt = pending["opt"]
        inline_id = pending["inline_id"]
        back = pending.get("back", {"page": 0, "show_hidden": False})

        try:
            m = self._find_mod(mod)
            m.config.parse_and_set(opt, message.text or "")
            val = m.config.get(opt)

            await self.bot.send_message(
                message.chat.id,
                self.S("saved", mod=mod, opt=opt, val=self._pretty(val))
            )

            text, kb = self._render_view(mod, opt, back_page=int(back.get("page", 0)), show_hidden=bool(back.get("show_hidden", False)))
            await self.bot.edit_message_text(
                inline_message_id=inline_id,
                text=text,
                reply_markup=kb,
                parse_mode="HTML",
                disable_web_page_preview=True
            )

        except Exception as e:
            await self.bot.send_message(message.chat.id, self.S("bad_value", err=str(e)))
        finally:
            self.db.remove(self._PENDING, str(message.reply_to_message.message_id))

    def _kb_modules(self, mods, page: int):
        total_pages = max(1, math.ceil(len(mods) / self._PER_PAGE))
        page = max(0, min(page, total_pages - 1))

        start = page * self._PER_PAGE
        chunk = mods[start:start + self._PER_PAGE]

        kb = InlineKeyboardBuilder()

        for mod in chunk:
            token = self._stash({"mod": mod, "page": 0, "show_hidden": False})
            kb.row(InlineKeyboardButton(text=f"📦 {mod}", callback_data=f"cfgui_mod_{token}"))

        nav = InlineKeyboardBuilder()
        if page > 0:
            token_prev = self._stash({"page": page - 1})
            nav.add(InlineKeyboardButton(text="◀️", callback_data=f"cfgui_mods_page_{token_prev}"))
        nav.add(InlineKeyboardButton(text=f"{page+1}/{total_pages}", callback_data=f"cfgui_mods_{self._stash({'page':page})}"))
        if page < total_pages - 1:
            token_next = self._stash({"page": page + 1})
            nav.add(InlineKeyboardButton(text="▶️", callback_data=f"cfgui_mods_page_{token_next}"))
        kb.row(*nav.buttons)

        kb.row(InlineKeyboardButton(text=self.S("btn_close"), callback_data="cfgui_close_0"))
        return kb.as_markup()

    def _kb_options(self, mod: str, page: int, show_hidden: bool):
        m = self._find_mod(mod)
        opts = m.config.keys(include_hidden=show_hidden)

        total_pages = max(1, math.ceil(len(opts) / self._PER_PAGE))
        page = max(0, min(page, total_pages - 1))

        start = page * self._PER_PAGE
        chunk = opts[start:start + self._PER_PAGE]

        kb = InlineKeyboardBuilder()

        for opt in chunk:
            cur = m.config.get(opt)
            meta = m.config.meta(opt)

            icon = "✅" if isinstance(cur, bool) and cur else ("❌" if isinstance(cur, bool) else "⚙️")
            if meta.hidden:
                icon = "🙈"

            token = self._stash({"mod": mod, "opt": opt, "page": page, "show_hidden": show_hidden})
            kb.row(InlineKeyboardButton(text=f"{icon} {opt}", callback_data=f"cfgui_view_{token}"))

        if show_hidden:
            t = self._stash({"mod": mod, "page": page, "show_hidden": True})
            kb.row(InlineKeyboardButton(text=self.S("btn_hide_hidden"), callback_data=f"cfgui_hidden_{t}"))
        else:
            t = self._stash({"mod": mod, "page": page, "show_hidden": False})
            kb.row(InlineKeyboardButton(text=self.S("btn_show_hidden"), callback_data=f"cfgui_hidden_{t}"))

        nav = InlineKeyboardBuilder()
        if page > 0:
            tprev = self._stash({"mod": mod, "page": page - 1, "show_hidden": show_hidden})
            nav.add(InlineKeyboardButton(text="◀️", callback_data=f"cfgui_mod_page_{tprev}"))
        nav.add(InlineKeyboardButton(text=f"{page+1}/{total_pages}", callback_data=f"cfgui_mod_{self._stash({'mod':mod,'page':page,'show_hidden':show_hidden})}"))
        if page < total_pages - 1:
            tnext = self._stash({"mod": mod, "page": page + 1, "show_hidden": show_hidden})
            nav.add(InlineKeyboardButton(text="▶️", callback_data=f"cfgui_mod_page_{tnext}"))
        kb.row(*nav.buttons)

        kb.row(InlineKeyboardButton(text=self.S("btn_back"), callback_data=f"cfgui_mods_{self._stash({'page':0})}"))
        kb.row(InlineKeyboardButton(text=self.S("btn_close"), callback_data="cfgui_close_0"))
        return kb.as_markup()

    def _render_view(self, mod: str, opt: str, back_page: int, show_hidden: bool):
        m = self._find_mod(mod)
        meta = m.config.meta(opt)
        val = m.config.get(opt)

        typ = type(val).__name__
        hidden_mark = self.S("hidden_mark") if meta.hidden else ""

        text = self.S(
            "view",
            mod=mod,
            opt=opt,
            hidden=hidden_mark,
            typ=typ,
            desc=(meta.description or "-"),
            val=self._pretty(val)
        )

        kb = InlineKeyboardBuilder()

        if isinstance(val, bool):
            t = self._stash({"mod": mod, "opt": opt, "page": back_page, "show_hidden": show_hidden})
            kb.row(InlineKeyboardButton(text=self.S("btn_toggle"), callback_data=f"cfgui_toggle_{t}"))

        if isinstance(meta.validator, loader.Choice):
            row = []
            for choice in meta.validator.choices:
                label = f"✅ {choice}" if choice == val else choice
                t = self._stash({"mod": mod, "opt": opt, "val": choice, "page": back_page, "show_hidden": show_hidden})
                row.append(InlineKeyboardButton(text=label, callback_data=f"cfgui_choice_{t}"))
                if len(row) == 2:
                    kb.row(*row)
                    row = []
            if row:
                kb.row(*row)

        if isinstance(val, (int, float)) and not isinstance(val, bool) and not isinstance(meta.validator, loader.Choice):
            step = meta.step
            if step is None:
                step = 1 if isinstance(val, int) else 0.1
            step_txt = str(step).rstrip("0").rstrip(".") if isinstance(step, float) else str(step)
            tdec = self._stash({"mod": mod, "opt": opt, "page": back_page, "show_hidden": show_hidden})
            tinc = self._stash({"mod": mod, "opt": opt, "page": back_page, "show_hidden": show_hidden})
            kb.row(
                InlineKeyboardButton(text=f"➖ {step_txt}", callback_data=f"cfgui_dec_{tdec}"),
                InlineKeyboardButton(text=f"➕ {step_txt}", callback_data=f"cfgui_inc_{tinc}"),
            )

        tset = self._stash({"mod": mod, "opt": opt, "page": back_page, "show_hidden": show_hidden})
        kb.row(InlineKeyboardButton(text=self.S("btn_set"), callback_data=f"cfgui_setinline_{tset}"))

        treset = self._stash({"mod": mod, "opt": opt, "page": back_page, "show_hidden": show_hidden})
        kb.row(InlineKeyboardButton(text=self.S("btn_reset"), callback_data=f"cfgui_reset_{treset}"))

        tback = self._stash({"mod": mod, "page": back_page, "show_hidden": show_hidden})
        kb.row(InlineKeyboardButton(text=self.S("btn_back"), callback_data=f"cfgui_mod_{tback}"))
        kb.row(InlineKeyboardButton(text=self.S("btn_close"), callback_data="cfgui_close_0"))

        return text, kb.as_markup()

    def _get_cfg_modules(self):
        mods = []
        for m in self.all_modules.modules:
            if hasattr(m, "config") and isinstance(getattr(m, "config"), loader.ModuleConfig):
                mods.append(m.name)
        return sorted(mods)

    def _find_mod(self, name: str):
        for m in self.all_modules.modules:
            if m.name == name:
                return m
        raise RuntimeError("Module not found")

    async def _edit_inline(self, call: CallbackQuery, text: str, reply_markup):
        return await self.bot.edit_message_text(
            inline_message_id=call.inline_message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    def _stash(self, payload: dict) -> str:
        token = utils.random_id()
        self.db.set(self._UI, token, payload)
        return token

    def _load(self, token: str) -> dict:
        st = self.db.get(self._UI, token, None)
        if not st:
            raise RuntimeError("Expired")
        return st

    @staticmethod
    def _pretty(val):
        if val is None:
            return "null"
        if isinstance(val, (dict, list)):
            return json.dumps(val, ensure_ascii=False, indent=2)
        return str(val)