# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import random
import asyncio
import logging
import re

from aiogram.types import (
    InlineQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from pyrogram import Client, types
from .. import loader, utils, fsm
from ..db import db

def slang_kb():
	kb = InlineKeyboardBuilder()
	
	ru = InlineKeyboardButton(text="🇷🇺 Русский", callback_data="selectlang_ru")
	en = InlineKeyboardButton(text="🇬🇧 English", callback_data="selectlang_en")
	be = InlineKeyboardButton(text="🇧🇾 Беларуская", callback_data="selectlang_be")
	de = InlineKeyboardButton(text="🇩🇪 Deutschland", callback_data="selectlang_de")
	es = InlineKeyboardButton(text="🇪🇸 Español", callback_data="selectlang_es")
	fr = InlineKeyboardButton(text="🇫🇷 Français", callback_data="selectlang_fr")
	it = InlineKeyboardButton(text="🇮🇹 Italiano", callback_data="selectlang_it")
	kk = InlineKeyboardButton(text="🇰🇿 Қазақ тілі", callback_data="selectlang_kk")
	uz = InlineKeyboardButton(text="🇺🇿 Oʻzbek tili", callback_data="selectlang_uz")
	
	kb.row(ru, en, be)
	kb.row(es, fr, it)
	kb.row(kk, uz)
	
	return kb.as_markup()

@loader.module(author="sh1tn3t | shashachkaaa")
class SettingsMod(loader.Module):
    """Настройки бота"""
    
    strings = {
        "ru": {
            "slang": "👇 Выберите язык",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Не верно введены аргументы</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>Максимальное кол-во отображаемых модулей не может быть меньше 10 и больше 100</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Теперь будет отображатся максимум <code>{args}</code> модулей на одной странице</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>На какой префикс нужно изменить?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Префикс был изменен на</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Какой алиас нужно добавить?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Неверно указаны аргументы.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Пример:</b> <code>addalias</code> (новый алиас) (команда)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Такой алиас уже существует</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Такой команды нет</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>Алиас</b> «<code>{alias}</code>» <b>для команды</b> «<code>{cmd}</code>» <b>был добавлен</b>",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>Какой алиас нужно удалить?</b>",
            "alias_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Такого алиаса нет</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>Алиас</b> «<code>{alias}</code>» <b>был удален</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Алиасы отсутствуют</b>",
            "aliases_list": "<emoji id=5956561916573782596>📄</emoji> <b>Список всех алиасов:</b>\n",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Какой модуль нужно скрыть?</b>",
            "mod_already_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>уже скрыт</b>\n\n{text}",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>скрыт</b>\n\n{text}",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Какой модуль нужно показать?</b>",
            "mod_not_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>не скрыт</b>\n\n{text}",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>теперь виден</b>\n\n{text}",
            "no_hidden_mods": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Скрытых модулей нет</b>",
            "hidden_mods_list": "<emoji id=5956561916573782596>📄</emoji> <b>Список скрытых модулей:</b>\n",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Укажите новый юзернейм для бота.</b>",
            "setinline_err": "<emoji id=5210952531676504517>❌</emoji> <b>Некорректный юзернейм. Юзернейм должен содержать только буквы, цифры, подчеркивания, иметь окончание «Bot» и быть длиной не менее 5 символов.</b>",
            "bot_creating": "<emoji id=5195083327597456039>🌙</emoji> <b>Создаю нового бота...</b>",
            "bot_father_err": "<emoji id=5210952531676504517>❌</emoji> <b>Не удалось создать нового бота. Ответ @BotFather:</b> <code>{res}</code>",
            "bot_setting_name": "<emoji id=5195083327597456039>🌙</emoji> <b>Настраиваю имя бота...</b>",
            "bot_setting_avatar": "<emoji id=5195083327597456039>🌙</emoji> <b>Настраиваю аватарку бота...</b>",
            "bot_setting_inline": "<emoji id=5195083327597456039>🌙</emoji> <b>Настраиваю инлайн...</b>",
            "bot_updating_user": "<emoji id=5195083327597456039>🌙</emoji> <b>Обновляю юзернейм бота...</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Инлайн бот <code>@{name}</code> успешно создан! Необходима перезагрузка для применения изменений</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>Никто не имеет доступ к вашему юзерботу!</b>",
            "ownerlist_caption": "<emoji id=5251203410396458957>🛡</emoji> <b>Всего <code>{count}</code> пользователей имеют доступ к вашему юзерботу</b>\n\n",
            "owner_user": "Пользователь",
            "ownerrm_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Необходим ответ на сообщение, ID или username пользователя!</b>",
            "owner_self_err": "<emoji id=5210952531676504517>❌</emoji> <b>Данную команду невозможно выполнить на самом себе!</b>",
            "owner_no_access": "<emoji id=5210952531676504517>❌</emoji> <b>У пользователя нет доступа к юзерботу!</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Права на юзербота у <a href='tg://user?id={id}'>{name}</a> успешно отняты!</b>",
            "owneradd_reply_err": "<emoji id=5210952531676504517>❌</emoji> <b>Необходим ответ на сообщение</b>",
            "owneradd_confirm": "🛡 <b>Вы уверены что хотите предоставить доступ к юзерботу <a href='tg://user?id={id}'>{name}</a>?</b> Он(а) получит доступ ко всем командам вашей Xioca, это может повлечь за собой плохие последствия. Решение может быть принято на ваш страх и риск!",
            "btn_confirm": "✅ Подтвердить",
            "btn_cancel": "❌ Отмена",
            "btn_send_confirm": "🛡 Отправить подтверждение",
            "not_your_button": "❗ Эта кнопка не ваша!",
            "access_granted": "✅ <b>Доступ <a href='tg://user?id={id}'>{name}</a> предоставлен!</b>",
            "access_denied": "❌ <b>Отказано в доступе для <a href='tg://user?id={id}'>{name}</a>!</b>"
        },
        "en": {
            "slang": "👇 Choose language",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Invalid arguments</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>Max modules cannot be less than 10 or more than 100</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Now up to <code>{args}</code> modules will be displayed on one page</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Which prefix should I set?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Prefix has been changed to</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Which alias should I add?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Invalid arguments.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Example:</b> <code>addalias</code> (new alias) (command)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>This alias already exists</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Command not found</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>for command</b> «<code>{cmd}</code>» <b>has been added</b>",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>Which alias should I delete?</b>",
            "alias_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Alias not found</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>was deleted</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>No aliases found</b>",
            "aliases_list": "<emoji id=5956561916573782596>📄</emoji> <b>List of all aliases:</b>\n",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Which module should I hide?</b>",
            "mod_already_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Module</b> «<code>{mod}</code>» <b>is already hidden</b>\n\n{text}",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>Module</b> «<code>{mod}</code>» <b>is hidden</b>\n\n{text}",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Which module should I show?</b>",
            "mod_not_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Module</b> «<code>{mod}</code>» <b>is not hidden</b>\n\n{text}",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>Module</b> «<code>{mod}</code>» is now visible\n\n{text}",
            "no_hidden_mods": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>No hidden modules</b>",
            "hidden_mods_list": "<emoji id=5956561916573782596>📄</emoji> <b>List of hidden modules:</b>\n",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Specify new username for the bot.</b>",
            "setinline_err": "<emoji id=5210952531676504517>❌</emoji> <b>Incorrect username. Username must contain letters, numbers, underscores, end with «Bot», and be at least 5 characters long.</b>",
            "bot_creating": "<emoji id=5195083327597456039>🌙</emoji> <b>Creating new bot...</b>",
            "bot_father_err": "<emoji id=5210952531676504517>❌</emoji> <b>Failed to create bot. @BotFather says:</b> <code>{res}</code>",
            "bot_setting_name": "<emoji id=5195083327597456039>🌙</emoji> <b>Setting bot name...</b>",
            "bot_setting_avatar": "<emoji id=5195083327597456039>🌙</emoji> <b>Setting bot avatar...</b>",
            "bot_setting_inline": "<emoji id=5195083327597456039>🌙</emoji> <b>Setting inline...</b>",
            "bot_updating_user": "<emoji id=5195083327597456039>🌙</emoji> <b>Updating bot username...</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Inline bot <code>@{name}</code> created! Restart required to apply changes</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>No one has access to your userbot!</b>",
            "ownerlist_caption": "<emoji id=5251203410396458957>🛡</emoji> <b>Total <code>{count}</code> users have access to your userbot</b>\n\n",
            "owner_user": "User",
            "ownerrm_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Reply to a message, or provide ID/username!</b>",
            "owner_self_err": "<emoji id=5210952531676504517>❌</emoji> <b>You cannot perform this on yourself!</b>",
            "owner_no_access": "<emoji id=5210952531676504517>❌</emoji> <b>User has no access!</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Access for <a href='tg://user?id={id}'>{name}</a> revoked!</b>",
            "owneradd_reply_err": "<emoji id=5210952531676504517>❌</emoji> <b>Reply to a message required</b>",
            "owneradd_confirm": "🛡 <b>Are you sure you want to grant access to <a href='tg://user?id={id}'>{name}</a>?</b> They will get access to all commands, this may have consequences. Decision is at your own risk!",
            "btn_confirm": "✅ Confirm",
            "btn_cancel": "❌ Cancel",
            "btn_send_confirm": "🛡 Send confirmation",
            "not_your_button": "❗ This button is not yours!",
            "access_granted": "✅ <b>Access granted for <a href='tg://user?id={id}'>{name}</a>!</b>",
            "access_denied": "❌ <b>Access denied for <a href='tg://user?id={id}'>{name}</a>!</b>"
        },
        "be": {
            "slang": "👇 Выберыце мову",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Няправільныя аргументы</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>Максімальная колькасць модуляў не можа быць меншай за 10 або большай за 100</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Цяпер будзе адлюстроўвацца максімум <code>{args}</code> модуляў на адной старонцы</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>На які прэфікс трэба змяніць?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Прэфікс быў зменены на</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Які аліяс трэба дадаць?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Няправільна ўказаны аргументы.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Прыклад:</b> <code>addalias</code> (новы аліяс) (каманда)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Такі аліяс ужо існуе</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Такой каманды няма</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>Аліяс</b> «<code>{alias}</code>» <b>для каманды</b> «<code>{cmd}</code>» <b>быў дададзены</b>",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>Які аліяс трэба выдаліць?</b>",
            "alias_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Такога аліясу няма</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>Аліяс</b> «<code>{alias}</code>» <b>быў выдалены</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Аліясы адсутнічаюць</b>",
            "aliases_list": "<emoji id=5956561916573782596>📄</emoji> <b>Спіс усіх аліясаў:</b>\n",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Які модуль трэба схаваць?</b>",
            "mod_already_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>ужо схаваны</b>\n\n{text}",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>схаваны</b>\n\n{text}",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Які модуль трэба паказаць?</b>",
            "mod_not_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>не схаваны</b>\n\n{text}",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>цяпер бачны</b>\n\n{text}",
            "no_hidden_mods": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Схаваных модуляў няма</b>",
            "hidden_mods_list": "<emoji id=5956561916573782596>📄</emoji> <b>Спіс схаваных модуляў:</b>\n",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Укажыце новы юзернэйм для бота.</b>",
            "setinline_err": "<emoji id=5210952531676504517>❌</emoji> <b>Няправільны юзернэйм. Ён павінен утрымліваць толькі літары, лічбы, падкрэсліванні, мець заканчэнне «Bot» і быць даўжынёй не менш за 5 сімвалаў.</b>",
            "bot_creating": "<emoji id=5195083327597456039>🌙</emoji> <b>Ствараю новага бота...</b>",
            "bot_father_err": "<emoji id=5210952531676504517>❌</emoji> <b>Не ўдалося стварыць новага бота. Адказ @BotFather:</b> <code>{res}</code>",
            "bot_setting_name": "<emoji id=5195083327597456039>🌙</emoji> <b>Наладжваю імя бота...</b>",
            "bot_setting_avatar": "<emoji id=5195083327597456039>🌙</emoji> <b>Наладжваю аватарку бота...</b>",
            "bot_setting_inline": "<emoji id=5195083327597456039>🌙</emoji> <b>Наладжваю інлайн...</b>",
            "bot_updating_user": "<emoji id=5195083327597456039>🌙</emoji> <b>Абнаўляю юзернэйм бота...</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Інлайн бот <code>@{name}</code> паспяхова створаны! Неабходна перазагрузка</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>Ніхто не мае доступу да вашага юзербота!</b>",
            "ownerlist_caption": "<emoji id=5251203410396458957>🛡</emoji> <b>Усяго <code>{count}</code> карыстальнікаў маюць доступ</b>\n\n",
            "owner_user": "Карыстальнік",
            "ownerrm_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Патрэбен адказ на паведамленне, ID або username!</b>",
            "owner_self_err": "<emoji id=5210952531676504517>❌</emoji> <b>Гэтую каманду немагчыма выканаць на сабе!</b>",
            "owner_no_access": "<emoji id=5210952531676504517>❌</emoji> <b>У карыстальніка няма доступу!</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Правы ў <a href='tg://user?id={id}'>{name}</a> адабраны!</b>",
            "owneradd_reply_err": "<emoji id=5210952531676504517>❌</emoji> <b>Патрэбен адказ на паведамленне</b>",
            "owneradd_confirm": "🛡 <b>Вы ўпэўнены, што хочаце даць доступ <a href='tg://user?id={id}'>{name}</a>?</b> Гэта можа мець наступствы.",
            "btn_confirm": "✅ Пацвердзіць",
            "btn_cancel": "❌ Адмена",
            "btn_send_confirm": "🛡 Адправіць пацверджанне",
            "not_your_button": "❗ Гэта кнопка не ваша!",
            "access_granted": "✅ <b>Доступ <a href='tg://user?id={id}'>{name}</a> дадзены!</b>",
            "access_denied": "❌ <b>Адмоўлена ў доступе для <a href='tg://user?id={id}'>{name}</a>!</b>"
        },
        "de": {
            "slang": "👇 Sprache wählen",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Ungültige Argumente</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>Max. Module dürfen nicht weniger als 10 oder mehr als 100 sein</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Jetzt werden maximal <code>{args}</code> Module pro Seite angezeigt</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Welchen Präfix soll ich setzen?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Präfix wurde geändert in</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Welchen Alias soll ich hinzufügen?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Ungültige Argumente.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Beispiel:</b> <code>addalias</code> (neuer Alias) (Befehl)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Dieser Alias existiert bereits</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Befehl nicht gefunden</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>für Befehl</b> «<code>{cmd}</code>» <b>hinzugefügt</b>",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>Welchen Alias soll ich löschen?</b>",
            "alias_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Alias nicht gefunden</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>gelöscht</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Keine Aliase gefunden</b>",
            "aliases_list": "<emoji id=5956561916573782596>📄</emoji> <b>Liste aller Aliase:</b>\n",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Welches Modul soll ausgeblendet werden?</b>",
            "mod_already_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Modul</b> «<code>{mod}</code>» <b>ist bereits ausgeblendet</b>\n\n{text}",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>Modul</b> «<code>{mod}</code>» <b>ist nun ausgeblendet</b>\n\n{text}",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Welches Modul soll angezeigt werden?</b>",
            "mod_not_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Modul</b> «<code>{mod}</code>» <b>ist nicht ausgeblendet</b>\n\n{text}",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>Modul</b> «<code>{mod}</code>» <b>ist nun sichtbar</b>\n\n{text}",
            "no_hidden_mods": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Keine ausgeblendeten Module</b>",
            "hidden_mods_list": "<emoji id=5956561916573782596>📄</emoji> <b>Ausgeblendete Module:</b>\n",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Geben Sie einen neuen Bot-Benutzernamen an.</b>",
            "setinline_err": "<emoji id=5210952531676504517>❌</emoji> <b>Ungültiger Benutzername. Muss auf «Bot» enden und min. 5 Zeichen lang sein.</b>",
            "bot_creating": "<emoji id=5195083327597456039>🌙</emoji> <b>Erstelle neuen Bot...</b>",
            "bot_father_err": "<emoji id=5210952531676504517>❌</emoji> <b>Fehler bei @BotFather:</b> <code>{res}</code>",
            "bot_setting_name": "<emoji id=5195083327597456039>🌙</emoji> <b>Setze Bot-Namen...</b>",
            "bot_setting_avatar": "<emoji id=5195083327597456039>🌙</emoji> <b>Setze Bot-Avatar...</b>",
            "bot_setting_inline": "<emoji id=5195083327597456039>🌙</emoji> <b>Aktiviere Inline-Modus...</b>",
            "bot_updating_user": "<emoji id=5195083327597456039>🌙</emoji> <b>Aktualisiere Bot-Benutzernamen...</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Bot <code>@{name}</code> erstellt! Neustart erforderlich.</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>Niemand hat Zugriff auf deinen Userbot!</b>",
            "ownerlist_caption": "<emoji id=5251203410396458957>🛡</emoji> <b>Insgesamt <code>{count}</code> Nutzer haben Zugriff</b>\n\n",
            "owner_user": "Nutzer",
            "ownerrm_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Antworte auf eine Nachricht oder gib ID/Benutzernamen an!</b>",
            "owner_self_err": "<emoji id=5210952531676504517>❌</emoji> <b>Du kannst dies nicht bei dir selbst tun!</b>",
            "owner_no_access": "<emoji id=5210952531676504517>❌</emoji> <b>Nutzer hat keinen Zugriff!</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Zugriff für <a href='tg://user?id={id}'>{name}</a> entzogen!</b>",
            "owneradd_reply_err": "<emoji id=5210952531676504517>❌</emoji> <b>Antwort auf eine Nachricht erforderlich</b>",
            "owneradd_confirm": "🛡 <b>Bist du sicher, dass du <a href='tg://user?id={id}'>{name}</a> Zugriff gewähren willst?</b>",
            "btn_confirm": "✅ Bestätigen",
            "btn_cancel": "❌ Abbrechen",
            "btn_send_confirm": "🛡 Bestätigung senden",
            "not_your_button": "❗ Das ist nicht deine Schaltfläche!",
            "access_granted": "✅ <b>Zugriff für <a href='tg://user?id={id}'>{name}</a> gewährt!</b>",
            "access_denied": "❌ <b>Zugriff für <a href='tg://user?id={id}'>{name}</a> verweigert!</b>"
        },
        "es": {
            "slang": "👇 Seleccionar idioma",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Argumentos inválidos</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>El máximo de módulos no puede ser menor a 10 ni mayor a 100</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Ahora se mostrarán hasta <code>{args}</code> módulos por página</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>¿Qué prefijo debo establecer?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>El prefijo ha sido cambiado a</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>¿Qué alias debo añadir?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Argumentos incorrectos.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Ejemplo:</b> <code>addalias</code> (nuevo alias) (comando)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Este alias ya existe</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Comando no encontrado</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>para el comando</b> «<code>{cmd}</code>» <b>añadido</b>",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>¿Qué alias debo eliminar?</b>",
            "alias_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Alias no encontrado</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>eliminado</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>No hay alias</b>",
            "aliases_list": "<emoji id=5956561916573782596>📄</emoji> <b>Lista de alias:</b>\n",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>¿Qué módulo quieres ocultar?</b>",
            "mod_already_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>El módulo</b> «<code>{mod}</code>» <b>ya está oculto</b>",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>Módulo</b> «<code>{mod}</code>» <b>oculto</b>",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>¿Qué módulo quieres mostrar?</b>",
            "mod_not_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>El módulo</b> «<code>{mod}</code>» <b>no está oculto</b>",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>El módulo</b> «<code>{mod}</code>» <b>ahora es visible</b>",
            "no_hidden_mods": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>No hay módulos ocultos</b>",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Indica el nuevo username para el bot.</b>",
            "setinline_err": "<emoji id=5210952531676504517>❌</emoji> <b>Username incorrecto. Debe terminar en «Bot» y tener al menos 5 caracteres.</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>¡Bot <code>@{name}</code> creado con éxito! Reinicia para aplicar cambios.</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>¡Nadie tiene acceso a tu userbot!</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b>¡Acceso revocado para <a href='tg://user?id={id}'>{name}</a>!</b>",
            "access_granted": "✅ <b>¡Acceso concedido a <a href='tg://user?id={id}'>{name}</a>!</b>"
        },
        "fr": {
            "slang": "👇 Choisir la langue",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Arguments invalides</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>Le max de modules doit être entre 10 et 100</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Désormais, <code>{args}</code> modules max seront affichés par page</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quel préfixe définir ?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Le préfixe a été changé en</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quel alias ajouter ?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Arguments incorrects.</b>",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Cet alias existe déjà</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Commande introuvable</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>ajouté pour</b> «<code>{cmd}</code>»",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>Quel alias supprimer ?</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>supprimé</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Aucun alias trouvé</b>",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quel module masquer ?</b>",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>Module</b> «<code>{mod}</code>» <b>masqué</b>",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quel module afficher ?</b>",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>Module</b> «<code>{mod}</code>» <b>est maintenant visible</b>",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Indiquez le nouveau username du bot.</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Bot <code>@{name}</code> créé ! Redémarrez pour appliquer.</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>Personne n'a accès à votre userbot !</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Accès révoqué pour <a href='tg://user?id={id}'>{name}</a> !</b>",
            "access_granted": "✅ <b>Accès accordé pour <a href='tg://user?id={id}'>{name}</a> !</b>"
        },
        "it": {
            "slang": "👇 Seleziona la lingua",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Argomenti non validi</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>Il numero massimo di moduli deve essere tra 10 e 100</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Ora verranno mostrati fino a <code>{args}</code> moduli per pagina</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quale prefisso vuoi impostare?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Il prefisso è stato cambiato in</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quale alias vuoi aggiungere?</b>",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Questo alias esiste già</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Comando non trovato</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>aggiunto per</b> «<code>{cmd}</code>»",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>eliminato</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Nessun alias trovato</b>",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quale modulo vuoi nascondere?</b>",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>Modulo</b> «<code>{mod}</code>» <b>nascosto</b>",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>Il modulo</b> «<code>{mod}</code>» <b>è ora visibile</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Bot <code>@{name}</code> creato! Riavvia per applicare le modifiche.</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Accesso revocato per <a href='tg://user?id={id}'>{name}</a>!</b>",
            "access_granted": "✅ <b>Accesso garantito per <a href='tg://user?id={id}'>{name}</a>!</b>"
        },
        "kk": {
            "slang": "👇 Тілді таңдаңыз",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Аргументтер қате енгізілді</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>Модульдер саны 10-нан аз және 100-ден көп болмауы керек</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Енді бір бетте ең көбі <code>{args}</code> модуль көрсетіледі</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Қай префиксті орнату керек?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Префикс</b> «{prefixes}» <b>болып өзгертілді</b>",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Қандай алиас қосу керек?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Аргументтер қате.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Мысалы:</b> <code>addalias</code> (жаңа алиас) (команда)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Мұндай алиас бұрыннан бар</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Мұндай команда табылмады</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> «<code>{alias}</code>» <b>алиасы</b> «<code>{cmd}</code>» <b>командасы үшін қосылды</b>",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>Қай алиасты өшіру керек?</b>",
            "alias_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Мұндай алиас табылмады</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> «<code>{alias}</code>» <b>алиасы өшірілді</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Алиастар жоқ</b>",
            "aliases_list": "<emoji id=5956561916573782596>📄</emoji> <b>Барлық алиастар тізімі:</b>\n",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Қай модульді жасыру керек?</b>",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> «<code>{mod}</code>» <b>модулі жасырылды</b>",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Қай модульді көрсету керек?</b>",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> «<code>{mod}</code>» <b>модулі енді көрінеді</b>",
            "no_hidden_mods": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Жасырын модульдер жоқ</b>",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Бот үшін жаңа юзернейм көрсетіңіз.</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Инлайн бот <code>@{name}</code> сәтті жасалды! Өзгерістерді қолдану үшін қайта жүктеу қажет</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>Юзерботыңызға ешкімнің рұқсаты жоқ!</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <a href='tg://user?id={id}'>{name}</a> <b>құқықтары сәтті алынды!</b>",
            "access_granted": "✅ <a href='tg://user?id={id}'>{name}</a> <b>үшін рұқсат берілді!</b>"
        },
        "uz": {
            "slang": "👇 Tilni tanlang",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Argumentlar noto'g'ri kiritildi</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>Modullar soni 10 dan kam va 100 dan ko'p bo'lishi mumkin emas</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Endi bir sahifada maksimal <code>{args}</code> modul ko'rsatiladi</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Qaysi prefiksga o'zgartirish kerak?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Prefiks</b> «{prefixes}» <b>ga o'zgartirildi</b>",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Qaysi aliasni qo'shish kerak?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Argumentlar xato.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Misol:</b> <code>addalias</code> (yangi alias) (buyruq)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Bunday alias allaqachon mavjud</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Bunday buyruq topilmadi</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> «<code>{alias}</code>» <b>aliasi</b> «<code>{cmd}</code>» <b>buyrug'i uchun qo'shildi</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> «<code>{alias}</code>» <b>aliasi o'chirildi</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Aliaslar mavjud emas</b>",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Qaysi modulni yashirish kerak?</b>",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> «<code>{mod}</code>» <b>moduli yashirildi</b>",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> «<code>{mod}</code>» <b>moduli endi ko'rinadi</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Inline bot <code>@{name}</code> muvaffaqiyatli yaratildi!</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>Userbotingizga hech kimning ruxsati yo'q!</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <a href='tg://user?id={id}'>{name}</a> <b>dan huquqlar olib qo'yildi!</b>",
            "access_granted": "✅ <a href='tg://user?id={id}'>{name}</a> <b>uchun ruxsat berildi!</b>"
        }
    }


    def __init__(self):
        self.db = db

    def _kb(self, user_id):
        b1 = InlineKeyboardButton(text=self.S("btn_confirm"), callback_data=f"giveaccess_{user_id}")
        b2 = InlineKeyboardButton(text=self.S("btn_cancel"), callback_data=f"cancel_{user_id}")
        kb_builder = InlineKeyboardBuilder()
        kb_builder.row(b1, b2)
        return kb_builder.as_markup()
    
    async def setlang_cmd(self, app: Client, message: types.Message):
    	"""Изменить язык"""
    	await utils.inline(self, message, "setlang")

    async def setmaxhelpmods_cmd(self, app: Client, message: types.Message, args: str):
        """Указать максимальное кол-во отображаемых модулей на одной странице помощи"""
        if not args:
            return await utils.answer(message, self.S("maxhelp_err_args"))
        
        try:
            val = int(args)
            if val <= 9 or val >= 101:
                return await utils.answer(message, self.S("maxhelp_err_range"))
            
            self.db.set("xioca.help", "maxmods", val)
            await utils.answer(message, self.S("maxhelp_success", args=args))
        except ValueError:
            await utils.answer(message, self.S("maxhelp_err_args"))

    async def setprefix_cmd(self, app: Client, message: types.Message, args: str):
        """Изменить префикс"""
        if not (args_list := args.split()):
            return await utils.answer(message, self.S("prefix_ask"))

        self.db.set("xioca.loader", "prefixes", list(set(args_list)))
        prefixes = ", ".join(f"<code>{prefix}</code>" for prefix in args_list)
        return await utils.answer(message, self.S("prefix_success", prefixes=prefixes))

    async def addalias_cmd(self, app: Client, message: types.Message, args: str):
        """Добавить алиас"""
        if not (args_split := args.lower().split(maxsplit=1)):
            return await utils.answer(message, self.S("alias_ask"))

        if len(args_split) != 2:
            return await utils.answer(message, self.S("alias_err_args"))

        aliases = self.all_modules.aliases
        if args_split[0] in aliases:
            return await utils.answer(message, self.S("alias_exists"))

        if not self.all_modules.command_handlers.get(args_split[1]):
            return await utils.answer(message, self.S("cmd_not_found"))

        aliases[args_split[0]] = args_split[1]
        self.db.set("xioca.loader", "aliases", aliases)
        return await utils.answer(message, self.S("alias_added", alias=args_split[0], cmd=args_split[1]))

    async def delalias_cmd(self, app: Client, message: types.Message, args: str):
        """Удалить алиас"""
        if not (alias_to_del := args.lower()):
            return await utils.answer(message, self.S("alias_del_ask"))

        aliases = self.all_modules.aliases
        if alias_to_del not in aliases:
            return await utils.answer(message, self.S("alias_not_found"))

        del aliases[alias_to_del]
        self.db.set("xioca.loader", "aliases", aliases)
        return await utils.answer(message, self.S("alias_deleted", alias=alias_to_del))

    async def aliases_cmd(self, app: Client, message: types.Message):
        """Показать все алиасы"""
        aliases = self.all_modules.aliases
        if not aliases:
            return await utils.answer(message, self.S("no_aliases"))

        text = self.S("aliases_list") + "\n".join(
            f"<emoji id=4972281662894244560>🛑</emoji> <code>{alias}</code> ➜ <code>{command}</code>"
            for alias, command in aliases.items()
        )
        return await utils.answer(message, text)

    async def hidemod_cmd(self, app: Client, message: types.Message, args: str):
        """Скрыть модуль"""
        if not args:
            return await utils.answer(message, self.S("hidemod_ask"))

        module_name = args.lower()
        hide_mods = self.db.get("help", "hide_mods", [])
        all_modules = [module.name.lower() for module in self.all_modules.modules]
        module_name, find_text = utils.find_closest_module_name(module_name, all_modules)
        
        if module_name in hide_mods:
            return await utils.answer(message, self.S("mod_already_hidden", mod=module_name, text=find_text))

        hide_mods.append(module_name)
        self.db.set("help", "hide_mods", hide_mods)
        return await utils.answer(message, self.S("mod_hidden", mod=module_name, text=find_text))

    async def showmod_cmd(self, app: Client, message: types.Message, args: str):
        """Показать скрытый модуль"""
        if not args:
            return await utils.answer(message, self.S("showmod_ask"))

        module_name = args.lower()
        hide_mods = self.db.get("help", "hide_mods", [])
        all_modules = [module.name.lower() for module in self.all_modules.modules]
        module_name, find_text = utils.find_closest_module_name(module_name, all_modules)
        
        if module_name not in hide_mods:
            return await utils.answer(message, self.S("mod_not_hidden", mod=module_name, text=find_text))

        hide_mods.remove(module_name)
        self.db.set("help", "hide_mods", hide_mods)
        return await utils.answer(message, self.S("mod_shown", mod=module_name, text=find_text))

    async def hiddenmods_cmd(self, app: Client, message: types.Message):
        """Показать список скрытых модулей"""
        hide_mods = self.db.get("help", "hide_mods", [])
        if not hide_mods:
            return await utils.answer(message, self.S("no_hidden_mods"))

        text = self.S("hidden_mods_list") + "\n".join(
            f"<emoji id=4972281662894244560>🛑</emoji> <code>{module}</code>"
            for module in hide_mods
        )
        return await utils.answer(message, text)

    async def setinline_cmd(self, app: Client, message: types.Message, args):
        """Сменить юзернейм инлайн бота"""
        if not args:
            return await utils.answer(message, self.S("setinline_ask"))
        name = args.strip().lower()
        if not re.match(r"^[a-zA-Z0-9_]{5,}bot$", name):
            return await utils.answer(message, self.S("setinline_err"))
        
        await utils.answer(message, self.S("bot_creating"))
        
        async with fsm.Conversation(app, "@BotFather", True) as conv:
            try:
                await conv.ask("/cancel")
            except Exception:
                await app.unblock_user("@BotFather")
            
            await conv.get_response()
            await asyncio.sleep(2)
            
            await conv.ask("/newbot")
            response = await conv.get_response()
            
            if not all(phrase not in response.text for phrase in ["That I cannot do.", "Sorry"]):
                return await utils.answer(message, self.S("bot_father_err", res=response.text))
            
            await utils.answer(message, self.S("bot_setting_name"))
            await conv.ask(f"Xioca of {utils.get_display_name(self.all_modules.me)[:45]}")
            await conv.get_response()
            
            await conv.ask(args)
            response = await conv.get_response()
            
            search = re.search(r"(?<=<code>)(.*?)(?=</code>)", response.text.html)
            if not search:
                return await utils.answer(message, self.S("bot_father_err", res=response.text))
            
            token = search.group(0)
            
            await utils.answer(message, self.S("bot_setting_avatar"))
            await conv.ask("/setuserpic")
            await conv.get_response()
            await conv.ask("@" + args)
            await conv.get_response()
            await conv.ask_media(random.choice(["bot_avatar1.png", "bot_avatar2.png", "bot_avatar3.png"]), media_type="photo")
            await conv.get_response()
            
            await utils.answer(message, self.S("bot_setting_inline"))
            await conv.ask("/setinline")
            await conv.get_response()
            
            await utils.answer(message, self.S("bot_updating_user"))
            await conv.ask("@" + args)
            await conv.get_response()
            await conv.ask("xioca  команда")
            await conv.get_response()
            
            self.db.set("xioca.bot", "token", token)
            await utils.answer(message, self.S("bot_success", name=name))

    async def ownerlist_cmd(self, app: Client, message: types.Message):
        """Список пользователей, имеющих доступ"""
        ids = self.db.get("xioca.loader", "allow", [])
        if not ids:
            return await utils.answer(message, self.S("ownerlist_empty"))
        
        make = str.maketrans({'1':'1️⃣','2':'2️⃣','3':'3️⃣','4':'4️⃣','5':'5️⃣','6':'6️⃣','7':'7️⃣','8':'8️⃣','9':'9️⃣','0':'0️⃣'})
        text = ""
        for i, uid in enumerate(ids, 1):
            try:
                user = await app.get_users(uid)
                name = user.first_name
            except:
                name = self.S("owner_user")
            text += f"{i} <a href='tg://user?id={uid}'>{name}</a>\n"
        
        await utils.answer(message, self.S("ownerlist_caption", count=len(ids)) + text.translate(make))

    async def ownerrm_cmd(self, app: Client, message: types.Message, args: str):
        """Отнять доступ"""
        r = message.reply_to_message
        if not r:
            if not args:
                return await utils.answer(message, self.S("ownerrm_err_args"))
            try:
                user = await app.get_users(args.split()[0].replace("@", ""))
                target_id, target_name = user.id, user.first_name
            except:
                return await utils.answer(message, self.S("ownerrm_err_args"))
        else:
            target_id, target_name = r.from_user.id, r.from_user.first_name
        
        if self.all_modules.me.id == target_id:
            return await utils.answer(message, self.S("owner_self_err"))
        
        ids = self.db.get("xioca.loader", "allow", [])
        if target_id not in ids:
            return await utils.answer(message, self.S("owner_no_access"))
        
        ids.remove(target_id)
        self.db.set("xioca.loader", "allow", ids)
        await utils.answer(message, self.S("owner_rm_success", id=target_id, name=target_name))

    async def owneradd_cmd(self, app: Client, message: types.Message):
        """Предоставить доступ"""
        r = message.reply_to_message
        if not r:
            return await utils.answer(message, self.S("owneradd_reply_err"))
        
        if self.all_modules.me.id == r.from_user.id:
            return await utils.answer(message, self.S("owner_self_err"))
        
        await utils.inline(self, message, f"owneradd {r.from_user.id}")
    
    @loader.on_bot(lambda self, app, inline_query: True)
    async def owneradd_inline_handler(self, app: Client, inline_query: InlineQuery):
        """Инлайн подтверждение"""
        args = inline_query.query.split()
        if len(args) < 2 or args[0] != "owneradd":
            return
        
        uid = int(args[1])
        user = await app.get_users(uid)
        text = self.S("owneradd_confirm", id=uid, name=user.first_name)
        await utils.answer_inline(inline_query, text, self.S("btn_send_confirm"), self._kb(uid))
        
    @loader.on_bot(lambda self, app, call: call.data.startswith("giveaccess_"))
    async def giveaccess_callback_handler(self, app: Client, call: CallbackQuery):
        """Подтверждение доступа"""
        uid = int(call.data.split("_")[1])
        if call.from_user.id != self.all_modules.me.id:
            return await call.answer(self.S("not_your_button"), True)

        ids = self.db.get("xioca.loader", "allow", [])
        if uid not in ids:
            ids.append(uid)
            self.db.set("xioca.loader", "allow", ids)
        
        user = await app.get_users(uid)
        await self.bot.edit_message_text(
            inline_message_id=call.inline_message_id, 
            text=self.S("access_granted", id=uid, name=user.first_name)
        )
    
    @loader.on_bot(lambda self, app, call: call.data.startswith("cancel_"))
    async def cancel_callback_handler(self, app: Client, call: CallbackQuery):
        """Отказ в доступе"""
        uid = int(call.data.split("_")[1])
        if call.from_user.id != self.all_modules.me.id:
            return await call.answer(self.S("not_your_button"), True)
            
        user = await app.get_users(uid)
        await self.bot.edit_message_text(
            inline_message_id=call.inline_message_id, 
            text=self.S("access_denied", id=uid, name=user.first_name)
        )

    @loader.inline("setlang")
    async def setlang_inline_handler(self, app: Client, inline_query: InlineQuery):
    	await utils.answer_inline(inline_query, self.S("slang"), "Set language", slang_kb())
    
    @loader.callback("selectlang")
    async def selectlang(self, app, callback):
    	cd = callback.data.split("_")
    	cdata = cd[0]
    	lang = cd[1]
    	
    	if self.all_modules.me.id != callback.from_user.id:
    		return await callback.answer(self.S("not_your_btn"))
		
    	self.db.set("xioca.loader", "select_lang", True)
    	self.db.set("xioca.loader", "language", lang)
		
    	await callback.answer("✅")
		
    	try:
    	    await self.bot.edit_message_text(inline_message_id=callback.inline_message_id, text=self.S("slang"), reply_markup=slang_kb())
    	except Exception as e:
     		logging.error(e)