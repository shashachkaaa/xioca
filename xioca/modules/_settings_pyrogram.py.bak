# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import asyncio
import logging
import re

from aiogram.types import (
    InlineQuery,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from pyrogram import Client, types
from .. import loader, utils, fsm


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
    kb.row(de, es, fr)
    kb.row(it, kk, uz)

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
            "slang": "👇 Select a language",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Invalid arguments</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>The maximum number of modules cannot be less than 10 or greater than 100</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Now up to <code>{args}</code> modules will be shown per help page</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>What prefixes do you want to set?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Prefix changed to</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Which alias do you want to add?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Invalid arguments.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Example:</b> <code>addalias</code> (new alias) (command)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>This alias already exists</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Command not found</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>for command</b> «<code>{cmd}</code>» <b>has been added</b>",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>Which alias do you want to remove?</b>",
            "alias_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Alias not found</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>has been removed</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>No aliases</b>",
            "aliases_list": "<emoji id=5956561916573782596>📄</emoji> <b>All aliases:</b>\n",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Which module do you want to hide?</b>",
            "mod_already_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Module</b> «<code>{mod}</code>» <b>is already hidden</b>\n\n{text}",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>Module</b> «<code>{mod}</code>» <b>is now hidden</b>\n\n{text}",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Which module do you want to show?</b>",
            "mod_not_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Module</b> «<code>{mod}</code>» <b>is not hidden</b>\n\n{text}",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>Module</b> «<code>{mod}</code>» <b>is now visible</b>\n\n{text}",
            "no_hidden_mods": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>No hidden modules</b>",
            "hidden_mods_list": "<emoji id=5956561916573782596>📄</emoji> <b>Hidden modules:</b>\n",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Enter a new username for the bot.</b>",
            "setinline_err": "<emoji id=5210952531676504517>❌</emoji> <b>Invalid username. It must contain only letters, digits and underscores, end with “Bot”, and be at least 5 characters long.</b>",
            "bot_creating": "<emoji id=5195083327597456039>🌙</emoji> <b>Creating a new bot...</b>",
            "bot_father_err": "<emoji id=5210952531676504517>❌</emoji> <b>Failed to create a new bot. @BotFather reply:</b> <code>{res}</code>",
            "bot_setting_name": "<emoji id=5195083327597456039>🌙</emoji> <b>Setting bot name...</b>",
            "bot_setting_avatar": "<emoji id=5195083327597456039>🌙</emoji> <b>Setting bot avatar...</b>",
            "bot_setting_inline": "<emoji id=5195083327597456039>🌙</emoji> <b>Setting inline mode...</b>",
            "bot_updating_user": "<emoji id=5195083327597456039>🌙</emoji> <b>Updating bot username...</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Inline bot <code>@{name}</code> created successfully! Restart is required to apply changes</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>No one has access to your userbot!</b>",
            "ownerlist_caption": "<emoji id=5251203410396458957>🛡</emoji> <b>Total <code>{count}</code> users have access to your userbot</b>\n\n",
            "owner_user": "User",
            "ownerrm_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Reply to a message, or provide user ID/username!</b>",
            "owner_self_err": "<emoji id=5210952531676504517>❌</emoji> <b>You can’t use this command on yourself!</b>",
            "owner_no_access": "<emoji id=5210952531676504517>❌</emoji> <b>This user has no access to the userbot!</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Access for <a href='tg://user?id={id}'>{name}</a> has been revoked!</b>",
            "owneradd_reply_err": "<emoji id=5210952531676504517>❌</emoji> <b>Reply to a message is required</b>",
            "owneradd_confirm": "🛡 <b>Are you sure you want to grant access to <a href='tg://user?id={id}'>{name}</a>?</b> They will get access to all commands of your Xioca, which may have bad consequences. Proceed at your own risk!",
            "btn_confirm": "✅ Confirm",
            "btn_cancel": "❌ Cancel",
            "btn_send_confirm": "🛡 Send confirmation",
            "not_your_button": "❗ This button is not yours!",
            "access_granted": "✅ <b>Access granted to <a href='tg://user?id={id}'>{name}</a>!</b>",
            "access_denied": "❌ <b>Access denied for <a href='tg://user?id={id}'>{name}</a>!</b>"
        },

        "be": {
            "slang": "👇 Абярыце мову",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Няправільныя аргументы</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>Максімальная колькасць модуляў не можа быць менш за 10 і больш за 100</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Цяпер будзе паказвацца максімум <code>{args}</code> модуляў на адной старонцы даведкі</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>На якія прэфіксы змяніць?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Прэфіксы зменены на</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Які аліяс дадаць?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Няправільныя аргументы.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Прыклад:</b> <code>addalias</code> (новы аліяс) (каманда)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Такі аліяс ужо існуе</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Такой каманды няма</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>Аліяс</b> «<code>{alias}</code>» <b>для каманды</b> «<code>{cmd}</code>» <b>дададзены</b>",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>Які аліяс выдаліць?</b>",
            "alias_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Такога аліяса няма</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>Аліяс</b> «<code>{alias}</code>» <b>выдалены</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Аліясаў няма</b>",
            "aliases_list": "<emoji id=5956561916573782596>📄</emoji> <b>Спіс усіх аліясоў:</b>\n",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Які модуль трэба схаваць?</b>",
            "mod_already_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>ужо схаваны</b>\n\n{text}",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>схаваны</b>\n\n{text}",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Які модуль трэба паказаць?</b>",
            "mod_not_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>не схаваны</b>\n\n{text}",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>цяпер бачны</b>\n\n{text}",
            "no_hidden_mods": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Схаваных модуляў няма</b>",
            "hidden_mods_list": "<emoji id=5956561916573782596>📄</emoji> <b>Спіс схаваных модуляў:</b>\n",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Укажыце новы юзернейм для бота.</b>",
            "setinline_err": "<emoji id=5210952531676504517>❌</emoji> <b>Некарэктны юзернейм. Ён павінен утрымліваць толькі літары, лічбы і падкрэсліванні, заканчвацца на «Bot» і мець даўжыню не менш за 5 сімвалаў.</b>",
            "bot_creating": "<emoji id=5195083327597456039>🌙</emoji> <b>Ствараю новага бота...</b>",
            "bot_father_err": "<emoji id=5210952531676504517>❌</emoji> <b>Не атрымалася стварыць новага бота. Адказ @BotFather:</b> <code>{res}</code>",
            "bot_setting_name": "<emoji id=5195083327597456039>🌙</emoji> <b>Наладжваю імя бота...</b>",
            "bot_setting_avatar": "<emoji id=5195083327597456039>🌙</emoji> <b>Наладжваю аватарку бота...</b>",
            "bot_setting_inline": "<emoji id=5195083327597456039>🌙</emoji> <b>Наладжваю інлайн...</b>",
            "bot_updating_user": "<emoji id=5195083327597456039>🌙</emoji> <b>Абнаўляю юзернейм бота...</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Інлайн-бот <code>@{name}</code> паспяхова створаны! Патрэбна перазагрузка для прымянення змен</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>Ніхто не мае доступу да вашага юзербота!</b>",
            "ownerlist_caption": "<emoji id=5251203410396458957>🛡</emoji> <b>Усяго <code>{count}</code> карыстальнікаў маюць доступ да вашага юзербота</b>\n\n",
            "owner_user": "Карыстальнік",
            "ownerrm_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Патрэбны адказ на паведамленне, ID ці username карыстальніка!</b>",
            "owner_self_err": "<emoji id=5210952531676504517>❌</emoji> <b>Немагчыма выканаць гэтую каманду на самім сабе!</b>",
            "owner_no_access": "<emoji id=5210952531676504517>❌</emoji> <b>Карыстальнік не мае доступу да юзербота!</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Доступ у <a href='tg://user?id={id}'>{name}</a> паспяхова адкліканы!</b>",
            "owneradd_reply_err": "<emoji id=5210952531676504517>❌</emoji> <b>Патрэбны адказ на паведамленне</b>",
            "owneradd_confirm": "🛡 <b>Вы ўпэўнены, што хочаце даць доступ да юзербота <a href='tg://user?id={id}'>{name}</a>?</b> Ён(яна) атрымае доступ да ўсіх каманд вашай Xioca, гэта можа мець дрэнныя наступствы. Рашэнне прымаецца на ваш страх і рызыку!",
            "btn_confirm": "✅ Пацвердзіць",
            "btn_cancel": "❌ Адмена",
            "btn_send_confirm": "🛡 Адправіць пацверджанне",
            "not_your_button": "❗ Гэта кнопка не ваша!",
            "access_granted": "✅ <b>Доступ для <a href='tg://user?id={id}'>{name}</a> прадастаўлены!</b>",
            "access_denied": "❌ <b>Адмоўлена ў доступе для <a href='tg://user?id={id}'>{name}</a>!</b>"
        },

        "de": {
            "slang": "👇 Sprache auswählen",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Ungültige Argumente</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>Die maximale Anzahl der Module darf nicht kleiner als 10 und nicht größer als 100 sein</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Jetzt werden maximal <code>{args}</code> Module pro Hilfeseite angezeigt</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Auf welche Präfixe soll geändert werden?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Präfix geändert zu</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Welchen Alias möchtest du hinzufügen?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Ungültige Argumente.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Beispiel:</b> <code>addalias</code> (neuer Alias) (Befehl)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Dieser Alias existiert bereits</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Befehl nicht gefunden</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>für den Befehl</b> «<code>{cmd}</code>» <b>wurde hinzugefügt</b>",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>Welchen Alias möchtest du entfernen?</b>",
            "alias_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Alias nicht gefunden</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>wurde entfernt</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Keine Aliasse</b>",
            "aliases_list": "<emoji id=5956561916573782596>📄</emoji> <b>Alle Aliasse:</b>\n",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Welches Modul soll ausgeblendet werden?</b>",
            "mod_already_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Modul</b> «<code>{mod}</code>» <b>ist bereits ausgeblendet</b>\n\n{text}",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>Modul</b> «<code>{mod}</code>» <b>wurde ausgeblendet</b>\n\n{text}",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Welches Modul soll angezeigt werden?</b>",
            "mod_not_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Modul</b> «<code>{mod}</code>» <b>ist nicht ausgeblendet</b>\n\n{text}",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>Modul</b> «<code>{mod}</code>» <b>ist jetzt sichtbar</b>\n\n{text}",
            "no_hidden_mods": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Keine ausgeblendeten Module</b>",
            "hidden_mods_list": "<emoji id=5956561916573782596>📄</emoji> <b>Ausgeblendete Module:</b>\n",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Gib einen neuen Benutzernamen für den Bot ein.</b>",
            "setinline_err": "<emoji id=5210952531676504517>❌</emoji> <b>Ungültiger Benutzername. Er darf nur Buchstaben, Zahlen und Unterstriche enthalten, muss mit „Bot“ enden und mindestens 5 Zeichen lang sein.</b>",
            "bot_creating": "<emoji id=5195083327597456039>🌙</emoji> <b>Erstelle einen neuen Bot...</b>",
            "bot_father_err": "<emoji id=5210952531676504517>❌</emoji> <b>Neuer Bot konnte nicht erstellt werden. Antwort von @BotFather:</b> <code>{res}</code>",
            "bot_setting_name": "<emoji id=5195083327597456039>🌙</emoji> <b>Richte den Bot-Namen ein...</b>",
            "bot_setting_avatar": "<emoji id=5195083327597456039>🌙</emoji> <b>Richte das Bot-Avatar ein...</b>",
            "bot_setting_inline": "<emoji id=5195083327597456039>🌙</emoji> <b>Richte Inline-Modus ein...</b>",
            "bot_updating_user": "<emoji id=5195083327597456039>🌙</emoji> <b>Aktualisiere Bot-Benutzername...</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Inline-Bot <code>@{name}</code> erfolgreich erstellt! Neustart erforderlich, um Änderungen anzuwenden</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>Niemand hat Zugriff auf deinen Userbot!</b>",
            "ownerlist_caption": "<emoji id=5251203410396458957>🛡</emoji> <b>Insgesamt haben <code>{count}</code> Nutzer Zugriff auf deinen Userbot</b>\n\n",
            "owner_user": "Benutzer",
            "ownerrm_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Antwort auf eine Nachricht oder User-ID/Username erforderlich!</b>",
            "owner_self_err": "<emoji id=5210952531676504517>❌</emoji> <b>Du kannst diesen Befehl nicht auf dich selbst anwenden!</b>",
            "owner_no_access": "<emoji id=5210952531676504517>❌</emoji> <b>Dieser Nutzer hat keinen Zugriff auf den Userbot!</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Zugriff für <a href='tg://user?id={id}'>{name}</a> wurde entzogen!</b>",
            "owneradd_reply_err": "<emoji id=5210952531676504517>❌</emoji> <b>Antwort auf eine Nachricht erforderlich</b>",
            "owneradd_confirm": "🛡 <b>Bist du sicher, dass du <a href='tg://user?id={id}'>{name}</a> Zugriff geben möchtest?</b> Diese Person erhält Zugriff auf alle Befehle deiner Xioca. Das kann negative Folgen haben. Entscheidung auf eigenes Risiko!",
            "btn_confirm": "✅ Bestätigen",
            "btn_cancel": "❌ Abbrechen",
            "btn_send_confirm": "🛡 Bestätigung senden",
            "not_your_button": "❗ Dieser Button gehört nicht dir!",
            "access_granted": "✅ <b>Zugriff für <a href='tg://user?id={id}'>{name}</a> wurde gewährt!</b>",
            "access_denied": "❌ <b>Zugriff für <a href='tg://user?id={id}'>{name}</a> wurde verweigert!</b>"
        },

        "es": {
            "slang": "👇 Selecciona un idioma",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Argumentos inválidos</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>El número máximo de módulos no puede ser menor que 10 ni mayor que 100</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Ahora se mostrarán hasta <code>{args}</code> módulos por página de ayuda</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>¿A qué prefijos quieres cambiar?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Prefijo cambiado a</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>¿Qué alias quieres añadir?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Argumentos inválidos.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Ejemplo:</b> <code>addalias</code> (nuevo alias) (comando)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Este alias ya existe</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>No existe ese comando</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>El alias</b> «<code>{alias}</code>» <b>para el comando</b> «<code>{cmd}</code>» <b>ha sido añadido</b>",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>¿Qué alias quieres eliminar?</b>",
            "alias_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>No existe ese alias</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>El alias</b> «<code>{alias}</code>» <b>ha sido eliminado</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>No hay aliases</b>",
            "aliases_list": "<emoji id=5956561916573782596>📄</emoji> <b>Lista de aliases:</b>\n",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>¿Qué módulo quieres ocultar?</b>",
            "mod_already_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>El módulo</b> «<code>{mod}</code>» <b>ya está oculto</b>\n\n{text}",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>El módulo</b> «<code>{mod}</code>» <b>ha sido ocultado</b>\n\n{text}",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>¿Qué módulo quieres mostrar?</b>",
            "mod_not_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>El módulo</b> «<code>{mod}</code>» <b>no está oculto</b>\n\n{text}",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>El módulo</b> «<code>{mod}</code>» <b>ahora es visible</b>\n\n{text}",
            "no_hidden_mods": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>No hay módulos ocultos</b>",
            "hidden_mods_list": "<emoji id=5956561916573782596>📄</emoji> <b>Módulos ocultos:</b>\n",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Indica un nuevo nombre de usuario para el bot.</b>",
            "setinline_err": "<emoji id=5210952531676504517>❌</emoji> <b>Nombre de usuario inválido. Debe contener solo letras, números y guiones bajos, terminar en «Bot» y tener al menos 5 caracteres.</b>",
            "bot_creating": "<emoji id=5195083327597456039>🌙</emoji> <b>Creando un nuevo bot...</b>",
            "bot_father_err": "<emoji id=5210952531676504517>❌</emoji> <b>No se pudo crear un nuevo bot. Respuesta de @BotFather:</b> <code>{res}</code>",
            "bot_setting_name": "<emoji id=5195083327597456039>🌙</emoji> <b>Configurando el nombre del bot...</b>",
            "bot_setting_avatar": "<emoji id=5195083327597456039>🌙</emoji> <b>Configurando el avatar del bot...</b>",
            "bot_setting_inline": "<emoji id=5195083327597456039>🌙</emoji> <b>Configurando el modo inline...</b>",
            "bot_updating_user": "<emoji id=5195083327597456039>🌙</emoji> <b>Actualizando el nombre de usuario del bot...</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>¡Bot inline <code>@{name}</code> creado con éxito! Se requiere reiniciar para aplicar los cambios</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>¡Nadie tiene acceso a tu userbot!</b>",
            "ownerlist_caption": "<emoji id=5251203410396458957>🛡</emoji> <b>En total <code>{count}</code> usuarios tienen acceso a tu userbot</b>\n\n",
            "owner_user": "Usuario",
            "ownerrm_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>¡Se requiere responder a un mensaje o indicar ID/username!</b>",
            "owner_self_err": "<emoji id=5210952531676504517>❌</emoji> <b>¡No puedes usar este comando contigo mismo!</b>",
            "owner_no_access": "<emoji id=5210952531676504517>❌</emoji> <b>¡Este usuario no tiene acceso al userbot!</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b>¡El acceso de <a href='tg://user?id={id}'>{name}</a> ha sido revocado!</b>",
            "owneradd_reply_err": "<emoji id=5210952531676504517>❌</emoji> <b>Se requiere responder a un mensaje</b>",
            "owneradd_confirm": "🛡 <b>¿Seguro que quieres conceder acceso a <a href='tg://user?id={id}'>{name}</a>?</b> Obtendrá acceso a todos los comandos de tu Xioca, lo cual puede tener consecuencias. Procede bajo tu propio riesgo.",
            "btn_confirm": "✅ Confirmar",
            "btn_cancel": "❌ Cancelar",
            "btn_send_confirm": "🛡 Enviar confirmación",
            "not_your_button": "❗ ¡Este botón no es tuyo!",
            "access_granted": "✅ <b>¡Acceso concedido a <a href='tg://user?id={id}'>{name}</a>!</b>",
            "access_denied": "❌ <b>¡Acceso denegado para <a href='tg://user?id={id}'>{name}</a>!</b>"
        },

        "fr": {
            "slang": "👇 Choisissez une langue",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Arguments invalides</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>Le nombre maximal de modules ne peut pas être inférieur à 10 ni supérieur à 100</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Désormais, jusqu’à <code>{args}</code> modules seront affichés par page d’aide</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quels préfixes voulez-vous définir ?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Préfixe modifié en</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quel alias voulez-vous ajouter ?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Arguments invalides.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Exemple :</b> <code>addalias</code> (nouvel alias) (commande)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Cet alias existe déjà</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Commande introuvable</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>L’alias</b> «<code>{alias}</code>» <b>pour la commande</b> «<code>{cmd}</code>» <b>a été ajouté</b>",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>Quel alias voulez-vous supprimer ?</b>",
            "alias_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Alias introuvable</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>L’alias</b> «<code>{alias}</code>» <b>a été supprimé</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Aucun alias</b>",
            "aliases_list": "<emoji id=5956561916573782596>📄</emoji> <b>Liste des alias :</b>\n",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quel module voulez-vous masquer ?</b>",
            "mod_already_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Le module</b> «<code>{mod}</code>» <b>est déjà masqué</b>\n\n{text}",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>Le module</b> «<code>{mod}</code>» <b>a été masqué</b>\n\n{text}",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quel module voulez-vous afficher ?</b>",
            "mod_not_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Le module</b> «<code>{mod}</code>» <b>n’est pas masqué</b>\n\n{text}",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>Le module</b> «<code>{mod}</code>» <b>est maintenant visible</b>\n\n{text}",
            "no_hidden_mods": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Aucun module masqué</b>",
            "hidden_mods_list": "<emoji id=5956561916573782596>📄</emoji> <b>Modules masqués :</b>\n",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Indiquez un nouveau nom d’utilisateur pour le bot.</b>",
            "setinline_err": "<emoji id=5210952531676504517>❌</emoji> <b>Nom d’utilisateur invalide. Il doit contenir uniquement des lettres, chiffres et underscores, se terminer par «Bot» et avoir au moins 5 caractères.</b>",
            "bot_creating": "<emoji id=5195083327597456039>🌙</emoji> <b>Création d’un nouveau bot...</b>",
            "bot_father_err": "<emoji id=5210952531676504517>❌</emoji> <b>Impossible de créer un nouveau bot. Réponse de @BotFather :</b> <code>{res}</code>",
            "bot_setting_name": "<emoji id=5195083327597456039>🌙</emoji> <b>Configuration du nom du bot...</b>",
            "bot_setting_avatar": "<emoji id=5195083327597456039>🌙</emoji> <b>Configuration de l’avatar du bot...</b>",
            "bot_setting_inline": "<emoji id=5195083327597456039>🌙</emoji> <b>Configuration du mode inline...</b>",
            "bot_updating_user": "<emoji id=5195083327597456039>🌙</emoji> <b>Mise à jour du nom d’utilisateur du bot...</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Bot inline <code>@{name}</code> créé avec succès ! Un redémarrage est requis pour appliquer les changements</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>Personne n’a accès à votre userbot !</b>",
            "ownerlist_caption": "<emoji id=5251203410396458957>🛡</emoji> <b>Au total, <code>{count}</code> utilisateurs ont accès à votre userbot</b>\n\n",
            "owner_user": "Utilisateur",
            "ownerrm_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Répondez à un message ou indiquez l’ID/username de l’utilisateur !</b>",
            "owner_self_err": "<emoji id=5210952531676504517>❌</emoji> <b>Impossible d’utiliser cette commande sur vous-même !</b>",
            "owner_no_access": "<emoji id=5210952531676504517>❌</emoji> <b>Cet utilisateur n’a pas accès au userbot !</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b>L’accès de <a href='tg://user?id={id}'>{name}</a> a été révoqué !</b>",
            "owneradd_reply_err": "<emoji id=5210952531676504517>❌</emoji> <b>Une réponse à un message est requise</b>",
            "owneradd_confirm": "🛡 <b>Voulez-vous vraiment accorder l’accès à <a href='tg://user?id={id}'>{name}</a> ?</b> Cette personne aura accès à toutes les commandes de votre Xioca, ce qui peut avoir de mauvaises conséquences. À vos risques et périls !",
            "btn_confirm": "✅ Confirmer",
            "btn_cancel": "❌ Annuler",
            "btn_send_confirm": "🛡 Envoyer la confirmation",
            "not_your_button": "❗ Ce bouton n’est pas le vôtre !",
            "access_granted": "✅ <b>Accès accordé à <a href='tg://user?id={id}'>{name}</a> !</b>",
            "access_denied": "❌ <b>Accès refusé pour <a href='tg://user?id={id}'>{name}</a> !</b>"
        },

        "it": {
            "slang": "👇 Seleziona una lingua",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Argomenti non validi</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>Il numero massimo di moduli non può essere inferiore a 10 o superiore a 100</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Ora verranno mostrati fino a <code>{args}</code> moduli per pagina di aiuto</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quali prefissi vuoi impostare?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Prefisso cambiato in</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quale alias vuoi aggiungere?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Argomenti non validi.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Esempio:</b> <code>addalias</code> (nuovo alias) (comando)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Questo alias esiste già</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Comando non trovato</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>per il comando</b> «<code>{cmd}</code>» <b>è stato aggiunto</b>",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>Quale alias vuoi rimuovere?</b>",
            "alias_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Alias non trovato</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>è stato rimosso</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Nessun alias</b>",
            "aliases_list": "<emoji id=5956561916573782596>📄</emoji> <b>Elenco alias:</b>\n",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quale modulo vuoi nascondere?</b>",
            "mod_already_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Il modulo</b> «<code>{mod}</code>» <b>è già nascosto</b>\n\n{text}",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>Il modulo</b> «<code>{mod}</code>» <b>è stato nascosto</b>\n\n{text}",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Quale modulo vuoi mostrare?</b>",
            "mod_not_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Il modulo</b> «<code>{mod}</code>» <b>non è nascosto</b>\n\n{text}",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>Il modulo</b> «<code>{mod}</code>» <b>ora è visibile</b>\n\n{text}",
            "no_hidden_mods": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Nessun modulo nascosto</b>",
            "hidden_mods_list": "<emoji id=5956561916573782596>📄</emoji> <b>Moduli nascosti:</b>\n",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Inserisci un nuovo username per il bot.</b>",
            "setinline_err": "<emoji id=5210952531676504517>❌</emoji> <b>Username non valido. Deve contenere solo lettere, numeri e underscore, terminare con “Bot” ed essere lungo almeno 5 caratteri.</b>",
            "bot_creating": "<emoji id=5195083327597456039>🌙</emoji> <b>Creazione di un nuovo bot...</b>",
            "bot_father_err": "<emoji id=5210952531676504517>❌</emoji> <b>Impossibile creare un nuovo bot. Risposta di @BotFather:</b> <code>{res}</code>",
            "bot_setting_name": "<emoji id=5195083327597456039>🌙</emoji> <b>Impostazione del nome del bot...</b>",
            "bot_setting_avatar": "<emoji id=5195083327597456039>🌙</emoji> <b>Impostazione dell’avatar del bot...</b>",
            "bot_setting_inline": "<emoji id=5195083327597456039>🌙</emoji> <b>Impostazione della modalità inline...</b>",
            "bot_updating_user": "<emoji id=5195083327597456039>🌙</emoji> <b>Aggiornamento dell’username del bot...</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Bot inline <code>@{name}</code> creato con successo! È necessario riavviare per applicare le modifiche</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>Nessuno ha accesso al tuo userbot!</b>",
            "ownerlist_caption": "<emoji id=5251203410396458957>🛡</emoji> <b>In totale <code>{count}</code> utenti hanno accesso al tuo userbot</b>\n\n",
            "owner_user": "Utente",
            "ownerrm_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Serve una risposta a un messaggio o l’ID/username dell’utente!</b>",
            "owner_self_err": "<emoji id=5210952531676504517>❌</emoji> <b>Non puoi usare questo comando su te stesso!</b>",
            "owner_no_access": "<emoji id=5210952531676504517>❌</emoji> <b>Questo utente non ha accesso al userbot!</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b>L’accesso di <a href='tg://user?id={id}'>{name}</a> è stato revocato!</b>",
            "owneradd_reply_err": "<emoji id=5210952531676504517>❌</emoji> <b>È richiesta una risposta a un messaggio</b>",
            "owneradd_confirm": "🛡 <b>Sei sicuro di voler concedere l’accesso a <a href='tg://user?id={id}'>{name}</a>?</b> Avrà accesso a tutti i comandi della tua Xioca, con possibili conseguenze. Procedi a tuo rischio!",
            "btn_confirm": "✅ Conferma",
            "btn_cancel": "❌ Annulla",
            "btn_send_confirm": "🛡 Invia conferma",
            "not_your_button": "❗ Questo pulsante non è tuo!",
            "access_granted": "✅ <b>Accesso concesso a <a href='tg://user?id={id}'>{name}</a>!</b>",
            "access_denied": "❌ <b>Accesso negato per <a href='tg://user?id={id}'>{name}</a>!</b>"
        },

        "kk": {
            "slang": "👇 Тілді таңдаңыз",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Аргументтер қате енгізілді</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>Көрсетілетін модульдер саны 10-нан аз және 100-ден көп болмауы керек</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Енді бір көмек бетінде ең көбі <code>{args}</code> модуль көрсетіледі</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Қандай префикстерге ауыстырамыз?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Префикс өзгертілді:</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Қандай алиас қосасыз?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Аргументтер қате.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Мысал:</b> <code>addalias</code> (жаңа алиас) (команда)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Мұндай алиас бар</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Мұндай команда жоқ</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>Алиас</b> «<code>{alias}</code>» <b>команда үшін</b> «<code>{cmd}</code>» <b>қосылды</b>",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>Қандай алиасты өшіресіз?</b>",
            "alias_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Мұндай алиас жоқ</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>Алиас</b> «<code>{alias}</code>» <b>өшірілді</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Алиастар жоқ</b>",
            "aliases_list": "<emoji id=5956561916573782596>📄</emoji> <b>Барлық алиастар тізімі:</b>\n",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Қай модульді жасырамыз?</b>",
            "mod_already_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>бұрыннан жасырылған</b>\n\n{text}",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>жасырылды</b>\n\n{text}",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Қай модульді көрсетеміз?</b>",
            "mod_not_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>жасырылмаған</b>\n\n{text}",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>енді көрінеді</b>\n\n{text}",
            "no_hidden_mods": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Жасырын модульдер жоқ</b>",
            "hidden_mods_list": "<emoji id=5956561916573782596>📄</emoji> <b>Жасырын модульдер тізімі:</b>\n",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Ботқа жаңа юзернейм енгізіңіз.</b>",
            "setinline_err": "<emoji id=5210952531676504517>❌</emoji> <b>Юзернейм қате. Тек әріптер, сандар және төменгі сызықша, соңында «Bot», ұзындығы кемінде 5 таңба болуы керек.</b>",
            "bot_creating": "<emoji id=5195083327597456039>🌙</emoji> <b>Жаңа бот жасалуда...</b>",
            "bot_father_err": "<emoji id=5210952531676504517>❌</emoji> <b>Жаңа бот жасау мүмкін болмады. @BotFather жауабы:</b> <code>{res}</code>",
            "bot_setting_name": "<emoji id=5195083327597456039>🌙</emoji> <b>Боттың атын орнатуда...</b>",
            "bot_setting_avatar": "<emoji id=5195083327597456039>🌙</emoji> <b>Аватар орнатуда...</b>",
            "bot_setting_inline": "<emoji id=5195083327597456039>🌙</emoji> <b>Inline-ды баптауда...</b>",
            "bot_updating_user": "<emoji id=5195083327597456039>🌙</emoji> <b>Бот юзернеймін жаңартуда...</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Inline бот <code>@{name}</code> сәтті жасалды! Өзгерістерді қолдану үшін қайта іске қосыңыз</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>Сіздің юзерботыңызға ешкімнің қолжетімділігі жоқ!</b>",
            "ownerlist_caption": "<emoji id=5251203410396458957>🛡</emoji> <b>Барлығы <code>{count}</code> пайдаланушыда қолжетімділік бар</b>\n\n",
            "owner_user": "Пайдаланушы",
            "ownerrm_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Хабарламаға жауап, ID немесе username қажет!</b>",
            "owner_self_err": "<emoji id=5210952531676504517>❌</emoji> <b>Бұл команданы өзіңізге қолдана алмайсыз!</b>",
            "owner_no_access": "<emoji id=5210952531676504517>❌</emoji> <b>Пайдаланушыда қолжетімділік жоқ!</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b><a href='tg://user?id={id}'>{name}</a> үшін қолжетімділік алынды!</b>",
            "owneradd_reply_err": "<emoji id=5210952531676504517>❌</emoji> <b>Хабарламаға жауап қажет</b>",
            "owneradd_confirm": "🛡 <b><a href='tg://user?id={id}'>{name}</a> пайдаланушысына қолжетімділік бергіңіз келе ме?</b> Ол сіздің Xioca-ңыздың барлық командаларына қол жеткізеді, бұл жағымсыз салдарға әкелуі мүмкін. Тәуекел өзіңізде!",
            "btn_confirm": "✅ Растау",
            "btn_cancel": "❌ Болдырмау",
            "btn_send_confirm": "🛡 Растауды жіберу",
            "not_your_button": "❗ Бұл батырма сіздікі емес!",
            "access_granted": "✅ <b><a href='tg://user?id={id}'>{name}</a> үшін қолжетімділік берілді!</b>",
            "access_denied": "❌ <b><a href='tg://user?id={id}'>{name}</a> үшін қолжетімділік берілмеді!</b>"
        },

        "uz": {
            "slang": "👇 Tilni tanlang",
            "maxhelp_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Noto‘g‘ri argumentlar</b>",
            "maxhelp_err_range": "<emoji id=5210952531676504517>❌</emoji> <b>Maksimal modullar soni 10 dan kam va 100 dan ko‘p bo‘lishi mumkin emas</b>",
            "maxhelp_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Endi yordam sahifasida maksimum <code>{args}</code> modul ko‘rsatiladi</b>",
            "prefix_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Qaysi prefikslarga o‘zgartiray?</b>",
            "prefix_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Prefiks o‘zgartirildi:</b> «{prefixes}»",
            "alias_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Qaysi aliasni qo‘shmoqchisiz?</b>",
            "alias_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Argumentlar noto‘g‘ri.</b>\n<emoji id=5206607081334906820>✔️</emoji> <b>Misol:</b> <code>addalias</code> (yangi alias) (komanda)",
            "alias_exists": "<emoji id=5210952531676504517>❌</emoji> <b>Bunday alias allaqachon bor</b>",
            "cmd_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Bunday komanda yo‘q</b>",
            "alias_added": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>komanda uchun</b> «<code>{cmd}</code>» <b>qo‘shildi</b>",
            "alias_del_ask": "<emoji id=5210952531676504517>❌</emoji> <b>Qaysi aliasni o‘chirmoqchisiz?</b>",
            "alias_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Bunday alias yo‘q</b>",
            "alias_deleted": "<emoji id=5206607081334906820>✔️</emoji> <b>Alias</b> «<code>{alias}</code>» <b>o‘chirildi</b>",
            "no_aliases": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Aliaslar yo‘q</b>",
            "aliases_list": "<emoji id=5956561916573782596>📄</emoji> <b>Aliaslar ro‘yxati:</b>\n",
            "hidemod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Qaysi modulni yashirmoqchisiz?</b>",
            "mod_already_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Modul</b> «<code>{mod}</code>» <b>allaqachon yashirilgan</b>\n\n{text}",
            "mod_hidden": "<emoji id=5206607081334906820>✔️</emoji> <b>Modul</b> «<code>{mod}</code>» <b>yashirildi</b>\n\n{text}",
            "showmod_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Qaysi modulni ko‘rsatmoqchisiz?</b>",
            "mod_not_hidden": "<emoji id=5210952531676504517>❌</emoji> <b>Modul</b> «<code>{mod}</code>» <b>yashirilmagan</b>\n\n{text}",
            "mod_shown": "<emoji id=5206607081334906820>✔️</emoji> <b>Modul</b> «<code>{mod}</code>» <b>endi ko‘rinadi</b>\n\n{text}",
            "no_hidden_mods": "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Yashirin modullar yo‘q</b>",
            "hidden_mods_list": "<emoji id=5956561916573782596>📄</emoji> <b>Yashirin modullar ro‘yxati:</b>\n",
            "setinline_ask": "<emoji id=5436113877181941026>❓</emoji> <b>Bot uchun yangi username kiriting.</b>",
            "setinline_err": "<emoji id=5210952531676504517>❌</emoji> <b>Username noto‘g‘ri. Faqat harflar, raqamlar va pastki chiziq bo‘lishi, «Bot» bilan tugashi va kamida 5 belgidan iborat bo‘lishi kerak.</b>",
            "bot_creating": "<emoji id=5195083327597456039>🌙</emoji> <b>Yangi bot yaratilmoqda...</b>",
            "bot_father_err": "<emoji id=5210952531676504517>❌</emoji> <b>Yangi bot yaratib bo‘lmadi. @BotFather javobi:</b> <code>{res}</code>",
            "bot_setting_name": "<emoji id=5195083327597456039>🌙</emoji> <b>Bot nomi sozlanmoqda...</b>",
            "bot_setting_avatar": "<emoji id=5195083327597456039>🌙</emoji> <b>Bot avatar sozlanmoqda...</b>",
            "bot_setting_inline": "<emoji id=5195083327597456039>🌙</emoji> <b>Inline sozlanmoqda...</b>",
            "bot_updating_user": "<emoji id=5195083327597456039>🌙</emoji> <b>Bot username yangilanmoqda...</b>",
            "bot_success": "<emoji id=5206607081334906820>✔️</emoji> <b>Inline bot <code>@{name}</code> muvaffaqiyatli yaratildi! O‘zgarishlarni qo‘llash uchun qayta ishga tushirish kerak</b>",
            "ownerlist_empty": "<emoji id=5210956306952758910>👀</emoji> <b>Sizning userbotingizga hech kimda kirish yo‘q!</b>",
            "ownerlist_caption": "<emoji id=5251203410396458957>🛡</emoji> <b>Jami <code>{count}</code> foydalanuvchida kirish bor</b>\n\n",
            "owner_user": "Foydalanuvchi",
            "ownerrm_err_args": "<emoji id=5210952531676504517>❌</emoji> <b>Xabarga javob, ID yoki username kerak!</b>",
            "owner_self_err": "<emoji id=5210952531676504517>❌</emoji> <b>Bu buyruqni o‘zingizga qo‘llab bo‘lmaydi!</b>",
            "owner_no_access": "<emoji id=5210952531676504517>❌</emoji> <b>Foydalanuvchida kirish yo‘q!</b>",
            "owner_rm_success": "<emoji id=5206607081334906820>✔️</emoji> <b><a href='tg://user?id={id}'>{name}</a> uchun kirish bekor qilindi!</b>",
            "owneradd_reply_err": "<emoji id=5210952531676504517>❌</emoji> <b>Xabarga javob kerak</b>",
            "owneradd_confirm": "🛡 <b><a href='tg://user?id={id}'>{name}</a> ga userbotga kirish berishni xohlaysizmi?</b> U sizning Xioca buyruqlaringizning barchasiga kirish oladi, bu yomon oqibatlarga olib kelishi mumkin. Qaror — o‘zingizning tavakkalingizda!",
            "btn_confirm": "✅ Tasdiqlash",
            "btn_cancel": "❌ Bekor qilish",
            "btn_send_confirm": "🛡 Tasdiq yuborish",
            "not_your_button": "❗ Bu tugma sizniki emas!",
            "access_granted": "✅ <b><a href='tg://user?id={id}'>{name}</a> ga kirish berildi!</b>",
            "access_denied": "❌ <b><a href='tg://user?id={id}'>{name}</a> ga kirish rad etildi!</b>"
        },
    }

    def __init__(self):
        cur_lang = self.db.get("xioca.loader", "language", "en")
        cur_prefixes = self.db.get("xioca.loader", "prefixes", ["."],)
        if isinstance(cur_prefixes, (list, tuple)):
            cur_prefixes_txt = " ".join(cur_prefixes) if cur_prefixes else "."
        else:
            cur_prefixes_txt = str(cur_prefixes) or "."

        def _sync_lang(old, new):
            self.db.set("xioca.loader", "select_lang", True)
            self.db.set("xioca.loader", "language", new)

        def _sync_prefixes(old, new):
            parts = [p.strip() for p in str(new).split() if p.strip()]
            if not parts:
                parts = ["."]
            self.db.set("xioca.loader", "prefixes", list(set(parts)))

        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "language",
                cur_lang,
                "Язык интерфейса (language)",
                validator=loader.validators.Choice("ru", "en", "be", "de", "es", "fr", "it", "kk", "uz"),
                on_change=_sync_lang,
            ),
            loader.ConfigValue(
                "prefixes",
                cur_prefixes_txt,
                "Префиксы команд (через пробел). Пример: . ! /",
                validator=loader.validators.String(min_len=1, max_len=64),
                on_change=_sync_prefixes,
            ),
        )

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
        except ValueError:
            return await utils.answer(message, self.S("maxhelp_err_args"))

        if val <= 9 or val >= 101:
            return await utils.answer(message, self.S("maxhelp_err_range"))

        help_module = self.all_modules.get_module("help")
        help_config = getattr(help_module, "config", None)

        if help_config is not None:
            help_config.set("max_help_modules", val)
        else:
            self.db.set("xioca.help", "maxmods", val)

        await utils.answer(message, self.S("maxhelp_success", args=args))

    async def setprefix_cmd(self, app: Client, message: types.Message, args: str):
        """Изменить префикс"""
        if not (args_list := args.split()):
            return await utils.answer(message, self.S("prefix_ask"))

        self.config.set("prefixes", " ".join(args_list))

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
            await conv.ask_media("bot_avatar.png", media_type="photo")
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

    @loader.inline("owneradd", True)
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
        lang = cd[1]

        if self.all_modules.me.id != callback.from_user.id:
            return await callback.answer(self.S("not_your_button"), True)

        try:
            self.config.set("language", lang)
        except Exception:
            self.db.set("xioca.loader", "select_lang", True)
            self.db.set("xioca.loader", "language", lang)

        await callback.answer("✅")

        try:
            await self.bot.edit_message_text(
                inline_message_id=callback.inline_message_id,
                text=self.S("slang"),
                reply_markup=slang_kb()
            )
        except Exception as e:
            logging.error(e)