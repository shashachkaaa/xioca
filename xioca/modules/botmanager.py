# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import logging
import html
import time
import atexit
import sys
import os
import re
import io
import requests
import traceback
import asyncio
from datetime import datetime
from packaging import version as ver

from aiogram.types import (
    InlineQuery,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
    BufferedInputFile,
    FSInputFile
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from meval import meval

from pyrogram import Client, types
from pyrogram.raw import functions, types
from .. import loader, utils, logger, __version__, __start_time__, __system_mod__, __get_version_url__, __get_commits_url__

def start_kb(S):
	b1 = InlineKeyboardButton(text=S("btn_control"), callback_data="userbot_control")
	b2 = InlineKeyboardButton(text=S("btn_settings"), callback_data="userbot_settings")
	b3 = InlineKeyboardButton(text=S("btn_info"), callback_data="userbot_info")
	
	kb = InlineKeyboardBuilder()
	kb.row(b1)
	kb.row(b2)
	kb.row(b3)
	return kb.as_markup()

def control(status, S):
	if status:
		b1 = InlineKeyboardButton(text=S("btn_stop"), callback_data="userbot_stop")
	else:
		b1 = InlineKeyboardButton(text=S("btn_start"), callback_data="userbot_start")
	
	b2 = InlineKeyboardButton(text=S("btn_restart"), callback_data="userbot_restart")
	b3 = InlineKeyboardButton(text=S("btn_check_update"), callback_data="userbot_checkupdate")
	b4 = InlineKeyboardButton(text=S("btn_logs"), callback_data="userbot_logs")
	back = InlineKeyboardButton(text=S("btn_back"), callback_data="userbot_back")
	
	kb = InlineKeyboardBuilder()
	kb.row(b1, b2)
	kb.row(b3)
	kb.row(b4)
	kb.row(back)
	return kb.as_markup()

def logs_kb(S):
	b1 = InlineKeyboardButton(text="📜 NOTSET", callback_data="userbot_logs_NOTSET")
	b2 = InlineKeyboardButton(text="🐛 DEBUG", callback_data="userbot_logs_DEBUG")
	b3 = InlineKeyboardButton(text="ℹ INFO", callback_data="userbot_logs_INFO")
	b4 = InlineKeyboardButton(text="⚠ WARNING", callback_data="userbot_logs_WARNING")
	b5 = InlineKeyboardButton(text="❌ ERROR", callback_data="userbot_logs_ERROR")
	b6 = InlineKeyboardButton(text="⛔ CRITICAL", callback_data="userbot_logs_CRITICAL")
	back = InlineKeyboardButton(text=S("btn_back"), callback_data="userbot_back")
	
	kb = InlineKeyboardBuilder()
	kb.row(b1, b2)
	kb.row(b3, b4)
	kb.row(b5, b6)
	kb.row(back)
	
	return kb.as_markup()

def settings(S):
	b1 = InlineKeyboardButton(text=S("btn_mod_manager"), callback_data="userbot_modulemanager")
	b2 = InlineKeyboardButton(text=S("btn_db_settings"), callback_data="userbot_dbsettings")
	back = InlineKeyboardButton(text=S("btn_back"), callback_data="userbot_back")
	
	kb = InlineKeyboardBuilder()
	kb.row(b1)
	kb.row(b2)
	kb.row(back)
	
	return kb.as_markup()

def dbsettings(S):
	b1 = InlineKeyboardButton(text=S("btn_sql_query"), callback_data="userbot_sqlquery")
	b2 = InlineKeyboardButton(text=S("btn_dl_db"), callback_data="userbot_getdb")
	back = InlineKeyboardButton(text=S("btn_back"), callback_data="userbot_back")
	
	kb = InlineKeyboardBuilder()
	kb.row(b1)
	kb.row(b2)
	kb.row(back)
	
	return kb.as_markup()

def back_kb(S):
	kb = InlineKeyboardBuilder()
	back = InlineKeyboardButton(text=S("btn_back"), callback_data="userbot_back")
	kb.row(back)
	
	return kb.as_markup()

def info_kb(S):
	b1 = InlineKeyboardButton(text=S("btn_support"), url="https://t.me/xiocasupport")
	b2 = InlineKeyboardButton(text=S("btn_mods_link"), url="https://xioca.ferz.live/mods")
	back = InlineKeyboardButton(text=S("btn_back"), callback_data="userbot_back")
	
	kb = InlineKeyboardBuilder()
	kb.row(b1, b2)
	kb.row(back)
	
	return kb.as_markup()

def slang_kb():
	kb = InlineKeyboardBuilder()
	
	ru = InlineKeyboardButton(text="🇷🇺 Русский", callback_data="select_lang_ru")
	en = InlineKeyboardButton(text="🇬🇧 English", callback_data="select_lang_en")
	be = InlineKeyboardButton(text="🇧🇾 Беларуская", callback_data="select_lang_be")
	de = InlineKeyboardButton(text="🇩🇪 Deutschland", callback_data="select_lang_de")
	es = InlineKeyboardButton(text="🇪🇸 Español", callback_data="select_lang_es")
	fr = InlineKeyboardButton(text="🇫🇷 Français", callback_data="select_lang_fr")
	it = InlineKeyboardButton(text="🇮🇹 Italiano", callback_data="select_lang_it")
	kk = InlineKeyboardButton(text="🇰🇿 Қазақ тілі", callback_data="select_lang_kk")
	uz = InlineKeyboardButton(text="🇺🇿 Oʻzbek tili", callback_data="select_lang_uz")
	
	kb.row(ru, en, be)
	kb.row(es, fr, it)
	kb.row(kk, uz)
	
	return kb.as_markup()

def modules_kb(self, page: int = 0, per_page: int = 25):
    all_modules = self.all_modules.modules
    
    system_modules = []
    user_modules = []
    
    for module in all_modules:
        if module.name.lower() in __system_mod__:
            system_modules.append(module)
        else:
            user_modules.append(module)
    
    sorted_modules = system_modules + user_modules
    total_pages = (len(sorted_modules) // per_page) + (1 if len(sorted_modules) % per_page else 0)
    
    start_idx = page * per_page
    end_idx = start_idx + per_page
    page_modules = sorted_modules[start_idx:end_idx]
    
    kb = InlineKeyboardBuilder()
    
    buttons = []
    for module in page_modules:
        buttons.append(
            InlineKeyboardButton(
                text=module.name,
                callback_data=f"userbot_module_{module.name.lower()}"
            )
        )
        
        if len(buttons) == 5:
            kb.row(*buttons)
            buttons = []
    
    if buttons:
        kb.row(*buttons)
    
    pagination_buttons = []
    
    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="⬅",
                callback_data=f"userbot_modulespage_{page - 1}"
            )
        )
    
    if page < total_pages - 1:
        pagination_buttons.append(
            InlineKeyboardButton(
                text="➡",
                callback_data=f"userbot_modulespage_{page + 1}"
            )
        )
    
    if pagination_buttons:
        kb.row(*pagination_buttons)
    
    back = InlineKeyboardButton(text=self.S("btn_back"), callback_data="userbot_back")
    kb.row(back)
    
    return kb.as_markup()

def module_settings_kb(S, name, actions: bool = True):
	b1 = InlineKeyboardButton(text=S("btn_delete"), callback_data=f"userbot_deletemodule_{name}")
	back = InlineKeyboardButton(text=S("btn_back"), callback_data="userbot_back")
	
	kb = InlineKeyboardBuilder()
	if actions:
		kb.row(b1)

	kb.row(back)

	return kb.as_markup()

@loader.module("shashachkaaa", __version__)
class BotManagerMod(loader.Module):
	"""Бот менеджер. Используется для системных команд бота."""

	strings = {
		"ru": {
			"slang": "🌎 Xioca поддерживает несколько языков, пожалуйста, выберите необходимый вам язык",
			"btn_control": "🎛 Управление юзерботом",
			"btn_settings": "⚙ Настройка юзербота",
			"btn_info": "ℹ Информация",
			"btn_stop": "🔴 Выключить юзербота",
			"btn_start": "🟢 Включить юзербота",
			"btn_restart": "🔄 Перезагрузить юзербота",
			"btn_check_update": "🆕 Проверить наличие обновлений",
			"btn_logs": "📤 Получить логи",
			"btn_back": "◀ Назад",
			"btn_mod_manager": "🌙 Модульный менеджер",
			"btn_db_settings": "🗂 База данных",
			"btn_sql_query": "⚙ Выполнить SQL запрос",
			"btn_dl_db": "📤 Скачать базу данных",
			"btn_support": "🆘 Поддержка",
			"btn_mods_link": "🗃 Модули",
			"btn_delete": "🗑 Удалить",
			"btn_update": "🔄 Установить обновление",
			"btn_yes": "✅ Да",
			"btn_no": "❌ Нет",
			"no_update_desc": "ℹ Нет описания обновления",
			"no_commits": "ℹ Нет данных о последних изменениях",
			"last_commit": "📌 <b>Последнее изменение <code>{sha}</code>:</b>",
			"update_desc_header": "📝 <b>Описание обновления:</b>",
			"changed_files": "📂 <b>Измененные файлы ({count}):</b>",
			"crit_update": "🚨 <b>КРИТИЧЕСКОЕ ОБНОВЛЕНИЕ!</b>\n",
			"new_version": "🔔 <b>Доступна новая версия!</b>",
			"version_info": "Текущая версия: <code>{curr}</code>\nНовая версия: <code>{new}</code>\n\n{changes}",
			"uptime_prefix": "⌚ <b>Прошло времени с момента запуска:</b> {uptime}\n",
			"status_on": "🟢 Юзербот активен",
			"status_off": "🔴 Юзербот выключен",
			"control_menu": "🎛 С помощью этого меню вы сможете <b>управлять юзерботом</b>.\n\n<b>{status}\n🌙 Установлено модулей:</b> {count}\n✏ <b>Префикс(ы):</b> ({prefix})\n{uptime}\n👇 <i>Жми любую кнопку ниже что бы выполнить какое либо действие с юзерботом.</i>",
			"install_success": "🌙 <b>Xioca успешно установлена и уже активна на вашем аккаунте!</b>\n\nℹ <b>Быстрый гайд по командам:</b>\n<code>.help</code> - Показать все доступные команды\n<code>.help</code> [команда / модуль] - Получить справку по конкретной команде.\n<code>.loadmod</code> [в ответ на файл] - Загрузить модуль из файла.\n<code>.unloadmod</code> [модуль] - Выгрузить модуль.\n<code>.ping</code> - Проверить, работает ли бот.\n<code>.restart</code> - Перезапустить бота.\n<code>.update</code> - Обновить бота.\n<code>.logs</code> - Получить логи бота.\n<code>.terminal</code> [команда] - Выполнить команду.",
			"folder_prompt": "💡 Создать папку с чатами поддержки/оффтопа, инлайн ботом и информационным каналом Xioca?",
			"manager_loaded": "Менеджер по командам бота загружен!",
			"not_your_btn": "Кнопка не ваша!",
			"folder_created": '✅ Папка "Xioca" успешно создана!',
			"sad_emoji": "😢",
			"start_text": "😎 Это - <code>Xioca</code>. Отличный юзербот с большим количеством команд и модулей к нему.\n\n❓ <b>Как установить?</b>\nДля <b>установки</b> воспользуйтесь <a href='https://xioca.ferz.live'>сайтом</a>.\n\n🌟 <b>Особенности:</b>\n- Удобное управление через команды.\n- Поддержка инлайн-режима.\n- Модульная архитектура для расширения функционала.\n- Регулярные обновления и поддержка.\n\n📚 <b>Документация:</b>\nПодробнее о возможностях и настройке можно узнать в <a href='https://github.com/shashachkaaa/Xioca'>документации</a>.\n\n🛠 <b>Поддержка:</b>\nЕсли у вас возникли вопросы, обратитесь в <a href='https://t.me/xiocasupport'>чат поддержки</a>.",
			"welcome_text": "👋 <b>Приветствую</b>, я - часть твоего юзербота <code>Xioca</code>, тут ты можешь найти настройки юзербота, информацию и прочее.\n\n👇 <i>Жми любую кнопку ниже что бы узнать подробности.</i>",
			"tb_not_found": "Traceback не найден",
			"starting_alert": "🚀 Xioca включается, ожидайте...",
			"starting_text": "<b>🚀 Юзербот включается...</b>\n🌙 <b>Установлено модулей:</b> {count}\n✏ <b>Префикс(ы):</b> ({prefix})\n\n👇 <i>Жми любую кнопку ниже что бы выполнить какое либо действие с юзерботом.</i>",
			"need_start": "❌ Юзербота необходимо сначала включить!",
			"restarting_alert": "🔄 Xioca перезагружается, ожидайте...",
			"restarting_text": "<b>🔄 Юзербот перезагружается...</b>\n🌙 Установлено модулей:</b> {count}\n✏ <b>Префикс(ы):</b> ({prefix})\n\n👇 <i>Жми любую кнопку ниже что бы выполнить какое либо действие с юзерботом.</i>",
			"latest_ver": "✅ У вас установлена последняя версия Xioca!",
			"select_logs": "👇 Выберите уровень логов",
			"no_logs": "❕ Нет логов на уровне {lvl} ({name})",
			"settings_text": "⚙ Это <b>меню настроек</b> Xioca. Тут можно полноценно управлять юзерботом и выполнять функции, которые не доступны в юзерботе.\n\n👇 <i>Выберай ниже, что необходимо настроить.</i>",
			"mod_manager_text": "🌙 Это <b>модульный менеджер</b> всех твоих модулей. Тут ты имеешь полную власть над ними. Это меню может часто пригодится при неполадках с юзерботом.\n\n👇 <i>Выбери модуль ниже, что бы выполнить какое либо действие с ним.</i>",
			"mod_author": "<b>❤️ Автор:</b> <code>{author}</code>\n",
			"mod_version": "<b>0️⃣ Версия:</b> <code>{version}</code>\n",
			"mod_desc_header": "\n<b>✍️ Описание:</b>\n    ╰ {desc}\n",
			"no_mod_desc": "Нет описания для модуля",
			"mod_info_title": "<b>🌙 Модуль:</b> <code>{name}</code>\n{author}{ver}{desc}\n{prompt}",
			"mod_action_prompt": "👇 <i>Выбери, какое действие выполнить с модулем.</i>",
			"mod_system_prompt": "🙅‍♂ <i>Это системный модуль, невозможно выполнить какие либо действия с ним.</i>",
			"mod_unloaded": '✅ Модуль "{mod}" успешно выгружен!',
			"db_menu_text": "🗂 Это меню с настройками <b>базы данных</b> (SQLite3). Будь очень оккуратен с этим меню, одно лишнее действие может повлечь за собой очень плохие последствия.\n\n👇 <i>Выберай следующее действие, которое необходимо выполнить.</i>",
			"sql_prompt": "⚙ Вводи сюда SQL запрос с <b>большой осторожностью</b>. Даже одна маленькая ошибка в запросе может повлечь последствия.\n\nℹ Пример запроса: <code>db.get(...)</code>",
			"db_caption": "🗂 <b>База данных Xioca за</b> <code>{date}</code>",
			"info_text": "🌙 <b>Xioca userbot</b> <code>{ver}</code>\n🧑‍💻 <b>Разработчик:</b> <a href='https://t.me/shashachkaaa'>Илья Евгеньевич</a>",
			"not_sql": "❌ <b>Это не SQL запрос!</b>",
			"sql_error": "❌ <b>Произошла ошибка:</b> <code>{error}</code>",
			"sql_success": "✅ <b>SQL запрос успешно выполнен:</b>\n<code>{result}</code>"
		},
		"en": {
			"slang": "🌎 Xioca supports multiple languages, please choose the language you need",
			"btn_control": "🎛 Userbot Control",
			"btn_settings": "⚙ Userbot Settings",
			"btn_info": "ℹ Information",
			"btn_stop": "🔴 Stop Userbot",
			"btn_start": "🟢 Start Userbot",
			"btn_restart": "🔄 Restart Userbot",
			"btn_check_update": "🆕 Check for Updates",
			"btn_logs": "📤 Get Logs",
			"btn_back": "◀ Back",
			"btn_mod_manager": "🌙 Module Manager",
			"btn_db_settings": "🗂 Database",
			"btn_sql_query": "⚙ Execute SQL Query",
			"btn_dl_db": "📤 Download Database",
			"btn_support": "🆘 Support",
			"btn_mods_link": "🗃 Modules",
			"btn_delete": "🗑 Delete",
			"btn_update": "🔄 Install Update",
			"btn_yes": "✅ Yes",
			"btn_no": "❌ No",
			"no_update_desc": "ℹ No update description",
			"no_commits": "ℹ No recent changes data",
			"last_commit": "📌 <b>Last commit <code>{sha}</code>:</b>",
			"update_desc_header": "📝 <b>Update description:</b>",
			"changed_files": "📂 <b>Changed files ({count}):</b>",
			"crit_update": "🚨 <b>CRITICAL UPDATE!</b>\n",
			"new_version": "🔔 <b>New version available!</b>",
			"version_info": "Current version: <code>{curr}</code>\nNew version: <code>{new}</code>\n\n{changes}",
			"uptime_prefix": "⌚ <b>Uptime:</b> {uptime}\n",
			"status_on": "🟢 Userbot active",
			"status_off": "🔴 Userbot disabled",
			"control_menu": "🎛 With this menu you can <b>control the userbot</b>.\n\n<b>{status}\n🌙 Installed modules:</b> {count}\n✏ <b>Prefix(es):</b> ({prefix})\n{uptime}\n👇 <i>Press any button below to perform an action.</i>",
			"install_success": "🌙 <b>Xioca successfully installed and active!</b>\n\nℹ <b>Quick command guide:</b>\n<code>.help</code> - Show all commands\n<code>.help</code> [command / module] - Get help for specific command.\n<code>.loadmod</code> [reply to file] - Load module from file.\n<code>.unloadmod</code> [module] - Unload module.\n<code>.ping</code> - Check if bot is working.\n<code>.restart</code> - Restart bot.\n<code>.update</code> - Update bot.\n<code>.logs</code> - Get bot logs.\n<code>.terminal</code> [command] - Execute command.",
			"folder_prompt": "💡 Create a folder with support/offtopic chats, inline bot and Xioca info channel?",
			"manager_loaded": "Bot command manager loaded!",
			"not_your_btn": "Not your button!",
			"folder_created": '✅ "Xioca" folder successfully created!',
			"sad_emoji": "😢",
			"start_text": "😎 This is <code>Xioca</code>. Excellent userbot with many commands and modules.\n\n❓ <b>How to install?</b>\nUse the <a href='https://xioca.ferz.live'>website</a> for <b>installation</b>.\n\n🌟 <b>Features:</b>\n- Convenient command control.\n- Inline mode support.\n- Modular architecture.\n- Regular updates and support.\n\n📚 <b>Documentation:</b>\nLearn more about features and configuration in <a href='https://github.com/shashachkaaa/Xioca'>documentation</a>.\n\n🛠 <b>Support:</b>\nIf you have questions, contact <a href='https://t.me/xiocasupport'>support chat</a>.",
			"welcome_text": "👋 <b>Welcome</b>, I am part of your userbot <code>Xioca</code>, here you can find settings, info and more.\n\n👇 <i>Press any button below for details.</i>",
			"tb_not_found": "Traceback not found",
			"starting_alert": "🚀 Xioca is starting, please wait...",
			"starting_text": "<b>🚀 Userbot starting...</b>\n🌙 <b>Installed modules:</b> {count}\n✏ <b>Prefix(es):</b> ({prefix})\n\n👇 <i>Press any button below to perform an action.</i>",
			"need_start": "❌ Userbot must be started first!",
			"restarting_alert": "🔄 Xioca is restarting, please wait...",
			"restarting_text": "<b>🔄 Userbot restarting...</b>\n🌙 Installed modules:</b> {count}\n✏ <b>Prefix(es):</b> ({prefix})\n\n👇 <i>Press any button below to perform an action.</i>",
			"latest_ver": "✅ You have the latest version of Xioca!",
			"select_logs": "👇 Select log level",
			"no_logs": "❕ No logs at level {lvl} ({name})",
			"settings_text": "⚙ This is <b>Xioca settings menu</b>. Here you can fully control the userbot.\n\n👇 <i>Select what you need to configure below.</i>",
			"mod_manager_text": "🌙 This is the <b>module manager</b>. Here you have full power over your modules. Useful for troubleshooting.\n\n👇 <i>Select a module below to perform an action.</i>",
			"mod_author": "<b>❤️ Author:</b> <code>{author}</code>\n",
			"mod_version": "<b>0️⃣ Version:</b> <code>{version}</code>\n",
			"mod_desc_header": "\n<b>✍️ Description:</b>\n    ╰ {desc}\n",
			"no_mod_desc": "No description for module",
			"mod_info_title": "<b>🌙 Module:</b> <code>{name}</code>\n{author}{ver}{desc}\n{prompt}",
			"mod_action_prompt": "👇 <i>Choose an action to perform with the module.</i>",
			"mod_system_prompt": "🙅‍♂ <i>This is a system module, no actions available.</i>",
			"mod_unloaded": '✅ Module "{mod}" successfully unloaded!',
			"db_menu_text": "🗂 This is the <b>database</b> settings menu. Be very careful here.\n\n👇 <i>Choose an action below.</i>",
			"sql_prompt": "⚙ Enter SQL query here with <b>great caution</b>. Even a small error can have consequences.\n\nℹ Example: <code>db.get(...)</code>",
			"db_caption": "🗂 <b>Xioca Database for</b> <code>{date}</code>",
			"info_text": "🌙 <b>Xioca userbot</b> <code>{ver}</code>\n🧑‍💻 <b>Developer:</b> <a href='https://t.me/shashachkaaa'>Ilya Evgenyevich</a>",
			"not_sql": "❌ <b>This is not a SQL query!</b>",
			"sql_error": "❌ <b>Error occurred:</b> <code>{error}</code>",
			"sql_success": "✅ <b>SQL query successfully executed:</b>\n<code>{result}</code>"
		},
		"be": {
			"slang": "🌎 Xioca падтрымлівае некалькі моў, калі ласка, выберыце неабходную вам мову",
			"btn_control": "🎛 Кіраванне юзерботам",
			"btn_settings": "⚙ Налады юзербота",
			"btn_info": "ℹ Інфармацыя",
			"btn_stop": "🔴 Выключыць юзербота",
			"btn_start": "🟢 Уключыць юзербота",
			"btn_restart": "🔄 Перазагрузіць юзербота",
			"btn_check_update": "🆕 Праверыць наяўнасць абнаўленняў",
			"btn_logs": "📤 Атрымаць логі",
			"btn_back": "◀ Назад",
			"btn_mod_manager": "🌙 Модульны менеджэр",
			"btn_db_settings": "🗂 База дадзеных",
			"btn_sql_query": "⚙ Выканаць SQL запыт",
			"btn_dl_db": "📤 Спампаваць базу дадзеных",
			"btn_support": "🆘 Падтрымка",
			"btn_mods_link": "🗃 Модулі",
			"btn_delete": "🗑 Выдаліць",
			"btn_update": "🔄 Усталяваць абнаўленне",
			"btn_yes": "✅ Так",
			"btn_no": "❌ Не",
			"no_update_desc": "ℹ Няма апісання абнаўлення",
			"no_commits": "ℹ Няма дадзеных пра апошнія змены",
			"last_commit": "📌 <b>Апошняе змяненне <code>{sha}</code>:</b>",
			"update_desc_header": "📝 <b>Апісанне абнаўлення:</b>",
			"changed_files": "📂 <b>Змененыя файлы ({count}):</b>",
			"crit_update": "🚨 <b>КРЫТЫЧНАЕ АБНАЎЛЕННЕ!</b>\n",
			"new_version": "🔔 <b>Даступная новая версія!</b>",
			"version_info": "Бягучая версія: <code>{curr}</code>\nНовая версія: <code>{new}</code>\n\n{changes}",
			"uptime_prefix": "⌚ <b>Час працы:</b> {uptime}\n",
			"status_on": "🟢 Юзербот актыўны",
			"status_off": "🔴 Юзербот выключаны",
			"control_menu": "🎛 З дапамогай гэтага меню вы зможаце <b>кіраваць юзерботам</b>.\n\n<b>{status}\n🌙 Усталявана модуляў:</b> {count}\n✏ <b>Прэфікс(ы):</b> ({prefix})\n{uptime}\n👇 <i>Цісні любую кнопку ніжэй каб выканаць дзеянне.</i>",
			"install_success": "🌙 <b>Xioca паспяхова ўсталявана і актыўная!</b>",
			"folder_prompt": "💡 Стварыць папку з чатамі падтрымкі, інлайн ботам і каналам Xioca?",
			"manager_loaded": "Менеджэр каманд бота загружаны!",
			"not_your_btn": "Кнопка не ваша!",
			"folder_created": '✅ Папка "Xioca" паспяхова створана!',
			"sad_emoji": "😢",
			"start_text": "😎 Гэта - <code>Xioca</code>. Выдатны юзербот з вялікай колькасцю каманд.",
			"welcome_text": "👋 <b>Вітаю</b>, я - частка твайго юзербота <code>Xioca</code>.\n\n👇 <i>Выберы дзеянне ніжэй.</i>",
			"tb_not_found": "Traceback не знойдзены",
			"starting_alert": "🚀 Xioca ўключаецца, пачакайце...",
			"starting_text": "<b>🚀 Юзербот ўключаецца...</b>",
			"need_start": "❌ Юзербота неабходна спачатку ўключыць!",
			"restarting_alert": "🔄 Xioca перазагружаецца...",
			"restarting_text": "<b>🔄 Юзербот перазагружаецца...</b>",
			"latest_ver": "✅ У вас усталявана апошняя версія Xioca!",
			"select_logs": "👇 Выберыце ўзровень логаў",
			"no_logs": "❕ Няма логаў на ўзроўні {lvl} ({name})",
			"settings_text": "⚙ Гэта меню налад Xioca.",
			"mod_manager_text": "🌙 Гэта модульны менеджэр усіх тваіх модуляў.",
			"mod_author": "<b>❤️ Аўтар:</b> <code>{author}</code>\n",
			"mod_version": "<b>0️⃣ Версія:</b> <code>{version}</code>\n",
			"mod_desc_header": "\n<b>✍️ Апісанне:</b>\n    ╰ {desc}\n",
			"no_mod_desc": "Няма апісання модуля",
			"mod_info_title": "<b>🌙 Модуль:</b> <code>{name}</code>\n{author}{ver}{desc}\n{prompt}",
			"mod_action_prompt": "👇 <i>Выберыце дзеянне для модуля.</i>",
			"mod_system_prompt": "🙅‍♂ <i>Гэта сістэмны модуль, дзеянні немагчымыя.</i>",
			"mod_unloaded": '✅ Модуль "{mod}" паспяхова выгружаны!',
			"db_menu_text": "🗂 Налады базы дадзеных (SQLite3).",
			"sql_prompt": "⚙ Уводзьце SQL запыт з асцярожнасцю.",
			"db_caption": "🗂 <b>База дадзеных Xioca за</b> <code>{date}</code>",
			"info_text": "🌙 <b>Xioca userbot</b> <code>{ver}</code>\n🧑‍💻 <b>Распрацоўшчык:</b> <a href='https://t.me/shashachkaaa'>Ілья Яўгенавіч</a>",
			"not_sql": "❌ <b>Гэта не SQL запыт!</b>",
			"sql_error": "❌ <b>Памылка:</b> <code>{error}</code>",
			"sql_success": "✅ <b>Запыт выкананы:</b>\n<code>{result}</code>"
		},
		"de": {
			"slang": "🌎 Xioca unterstützt mehrere Sprachen, bitte wählen Sie die gewünschte Sprache",
			"btn_control": "🎛 Steuerung",
			"btn_settings": "⚙ Einstellungen",
			"btn_info": "ℹ Information",
			"btn_stop": "🔴 Userbot stoppen",
			"btn_start": "🟢 Userbot starten",
			"btn_restart": "🔄 Userbot neu starten",
			"btn_check_update": "🆕 Nach Updates suchen",
			"btn_logs": "📤 Logs abrufen",
			"btn_back": "◀ Zurück",
			"btn_mod_manager": "🌙 Modul-Manager",
			"btn_db_settings": "🗂 Datenbank",
			"btn_sql_query": "⚙ SQL-Abfrage ausführen",
			"btn_dl_db": "📤 Datenbank herunterladen",
			"btn_support": "🆘 Support",
			"btn_mods_link": "🗃 Module",
			"btn_delete": "🗑 Löschen",
			"btn_update": "🔄 Update installieren",
			"btn_yes": "✅ Ja",
			"btn_no": "❌ Nein",
			"no_update_desc": "ℹ Keine Update-Beschreibung",
			"no_commits": "ℹ Keine aktuellen Änderungen",
			"last_commit": "📌 <b>Letzte Änderung <code>{sha}</code>:</b>",
			"update_desc_header": "📝 <b>Update-Beschreibung:</b>",
			"changed_files": "📂 <b>Geänderte Dateien ({count}):</b>",
			"crit_update": "🚨 <b>KRITISCHES UPDATE!</b>\n",
			"new_version": "🔔 <b>Neue Version verfügbar!</b>",
			"version_info": "Aktuelle Version: <code>{curr}</code>\nNeue Version: <code>{new}</code>\n\n{changes}",
			"uptime_prefix": "⌚ <b>Laufzeit:</b> {uptime}\n",
			"status_on": "🟢 Userbot aktiv",
			"status_off": "🔴 Userbot deaktiviert",
			"control_menu": "🎛 Hier können Sie den <b>Userbot steuern</b>.\n\n<b>{status}\n🌙 Installierte Module:</b> {count}\n✏ <b>Präfix(e):</b> ({prefix})\n{uptime}",
			"install_success": "🌙 <b>Xioca erfolgreich installiert!</b>",
			"folder_prompt": "💡 Ordner für Support-Chats und Xioca-Info erstellen?",
			"manager_loaded": "Bot-Manager geladen!",
			"not_your_btn": "Nicht Ihre Schaltfläche!",
			"folder_created": '✅ Ordner "Xioca" wurde erstellt!',
			"sad_emoji": "😢",
			"start_text": "😎 Das ist <code>Xioca</code>. Ein exzellenter Userbot.",
			"welcome_text": "👋 <b>Willkommen</b>, ich bin Teil deines <code>Xioca</code> Userbots.",
			"tb_not_found": "Traceback nicht gefunden",
			"starting_alert": "🚀 Xioca startet, bitte warten...",
			"starting_text": "<b>🚀 Userbot startet...</b>",
			"need_start": "❌ Userbot muss zuerst gestartet werden!",
			"restarting_alert": "🔄 Xioca startet neu...",
			"restarting_text": "<b>🔄 Userbot startet neu...</b>",
			"latest_ver": "✅ Du hast die neueste Version von Xioca!",
			"select_logs": "👇 Log-Level wählen",
			"no_logs": "❕ Keine Logs für Level {lvl} ({name})",
			"settings_text": "⚙ Xioca-Einstellungen.",
			"mod_manager_text": "🌙 Modul-Manager für alle installierten Module.",
			"mod_author": "<b>❤️ Autor:</b> <code>{author}</code>\n",
			"mod_version": "<b>0️⃣ Version:</b> <code>{version}</code>\n",
			"mod_desc_header": "\n<b>✍️ Beschreibung:</b>\n    ╰ {desc}\n",
			"no_mod_desc": "Keine Beschreibung verfügbar",
			"mod_info_title": "<b>🌙 Modul:</b> <code>{name}</code>\n{author}{ver}{desc}\n{prompt}",
			"mod_action_prompt": "👇 Aktion wählen.",
			"mod_system_prompt": "🙅‍♂ <i>Systemmodul: Keine Aktionen möglich.</i>",
			"mod_unloaded": '✅ Modul "{mod}" entladen!',
			"db_menu_text": "🗂 Datenbankeinstellungen (SQLite3).",
			"sql_prompt": "⚙ SQL-Abfrage mit Vorsicht eingeben.",
			"db_caption": "🗂 <b>Xioca Datenbank vom</b> <code>{date}</code>",
			"info_text": "🌙 <b>Xioca userbot</b> <code>{ver}</code>\n🧑‍💻 <b>Entwickler:</b> Ilya Evgenievich",
			"not_sql": "❌ <b>Keine SQL-Abfrage!</b>",
			"sql_error": "❌ <b>Fehler:</b> <code>{error}</code>",
			"sql_success": "✅ <b>SQL erfolgreich:</b>\n<code>{result}</code>"
		},
		"es": {
			"slang": "🌎 Xioca es compatible con varios idiomas, por favor, elija el idioma que necesite",
			"btn_control": "🎛 Control del Userbot",
			"btn_settings": "⚙ Ajustes",
			"btn_info": "ℹ Información",
			"btn_stop": "🔴 Detener",
			"btn_start": "🟢 Iniciar",
			"btn_restart": "🔄 Reiniciar",
			"btn_check_update": "🆕 Buscar actualizaciones",
			"btn_logs": "📤 Obtener Logs",
			"btn_back": "◀ Volver",
			"btn_mod_manager": "🌙 Gestor de Módulos",
			"btn_db_settings": "🗂 Base de Datos",
			"btn_sql_query": "⚙ Ejecutar SQL",
			"btn_dl_db": "📤 Descargar BD",
			"btn_support": "🆘 Soporte",
			"btn_mods_link": "🗃 Módulos",
			"btn_delete": "🗑 Eliminar",
			"btn_update": "🔄 Instalar actualización",
			"btn_yes": "✅ Sí",
			"btn_no": "❌ No",
			"no_update_desc": "ℹ Sin descripción de actualización",
			"no_commits": "ℹ Sin datos de cambios recientes",
			"last_commit": "📌 <b>Último cambio <code>{sha}</code>:</b>",
			"update_desc_header": "📝 <b>Descripción:</b>",
			"changed_files": "📂 <b>Archivos modificados ({count}):</b>",
			"crit_update": "🚨 <b>¡ACTUALIZACIÓN CRÍTICA!</b>\n",
			"new_version": "🔔 <b>¡Nueva versión disponible!</b>",
			"version_info": "Versión actual: <code>{curr}</code>\nNueva versión: <code>{new}</code>\n\n{changes}",
			"uptime_prefix": "⌚ <b>Tiempo activo:</b> {uptime}\n",
			"status_on": "🟢 Userbot activo",
			"status_off": "🔴 Userbot desactivado",
			"control_menu": "🎛 Menú de <b>control del userbot</b>.\n\n<b>{status}\n🌙 Módulos:</b> {count}\n✏ <b>Prefijo:</b> ({prefix})\n{uptime}",
			"install_success": "🌙 <b>¡Xioca instalado correctamente!</b>",
			"folder_prompt": "💡 ¿Crear carpeta con chats de soporte e info?",
			"manager_loaded": "¡Gestor de comandos cargado!",
			"not_your_btn": "¡No es tu botón!",
			"folder_created": '✅ ¡Carpeta "Xioca" creada!',
			"sad_emoji": "😢",
			"start_text": "😎 Este es <code>Xioca</code>. Un excelente userbot.",
			"welcome_text": "👋 <b>Bienvenido</b>, soy parte de tu userbot <code>Xioca</code>.",
			"tb_not_found": "Traceback no encontrado",
			"starting_alert": "🚀 Xioca iniciando...",
			"starting_text": "<b>🚀 Iniciando userbot...</b>",
			"need_start": "❌ ¡Inicia el userbot primero!",
			"restarting_alert": "🔄 Reiniciando...",
			"restarting_text": "<b>🔄 Reiniciando userbot...</b>",
			"latest_ver": "✅ ¡Tienes la última versión!",
			"select_logs": "👇 Selecciona nivel de logs",
			"no_logs": "❕ Sin logs en nivel {lvl}",
			"settings_text": "⚙ Menú de ajustes de Xioca.",
			"mod_manager_text": "🌙 Gestor de todos tus módulos.",
			"mod_author": "<b>❤️ Autor:</b> <code>{author}</code>\n",
			"mod_version": "<b>0️⃣ Versión:</b> <code>{version}</code>\n",
			"mod_desc_header": "\n<b>✍️ Descripción:</b>\n    ╰ {desc}\n",
			"no_mod_desc": "Sin descripción",
			"mod_info_title": "<b>🌙 Módulo:</b> <code>{name}</code>\n{author}{ver}{desc}\n{prompt}",
			"mod_action_prompt": "👇 Elige una acción.",
			"mod_system_prompt": "🙅‍♂ <i>Módulo del sistema: sin acciones.</i>",
			"mod_unloaded": '✅ ¡Módulo "{mod}" eliminado!',
			"db_menu_text": "🗂 Ajustes de base de datos.",
			"sql_prompt": "⚙ Ingresa consulta SQL con precaución.",
			"db_caption": "🗂 <b>Base de datos del</b> <code>{date}</code>",
			"info_text": "🌙 <b>Xioca userbot</b> <code>{ver}</code>\n🧑‍💻 <b>Desarrollador:</b> Ilya Evgenievich",
			"not_sql": "❌ <b>¡No es SQL!</b>",
			"sql_error": "❌ <b>Error:</b> <code>{error}</code>",
			"sql_success": "✅ <b>SQL ejecutado:</b>\n<code>{result}</code>"
		},
		"fr": {
			"slang": "🌎 Xioca prend en charge plusieurs langues, veuillez choisir la langue dont vous avez besoin",
			"btn_control": "🎛 Contrôle",
			"btn_settings": "⚙ Paramètres",
			"btn_info": "ℹ Info",
			"btn_stop": "🔴 Arrêter",
			"btn_start": "🟢 Démarrer",
			"btn_restart": "🔄 Redémarrer",
			"btn_check_update": "🆕 Mises à jour",
			"btn_logs": "📤 Logs",
			"btn_back": "◀ Retour",
			"btn_mod_manager": "🌙 Modules",
			"btn_db_settings": "🗂 Base de données",
			"btn_sql_query": "⚙ Requête SQL",
			"btn_dl_db": "📤 Télécharger BD",
			"btn_support": "🆘 Support",
			"btn_mods_link": "🗃 Modules",
			"btn_delete": "🗑 Supprimer",
			"btn_update": "🔄 Installer l'update",
			"btn_yes": "✅ Oui",
			"btn_no": "❌ Non",
			"no_update_desc": "ℹ Pas de description",
			"no_commits": "ℹ Pas de changements récents",
			"last_commit": "📌 <b>Dernier commit <code>{sha}</code>:</b>",
			"update_desc_header": "📝 <b>Description:</b>",
			"changed_files": "📂 <b>Fichiers modifiés ({count}):</b>",
			"crit_update": "🚨 <b>MISE À JOUR CRITIQUE !</b>\n",
			"new_version": "🔔 <b>Nouvelle version disponible !</b>",
			"version_info": "Version actuelle: <code>{curr}</code>\nNouvelle: <code>{new}</code>\n\n{changes}",
			"uptime_prefix": "⌚ <b>Uptime:</b> {uptime}\n",
			"status_on": "🟢 Actif",
			"status_off": "🔴 Désactivé",
			"control_menu": "🎛 Contrôle de votre <b>userbot</b>.\n\n<b>{status}\n🌙 Modules:</b> {count}\n✏ <b>Prefix:</b> ({prefix})",
			"install_success": "🌙 <b>Xioca installé avec succès !</b>",
			"folder_prompt": "💡 Créer un dossier avec les chats support ?",
			"manager_loaded": "Gestionnaire chargé !",
			"not_your_btn": "Pas votre bouton !",
			"folder_created": '✅ Dossier "Xioca" créé !',
			"sad_emoji": "😢",
			"start_text": "😎 C'est <code>Xioca</code>.",
			"welcome_text": "👋 <b>Bienvenue</b>, je suis votre userbot <code>Xioca</code>.",
			"tb_not_found": "Traceback non trouvé",
			"starting_alert": "🚀 Lancement de Xioca...",
			"starting_text": "<b>🚀 Démarrage...</b>",
			"need_start": "❌ Démarrez d'abord !",
			"restarting_alert": "🔄 Redémarrage...",
			"restarting_text": "<b>🔄 Redémarrage en cours...</b>",
			"latest_ver": "✅ Version à jour !",
			"select_logs": "👇 Niveau de logs",
			"no_logs": "❕ Aucun log niveau {lvl}",
			"settings_text": "⚙ Paramètres Xioca.",
			"mod_manager_text": "🌙 Gestionnaire de modules.",
			"mod_author": "<b>❤️ Auteur:</b> <code>{author}</code>\n",
			"mod_version": "<b>0️⃣ Version:</b> <code>{version}</code>\n",
			"mod_desc_header": "\n<b>✍️ Description:</b>\n    ╰ {desc}\n",
			"no_mod_desc": "Pas de description",
			"mod_info_title": "<b>🌙 Module:</b> <code>{name}</code>\n{author}{ver}{desc}\n{prompt}",
			"mod_action_prompt": "👇 Choisir une action.",
			"mod_system_prompt": "🙅‍♂ <i>Module système : aucune action.</i>",
			"mod_unloaded": '✅ Module "{mod}" déchargé !',
			"db_menu_text": "🗂 Paramètres BD.",
			"sql_prompt": "⚙ Requête SQL (attention).",
			"db_caption": "🗂 <b>BD du</b> <code>{date}</code>",
			"info_text": "🌙 <b>Xioca</b> <code>{ver}</code>\n🧑‍💻 Dev: Ilya Evgenievich",
			"not_sql": "❌ <b>Pas du SQL !</b>",
			"sql_error": "❌ <b>Erreur:</b> <code>{error}</code>",
			"sql_success": "✅ <b>Succès SQL:</b>\n<code>{result}</code>"
		},
		"it": {
			"slang": "🌎 Xioca supporta più lingue, per favore, seleziona la lingua di cui hai bisogno",
			"btn_control": "🎛 Controllo",
			"btn_settings": "⚙ Impostazioni",
			"btn_info": "ℹ Info",
			"btn_stop": "🔴 Ferma",
			"btn_start": "🟢 Avvia",
			"btn_restart": "🔄 Riavvia",
			"btn_check_update": "🆕 Aggiornamenti",
			"btn_logs": "📤 Log",
			"btn_back": "◀ Indietro",
			"btn_mod_manager": "🌙 Moduli",
			"btn_db_settings": "🗂 Database",
			"btn_sql_query": "⚙ Query SQL",
			"btn_dl_db": "📤 Scarica DB",
			"btn_support": "🆘 Supporto",
			"btn_mods_link": "🗃 Moduli",
			"btn_delete": "🗑 Elimina",
			"btn_update": "🔄 Installa",
			"btn_yes": "✅ Sì",
			"btn_no": "❌ No",
			"no_update_desc": "ℹ Nessuna descrizione",
			"no_commits": "ℹ Nessun dato recente",
			"last_commit": "📌 <b>Ultimo commit <code>{sha}</code>:</b>",
			"update_desc_header": "📝 <b>Descrizione:</b>",
			"changed_files": "📂 <b>File modificati ({count}):</b>",
			"crit_update": "🚨 <b>AGGIORNAMENTO CRITICO!</b>\n",
			"new_version": "🔔 <b>Nuova versione!</b>",
			"version_info": "Corrente: <code>{curr}</code>\nNuova: <code>{new}</code>\n\n{changes}",
			"uptime_prefix": "⌚ <b>Uptime:</b> {uptime}\n",
			"status_on": "🟢 Attivo",
			"status_off": "🔴 Disattivato",
			"control_menu": "🎛 Gestione <b>userbot</b>.\n\n<b>{status}\n🌙 Moduli:</b> {count}\n✏ <b>Prefisso:</b> ({prefix})",
			"install_success": "🌙 <b>Xioca installato!</b>",
			"folder_prompt": "💡 Creare cartella di supporto?",
			"manager_loaded": "Gestore caricato!",
			"not_your_btn": "Non è il tuo tasto!",
			"folder_created": '✅ Cartella "Xioca" creata!',
			"sad_emoji": "😢",
			"start_text": "😎 Questo è <code>Xioca</code>.",
			"welcome_text": "👋 <b>Benvenuto</b>, sono <code>Xioca</code>.",
			"tb_not_found": "Traceback non trovato",
			"starting_alert": "🚀 Avvio in corso...",
			"starting_text": "<b>🚀 Avvio...</b>",
			"need_start": "❌ Avvialo prima!",
			"restarting_alert": "🔄 Riavvio...",
			"restarting_text": "<b>🔄 Riavvio...</b>",
			"latest_ver": "✅ Versione aggiornata!",
			"select_logs": "👇 Livello log",
			"no_logs": "❕ Nessun log livello {lvl}",
			"settings_text": "⚙ Impostazioni Xioca.",
			"mod_manager_text": "🌙 Gestore moduli.",
			"mod_author": "<b>❤️ Autore:</b> <code>{author}</code>\n",
			"mod_version": "<b>0️⃣ Versione:</b> <code>{version}</code>\n",
			"mod_desc_header": "\n<b>✍️ Descrizione:</b>\n    ╰ {desc}\n",
			"no_mod_desc": "Nessuna descrizione",
			"mod_info_title": "<b>🌙 Modulo:</b> <code>{name}</code>\n{author}{ver}{desc}\n{prompt}",
			"mod_action_prompt": "👇 Scegli azione.",
			"mod_system_prompt": "🙅‍♂ <i>Modulo sistema: nessuna azione.</i>",
			"mod_unloaded": '✅ Modulo "{mod}" rimosso!',
			"db_menu_text": "🗂 Impostazioni DB.",
			"sql_prompt": "⚙ Query SQL (attenzione).",
			"db_caption": "🗂 <b>DB del</b> <code>{date}</code>",
			"info_text": "🌙 <b>Xioca</b> <code>{ver}</code>\n🧑‍💻 Dev: Ilya Evgenievich",
			"not_sql": "❌ <b>Non è SQL!</b>",
			"sql_error": "❌ <b>Errore:</b> <code>{error}</code>",
			"sql_success": "✅ <b>SQL eseguito:</b>\n<code>{result}</code>"
		},
		"kk": {
			"slang": "🌎 Xioca бірнеше тілді қолдайды, қажетті тілді таңдаңыз",
			"btn_control": "🎛 Юзерботты басқару",
			"btn_settings": "⚙ Юзербот баптаулары",
			"btn_info": "ℹ Ақпарат",
			"btn_stop": "🔴 Юзерботты өшіру",
			"btn_start": "🟢 Юзерботты қосу",
			"btn_restart": "🔄 Юзерботты қайта жүктеу",
			"btn_check_update": "🆕 Жаңартуларды тексеру",
			"btn_logs": "📤 Логтарды алу",
			"btn_back": "◀ Артқа",
			"btn_mod_manager": "🌙 Модульдік менеджер",
			"btn_db_settings": "🗂 Мәліметтер базасы",
			"btn_sql_query": "⚙ SQL сұранысын орындау",
			"btn_dl_db": "📤 Базаны жүктеп алу",
			"btn_support": "🆘 Қолдау",
			"btn_mods_link": "🗃 Модульдер",
			"btn_delete": "🗑 Өшіру",
			"btn_update": "🔄 Жаңартуды орнату",
			"btn_yes": "✅ Иә",
			"btn_no": "❌ Жоқ",
			"no_update_desc": "ℹ Жаңарту сипаттамасы жоқ",
			"no_commits": "ℹ Соңғы өзгерістер туралы дерек жоқ",
			"last_commit": "📌 <b>Соңғы өзгеріс <code>{sha}</code>:</b>",
			"update_desc_header": "📝 <b>Жаңарту сипаттамасы:</b>",
			"changed_files": "📂 <b>Өзгертілген файлдар ({count}):</b>",
			"crit_update": "🚨 <b>МАҢЫЗДЫ ЖАҢАРТУ!</b>\n",
			"new_version": "🔔 <b>Жаңа нұсқа қолжетімді!</b>",
			"version_info": "Ағымдағы нұсқа: <code>{curr}</code>\nЖаңа нұсқа: <code>{new}</code>\n\n{changes}",
			"uptime_prefix": "⌚ <b>Жұмыс уақыты:</b> {uptime}\n",
			"status_on": "🟢 Юзербот белсенді",
			"status_off": "🔴 Юзербот өшірулі",
			"control_menu": "🎛 Осы мәзір арқылы <b>юзерботты басқара</b> аласыз.\n\n<b>{status}\n🌙 Орнатылған модульдер:</b> {count}\n✏ <b>Префикс(тер):</b> ({prefix})\n{uptime}",
			"install_success": "🌙 <b>Xioca сәтті орнатылды және белсенді!</b>",
			"folder_prompt": "💡 Қолдау чаттары мен Xioca арнасы үшін папка жасау керек пе?",
			"manager_loaded": "Командалар менеджері жүктелді!",
			"not_your_btn": "Бұл сіздің батырмаңыз емес!",
			"folder_created": '✅ "Xioca" папкасы жасалды!',
			"sad_emoji": "😢",
			"start_text": "😎 Бұл - <code>Xioca</code>. Көптеген командалары бар юзербот.",
			"welcome_text": "👋 <b>Сәлем</b>, мен сенің <code>Xioca</code> юзерботыңның бөлігімін.",
			"tb_not_found": "Traceback табылмады",
			"starting_alert": "🚀 Xioca қосылуда, күте тұрыңыз...",
			"starting_text": "<b>🚀 Юзербот қосылуда...</b>",
			"need_start": "❌ Алдымен юзерботты қосу керек!",
			"restarting_alert": "🔄 Қайта жүктелуде...",
			"restarting_text": "<b>🔄 Юзербот қайта жүктелуде...</b>",
			"latest_ver": "✅ Сізде Xioca-ның соңғы нұсқасы орнатылған!",
			"select_logs": "👇 Лог деңгейін таңдаңыз",
			"no_logs": "❕ {lvl} деңгейінде логтар жоқ",
			"settings_text": "⚙ Бұл - Xioca баптаулар мәзірі.",
			"mod_manager_text": "🌙 Бұл - модульдер менеджері.",
			"mod_author": "<b>❤️ Авторы:</b> <code>{author}</code>\n",
			"mod_version": "<b>0️⃣ Нұсқасы:</b> <code>{version}</code>\n",
			"mod_desc_header": "\n<b>✍️ Сипаттамасы:</b>\n    ╰ {desc}\n",
			"no_mod_desc": "Модуль сипаттамасы жоқ",
			"mod_info_title": "<b>🌙 Модуль:</b> <code>{name}</code>\n{author}{ver}{desc}\n{prompt}",
			"mod_action_prompt": "👇 Модульмен әрекетті таңдаңыз.",
			"mod_system_prompt": "🙅‍♂ <i>Бұл жүйелік модуль, әрекет ету мүмкін емес.</i>",
			"mod_unloaded": '✅ "{mod}" модулі сәтті жойылды!',
			"db_menu_text": "🗂 Мәліметтер базасының баптаулары.",
			"sql_prompt": "⚙ SQL сұранысын абайлап енгізіңіз.",
			"db_caption": "🗂 <b>Xioca базасы:</b> <code>{date}</code>",
			"info_text": "🌙 <b>Xioca userbot</b> <code>{ver}</code>\n🧑‍💻 <b>Әзірлеуші:</b> Илья Евгеньевич",
			"not_sql": "❌ <b>Бұл SQL сұранысы емес!</b>",
			"sql_error": "❌ <b>Қате:</b> <code>{error}</code>",
			"sql_success": "✅ <b>SQL сәтті орындалды:</b>\n<code>{result}</code>"
		},
		"uz": {
			"slang": "🌎 Xioca bir nechta tillarni qoʻllab-quvvatlaydi, iltimos, sizga kerakli tilni tanlang",
			"btn_control": "🎛 Yuzerbotni boshqarish",
			"btn_settings": "⚙ Sozlamalar",
			"btn_info": "ℹ Ma'lumot",
			"btn_stop": "🔴 O'chirish",
			"btn_start": "🟢 Yoqish",
			"btn_restart": "🔄 Qayta ishga tushirish",
			"btn_check_update": "🆕 Yangilanishlarni tekshirish",
			"btn_logs": "📤 Loglarni olish",
			"btn_back": "◀ Orqaga",
			"btn_mod_manager": "🌙 Modul menejeri",
			"btn_db_settings": "🗂 Ma'lumotlar bazasi",
			"btn_sql_query": "⚙ SQL so'rovini bajarish",
			"btn_dl_db": "📤 Bazani yuklab olish",
			"btn_support": "🆘 Qo'llab-quvvatlash",
			"btn_mods_link": "🗃 Modullar",
			"btn_delete": "🗑 O'chirish",
			"btn_update": "🔄 Yangilanishni o'rnatish",
			"btn_yes": "✅ Ha",
			"btn_no": "❌ Yo'q",
			"no_update_desc": "ℹ Yangilanish tavsifi yo'q",
			"no_commits": "ℹ Oxirgi o'zgarishlar haqida ma'lumot yo'q",
			"last_commit": "📌 <b>Oxirgi o'zgarish <code>{sha}</code>:</b>",
			"update_desc_header": "📝 <b>Tavsif:</b>",
			"changed_files": "📂 <b>O'zgargan fayllar ({count}):</b>",
			"crit_update": "🚨 <b>MUHIM YANGILANISH!</b>\n",
			"new_version": "🔔 <b>Yangi versiya mavjud!</b>",
			"version_info": "Joriy: <code>{curr}</code>\nYangi: <code>{new}</code>\n\n{changes}",
			"uptime_prefix": "⌚ <b>Ish vaqti:</b> {uptime}\n",
			"status_on": "🟢 Faol",
			"status_off": "🔴 O'chirilgan",
			"control_menu": "🎛 <b>Yuzerbotni boshqarish</b> menyusi.\n\n<b>{status}\n🌙 Modullar:</b> {count}\n✏ <b>Prefiks:</b> ({prefix})",
			"install_success": "🌙 <b>Xioca muvaffaqiyatli o'rnatildi!</b>",
			"folder_prompt": "💡 Qo'llab-quvvatlash chatlari uchun jild yaratilsinmi?",
			"manager_loaded": "Menejer yuklandi!",
			"not_your_btn": "Bu sizning tugmangiz emas!",
			"folder_created": '✅ "Xioca" jildi yaratildi!',
			"sad_emoji": "😢",
			"start_text": "😎 Bu - <code>Xioca</code> yuzerboti.",
			"welcome_text": "👋 <b>Xush kelibsiz</b>, men <code>Xioca</code> yuzerbotingman.",
			"tb_not_found": "Traceback topilmadi",
			"starting_alert": "🚀 Xioca yoqilmoqda...",
			"starting_text": "<b>🚀 Yoqilmoqda...</b>",
			"need_start": "❌ Avval botni yoqing!",
			"restarting_alert": "🔄 Qayta yuklanmoqda...",
			"restarting_text": "<b>🔄 Qayta yuklanmoqda...</b>",
			"latest_ver": "✅ Sizda oxirgi versiya o'rnatilgan!",
			"select_logs": "👇 Log darajasini tanlang",
			"no_logs": "❕ {lvl} darajasida loglar yo'q",
			"settings_text": "⚙ Xioca sozlamalari menyusi.",
			"mod_manager_text": "🌙 Modullar menejeri.",
			"mod_author": "<b>❤️ Muallif:</b> <code>{author}</code>\n",
			"mod_version": "<b>0️⃣ Versiya:</b> <code>{version}</code>\n",
			"mod_desc_header": "\n<b>✍️ Tavsif:</b>\n    ╰ {desc}\n",
			"no_mod_desc": "Tavsif yo'q",
			"mod_info_title": "<b>🌙 Modul:</b> <code>{name}</code>\n{author}{ver}{desc}\n{prompt}",
			"mod_action_prompt": "👇 Harakatni tanlang.",
			"mod_system_prompt": "🙅‍♂ <i>Tizim moduli: harakatlar cheklangan.</i>",
			"mod_unloaded": """✅ "{mod}" moduli o'chirildi!""",
			"db_menu_text": "🗂 Baza sozlamalari.",
			"sql_prompt": "⚙ SQL so'rovini ehtiyotkorlik bilan kiriting.",
			"db_caption": "🗂 <b>Baza sanasi:</b> <code>{date}</code>",
			"info_text": "🌙 <b>Xioca</b> <code>{ver}</code>\n🧑‍💻 Tuzuvchi: Ilya Evgenievich",
			"not_sql": "❌ <b>Bu SQL so'rovi emas!</b>",
			"sql_error": "❌ <b>Xato:</b> <code>{error}</code>",
			"sql_success": "✅ <b>SQL muvaffaqiyatli:</b>\n<code>{result}</code>"
		}
	}
	
	def _start(self):
		os.execl(sys.executable, sys.executable, "-m", "xioca")
	
	CRITICAL_KEYWORDS = [
		"security", "critical", "fix", "hotfix", 
		"urgent", "важно", "критично", "исправление",
		"уязвимость", "vulnerability", "фикс"
	]
	
	def _is_critical_update(self, commit_message: str) -> bool:
		commit_message_lower = commit_message.lower()
		return any(keyword in commit_message_lower for keyword in self.CRITICAL_KEYWORDS)
	
	async def auto_check_update(self):
		while True:
			nu = self.db.get("xioca.loader", "new_update", False)
			if not nu:
				await asyncio.sleep(300)
			else:
				await asyncio.sleep(86400)
			await self._check_update()
	
	async def _check_update(self):
		try:
			r = requests.get(__get_version_url__)
			match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", r.text)
			if not match:
				return
			
			version = match.group(1)
			if ver.parse(str(version)) == ver.parse(str(__version__)):
				return False
			
			desc_match = re.search(r"__update_desc__\s*=\s*(?:\"\"\"|''')(.*?)(?:\"\"\"|''')", r.text, re.DOTALL)
			if not desc_match:
				desc_match = re.search(r"__update_desc__\s*=\s*[\"'](.*?)[\"']", r.text, re.DOTALL)
			
			update_description = desc_match.group(1).strip() if desc_match else self.S("no_update_desc")
			
			response = requests.get(__get_commits_url__, params={"per_page": 1})
			response.raise_for_status()
			commits = response.json()
			
			if not commits:
				changes = [self.S("no_commits")]
				is_critical = False
			else:
				commit = commits[0]
				commit_sha = commit["sha"]
				commit_message = commit["commit"]["message"].split("\n")[0]
				is_critical = self._is_critical_update(commit_message)
				commit_url = f"{__get_commits_url__}/{commit_sha}"
				files_response = requests.get(commit_url)
				files_response.raise_for_status()
				commit_data = files_response.json()
				
				files = [f["filename"] for f in commit_data.get("files", [])]
				changes = [
					self.S("last_commit", sha=commit_sha[:7]),
					f"💬 <code>{commit_message}</code>",
					self.S("update_desc_header"),
					f"<code>{update_description}</code>",
					self.S("changed_files", count=len(files))
				]
				
				
				for file in files:
					changes.append(f"  - <code>{file}</code>")
			
			update_header = (
				self.S("crit_update")
				if is_critical else
				self.S("new_version")
			)
			chg = "\n".join(changes)
			
			update_kb = InlineKeyboardBuilder()
			upd = InlineKeyboardButton(text=self.S("btn_update"), callback_data="update")
			update_kb.row(upd)
			await self.bot.send_message(self.all_modules.me.id, f"""{update_header}
{self.S('version_info', curr=__version__, new=version, changes=chg)}""", reply_markup=update_kb.as_markup())
			self.db.set("xioca.loader", "new_update", True)
			return True
		except Exception as e:
			logging.error(f"Ошибка при проверке обновлений: {e}")
	
	async def on_load(self, app: Client):
		status = self.db.set("xioca.loader", "status", True)
		if (restart := self.db.get("xioca.loader", "restart")):
			if restart["type"] == "bot_restart":
				id = restart["msg"].split(":")
				status = self.db.get("xioca.loader", "status", True)
				prefixes = self.db.get("xioca.loader", "prefixes", ["."])
				prefix = " | ".join(prefixes)
				uptime = datetime.now() - __start_time__
				uptime_str = str(uptime).split('.')[0]
				upt = self.S("uptime_prefix", uptime=uptime_str) if status else '\n'
				
				status_str = self.S("status_on") if status else self.S("status_off")
				try:
					await self.bot.edit_message_text(chat_id=int(id[0]), message_id=int(id[1]), text=self.S("control_menu", status=status_str, count=len(self.all_modules.modules), prefix=prefix, uptime=upt), reply_markup=control(status, self.S))
				except:
					pass
		
		if not self.db.get("xioca.loader", "start", False):
			try:
				await self.bot.send_message(self.all_modules.me.id, self.S("install_success"))
				self.db.set("xioca.loader", "start", True)
			except Exception as e:
				logging.error(f"Ошибка при отправке стартового сообщения: {e}")
	
		if self.db.get("xioca.loader", "addfolder", "none") == "none":
			b = InlineKeyboardButton(text=self.S("btn_yes"), callback_data="createfolder_yes")
			b2 = InlineKeyboardButton(text=self.S("btn_no"), callback_data="createfolder_no")
			sugest = InlineKeyboardBuilder()
			sugest.row(b, b2)
			await self.bot.send_message(self.all_modules.me.id, self.S("folder_prompt"), reply_markup=sugest.as_markup())
		else:
			pass
		
		if not self.db.get("xioca.loader", "select_lang", False):
			try:
				await self.bot.send_message(self.all_modules.me.id, self.S("slang"), reply_markup=slang_kb())
			except Exception as e:
				logging.error(f"Ошибка при отправке сообщения: {e}")
			
		asyncio.create_task(self.auto_check_update())
		await self._check_update()
		self.db.set("xioca.bot", "sql_status", False)
		logging.info(self.S("manager_loaded"))
	
	@loader.on_bot(lambda self, app, call: call.data.startswith("select_lang_"))
	async def select_lang_callback_handler(self, app, callback):
		if self.all_modules.me.id != callback.from_user.id:
			return await callback.answer(self.S("not_your_btn"))
		
		cd = callback.data.split("_")
		lang = cd[2]
		
		self.db.set("xioca.loader", "select_lang", True)
		self.db.set("xioca.loader", "language", lang)
		
		await callback.answer("✅")
		
		try:
		    await callback.message.edit_text(self.S("slang"), reply_markup=slang_kb())
		except Exception as e:
			logging.error(e)
	
	@loader.on_bot(lambda self, app, call: call.data.startswith("createfolder_"))
	async def createfolder_callback_handler(self, app, callback):
		if self.all_modules.me.id != callback.from_user.id:
			return await callback.answer(self.S("not_your_btn"))
		
		cd = callback.data.split("_")
		data = cd[1]
		
		if data == "yes":
			self.db.set("xioca.loader", "addfolder", "yes")
			folder_title = "Xioca"
			include_peers_ids = [-1003123091370, -1003124231651, -1003148667569]
			include_peers_usernames = ["xiocainfo", "xiocasupport", "xiocaofftop"]
			
			for _ in include_peers_usernames:
				await app.join_chat(_)
			
			await app.create_folder(name=folder_title, included_chats=include_peers_ids, pinned_chats=[(self.all_modules.bot_manager.bot).id])
			
			await callback.message.edit_text(self.S("folder_created"))
			self.db.set("xioca.loader", "addfolder", "yes")
		else:
			self.db.set("xioca.loader", "addfolder", "no")
			await callback.message.edit_text(self.S("sad_emoji"))
	
	@loader.on_bot(lambda self, app, m: m.text == "/start")
	async def start_message_handler(self, app: Client, message: Message):
		"""Меню"""
    
		if self.all_modules.me.id != message.from_user.id:
			return await message.answer(self.S("start_text"))
		await message.answer(self.S("welcome_text"), reply_markup=start_kb(self.S))
	
	@loader.on_bot(lambda self, app, call: call.data.startswith("traceback_"))
	async def traceback_callback_handler(self, app, callback):
		if self.all_modules.me.id != callback.from_user.id:
			return await callback.answer(self.S("not_your_btn"))
		
		tb = self.db.get("xioca.logger", callback.data)
		
		if tb:
			text = callback.message.html_text
			await callback.message.edit_text(f"{text}\n{tb}")
			self.db.remove("xioca.logger", callback.data)
		else:
			return await callback.answer(self.S("tb_not_found"), True)
	
	@loader.on_bot(lambda self, app, call: call.data.startswith("userbot_"))
	async def userbot_callback_handler(self, app, callback):
		if self.all_modules.me.id != callback.from_user.id:
			return await callback.answer(self.S("not_your_btn"))
		
		cd = callback.data.split("_")
		data = cd[1]
		
		if data == "back":
			self.db.set("xioca.bot", "sql_status", False)
			await callback.message.delete()
			await callback.message.answer(self.S("welcome_text"), reply_markup=start_kb(self.S))
		
		elif data == "control":
			status = self.db.get("xioca.loader", "status", True)
			prefixes = self.db.get("xioca.loader", "prefixes", ["."])
			prefix = " | ".join(prefixes)
			uptime = datetime.now() - __start_time__
			uptime_str = str(uptime).split('.')[0]
			upt = self.S("uptime_prefix", uptime=uptime_str) if status else '\n'
			status_str = self.S("status_on") if status else self.S("status_off")
			
			await callback.message.edit_text(self.S("control_menu", status=status_str, count=len(self.all_modules.modules), prefix=prefix, uptime=upt), reply_markup=control(status, self.S))

		elif data == "stop":
			await app.stop()
			status = self.db.set("xioca.loader", "status", False)
			status = self.db.get("xioca.loader", "status", True)
			prefixes = self.db.get("xioca.loader", "prefixes", ["."])
			prefix = " | ".join(prefixes)
			uptime = datetime.now() - __start_time__
			uptime_str = str(uptime).split('.')[0]
			upt = f'\n{self.S("uptime_prefix", uptime=uptime_str)}' if status else '\n'
			status_str = self.S("status_on") if status else self.S("status_off")
			
			await callback.message.edit_text(self.S("control_menu", status=status_str, count=len(self.all_modules.modules), prefix=prefix, uptime=upt), reply_markup=control(status, self.S))

		elif data == "start":
			atexit.register(self._start)
			
			self.db.set(
				"xioca.loader", "restart", {
					"msg": f"{callback.message.chat.id}:{callback.message.message_id}",
					"type": "bot_restart",
					"time": time.time()
				}
			)
			
			await callback.answer(self.S("starting_alert"), True)
			prefixes = self.db.get("xioca.loader", "prefixes", ["."])
			prefix = " | ".join(prefixes)
			status = self.db.get("xioca.loader", "status", True)
			await callback.message.edit_text(self.S("starting_text", count=len(self.all_modules.modules), prefix=prefix), reply_markup=control(status, self.S))
			sys.exit(0)
			
		elif data == "restart":
			atexit.register(self._start)
			status = self.db.get("xioca.loader", "status", True)
			
			if not status:
				return await callback.answer(self.S("need_start"))
			
			self.db.set(
				"xioca.loader", "restart", {
					"msg": f"{callback.message.chat.id}:{callback.message.message_id}",
					"type": "bot_restart",
					"time": time.time()
				}
			)
			
			status = self.db.set("xioca.loader", "status", True)
			await callback.answer(self.S("restarting_alert"), True)
			prefixes = self.db.get("xioca.loader", "prefixes", ["."])
			prefix = " | ".join(prefixes)
			await callback.message.edit_text(self.S("restarting_text", count=len(self.all_modules.modules), prefix=prefix), reply_markup=control(status, self.S))
			sys.exit(0)
		
		elif data == "checkupdate":
			status = self.db.get("xioca.loader", "status", True)
			
			if not status:
				return await callback.answer(self.S("need_start"))
				
			cu = await self._check_update()
			if not cu:
				return await callback.answer(self.S("latest_ver"), True)
			await callback.answer()
			
		elif data == "logs":
			if len(cd) < 3:
				await callback.message.edit_text(self.S("select_logs"), reply_markup=logs_kb(self.S))
			else:
				lvl = logger.get_valid_level(cd[2])
				handler = logging.getLogger().handlers[0]
				logs = ("\n".join(handler.dumps(lvl))).encode("utf-8")
				if not logs:
					return await callback.answer(self.S("no_logs", lvl=lvl, name=logging.getLevelName(lvl)), True)
				
				logs = io.BytesIO(logs)
				logs.name = f"xioca_{cd[2]}.txt"
				document = BufferedInputFile(logs.read(), filename=f"xioca_{cd[2]}.txt")
				await self.bot.send_document(callback.from_user.id, document=document)
				logs.close()
				await callback.answer()
				
		elif data == "settings":
			await callback.message.edit_text(self.S("settings_text"), reply_markup=settings(self.S))

		elif data == "modulemanager":
			await callback.message.edit_text(self.S("mod_manager_text"), reply_markup=modules_kb(self, page=0))
		
		elif data == "modulespage":
			await callback.message.edit_text(self.S("mod_manager_text"), reply_markup=modules_kb(self, page=int(cd[2])))

		elif data == "module":
			name = cd[2]
			
			if name in __system_mod__:
				actions = False
			else:
				actions = True
			
			module = self.all_modules.get_module(name)
			prefix = self.db.get("xioca.loader", "prefixes", ["."])[0]
			author = self.S("mod_author", author=module.author) if module.author else ""
			vers = self.S("mod_version", version=module.version) if module.version else ""
			desc = self.S("mod_desc_header", desc=module.__doc__ or self.S("no_mod_desc"))
			
			prompt = self.S("mod_action_prompt") if actions else self.S("mod_system_prompt")
			
			await callback.message.edit_text(self.S("mod_info_title", name=module.name, author=author, ver=vers, desc=desc, prompt=prompt), reply_markup=module_settings_kb(self.S, name, actions))
		
		elif data == "deletemodule":
			mod = cd[2].lower()
			
			self.all_modules.unload_module(mod)
			os.remove(f"xioca/modules/{mod}.py")
			
			await callback.answer(self.S("mod_unloaded", mod=mod), True)
			return await callback.message.edit_text(self.S("mod_manager_text"), reply_markup=modules_kb(self, page=0))
		
		elif data == "dbsettings":
			return await callback.message.edit_text(self.S("db_menu_text"), reply_markup=dbsettings(self.S))
		
		elif data == "sqlquery":
			self.db.set("xioca.bot", "sql_status", True)
			return await callback.message.edit_text(self.S("sql_prompt"), reply_markup=back_kb(self.S))
		
		elif data == "getdb":
			await callback.answer()
			await self.bot.send_document(chat_id=callback.message.chat.id, document=FSInputFile("db.db"), caption=self.S("db_caption", date=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")))
		
		elif data == "info":
			return await callback.message.edit_text(self.S("info_text", ver=__version__), disable_web_page_preview=True, reply_markup=info_kb(self.S))

	@loader.on_bot(lambda _, m: True)
	async def watcher(self, app, message):
		status = self.db.get("xioca.bot", "sql_status", True)
		
		if not status:
			return
		
		if message.from_user.id != self.all_modules.me.id:
			return
		
		chat_id = message.from_user.id
		
		if not message.text.startswith("self.db.") and not message.text.startswith("db."):
			return await self.bot.send_message(chat_id, self.S("not_sql"))
		
		try:
			result = html.escape(str(await meval(message.text, globals(), **self.getattrs(app, message))))
		except:
			return await self.bot.send_message(chat_id, self.S("sql_error", error=html.escape(traceback.format_exc())))
		
		output = (self.S("sql_success", result=result))
		outputs = [output[i: i + 4083] for i in range(0, len(output), 4083)]
		await self.bot.send_message(chat_id, f"{outputs[0]}")
		for output in outputs[1:]:
			await self.bot.send_message(chat_id, f"<code>{output}</code>")
	
	def getattrs(self, app: Client, message: types.Message):
		return {
			"self": self,
			"db": self.db
			}
