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

import random
import asyncio
import logging
import re

from aiogram.types import (
    InlineQuery,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loguru import logger

from pyrogram import Client, types
from .. import loader, utils, fsm
from ..db import db

def kb(id):
	b1 = InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"giveaccess_{id}")
	b2 = InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel_{id}")
	kb = InlineKeyboardBuilder()
	kb.row(b1, b2)
	
	return kb.as_markup()

@loader.module(author="sh1tn3t | shashachkaaa")
class SettingsMod(loader.Module):
    """Настройки бота"""
    
    def __init__(self):
    	self.db = db

    async def setprefix_cmd(self, app: Client, message: types.Message, args: str):
        """Изменить префикс, можно несколько штук разделённые пробелом. Использование: setprefix <префикс> [префикс, ...]"""
        if not (args := args.split()):
            return await utils.answer(
                message, "<emoji id=5436113877181941026>❓</emoji> <b>На какой префикс нужно изменить?</b>")

        self.db.set("xioca.loader", "prefixes", list(set(args)))
        prefixes = ", ".join(f"<code>{prefix}</code>" for prefix in args)
        return await utils.answer(
            message, f"<emoji id=5206607081334906820>✔️</emoji> <b>Префикс был изменен на</b> «{prefixes}»")

    async def addalias_cmd(self, app: Client, message: types.Message, args: str):
        """Добавить алиас. Использование: addalias <новый алиас> <команда>"""
        if not (args := args.lower().split(maxsplit=1)):
            return await utils.answer(
                message, "<emoji id=5436113877181941026>❓</emoji> <b>Какой алиас нужно добавить?</b>")

        if len(args) != 2:
            return await utils.answer(
                message, "<emoji id=5210952531676504517>❌</emoji> <b>Неверно указаны аргументы."
                         "<emoji id=5206607081334906820>✔️</emoji> <b>Пример:</b> <code>addalias</code> (новый алиас) (команда)"
            )

        aliases = self.all_modules.aliases
        if args[0] in aliases:
            return await utils.answer(
                message, "<emoji id=5210952531676504517>❌</emoji> <b>Такой алиас уже существует</b>")

        if not self.all_modules.command_handlers.get(args[1]):
            return await utils.answer(
                message, "<emoji id=5210952531676504517>❌</emoji> <b>Такой команды нет</b>")

        aliases[args[0]] = args[1]
        self.db.set("xioca.loader", "aliases", aliases)

        return await utils.answer(
            message, f"<emoji id=5206607081334906820>✔️</emoji> <b>Алиас</b> «<code>{args[0]}</code>» <b>для команды</b> «<code>{args[1]}</code>» <b>был добавлен</b>")

    async def delalias_cmd(self, app: Client, message: types.Message, args: str):
        """Удалить алиас. Использование: delalias <алиас>"""
        if not (args := args.lower()):
            return await utils.answer(
                message, "<emoji id=5210952531676504517>❌</emoji> <b>Какой алиас нужно удалить?</b>")

        aliases = self.all_modules.aliases
        if args not in aliases:
            return await utils.answer(
                message, "<emoji id=5210952531676504517>❌</emoji> <b>Такого алиаса нет</b>")

        del aliases[args]
        self.db.set("xioca.loader", "aliases", aliases)

        return await utils.answer(
            message, f"<emoji id=5206607081334906820>✔️</emoji> <b>Алиас</b> «<code>{args}</code>» <b>был удален</b>")

    async def aliases_cmd(self, app: Client, message: types.Message):
        """Показать все алиасы"""
        aliases = self.all_modules.aliases
        if not aliases:
            return await utils.answer(
                message, "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Алиасы отсутствуют</b>")

        return await utils.answer(
            message, "<emoji id=5956561916573782596>📄</emoji> <b>Список всех алиасов:</b>\n" + "\n".join(
                f"<emoji id=4972281662894244560>🛑</emoji> <code>{alias}</code> ➜ <code>{command}</code>"
                for alias, command in aliases.items()
            )
        )

    async def hidemod_cmd(self, app: Client, message: types.Message, args: str):
        """Скрыть модуль. Использование: hidemod <название модуля>"""
        if not args:
            return await utils.answer(
                message, "<emoji id=5436113877181941026>❓</emoji> <b>Какой модуль нужно скрыть?</b>"
            )

        module_name = args.lower()
        hide_mods = self.db.get("help", "hide_mods", [])
        
        all_modules = [module.name.lower() for module in self.all_modules.modules]
        
        module_name, text = utils.find_closest_module_name(module_name, all_modules)
        
        if module_name in hide_mods:
            return await utils.answer(
                message, f"<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{module_name}</code>» <b>уже скрыт</b>\n\n{text}"
            )

        hide_mods.append(module_name)
        self.db.set("help", "hide_mods", hide_mods)

        return await utils.answer(
            message, f"<emoji id=5206607081334906820>✔️</emoji> <b>Модуль</b> «<code>{module_name}</code>» <b>скрыт</b>\n\n{text}"
        )

    async def showmod_cmd(self, app: Client, message: types.Message, args: str):
        """Показать скрытый модуль. Использование: showmod <название модуля>"""
        if not args:
            return await utils.answer(
                message, "<emoji id=5436113877181941026>❓</emoji> <b>Какой модуль нужно показать?</b>"
            )

        module_name = args.lower()
        hide_mods = self.db.get("help", "hide_mods", [])
        
        all_modules = [module.name.lower() for module in self.all_modules.modules]
        
        module_name, text = utils.find_closest_module_name(module_name, all_modules)
        
        if module_name not in hide_mods:
            return await utils.answer(
                message, f"<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{module_name}</code>» <b>не скрыт</b>\n\n{text}"
            )

        hide_mods.remove(module_name)
        self.db.set("help", "hide_mods", hide_mods)

        return await utils.answer(
            message, f"<emoji id=5206607081334906820>✔️</emoji> <b>Модуль</b> «<code>{module_name}</code>» <b>теперь виден</b>\n\n{text}"
        )

    async def hiddenmods_cmd(self, app: Client, message: types.Message):
        """Показать список скрытых модулей. Использование: hiddenmods"""
        hide_mods = self.db.get("help", "hide_mods", [])
        
        if not hide_mods:
            return await utils.answer(
                message, "<emoji id=5463044060862244442>🤷‍♂</emoji> <b>Скрытых модулей нет</b>"
            )

        return await utils.answer(
            message, "<emoji id=5956561916573782596>📄</emoji> <b>Список скрытых модулей:</b>\n" + "\n".join(
                f"<emoji id=4972281662894244560>🛑</emoji> <code>{module}</code>"
                for module in hide_mods
            )
        )

    async def setinline_cmd(self, app: Client, message: types.Message, args):
    	"""Сменить юзернейм инлайн бота"""
    	
    	if not args:
    		return await utils.answer(message, "<emoji id=5436113877181941026>❓</emoji> <b>Укажите новый юзернейм для бота.</b>")
    	name = args.strip().lower()
    	if not re.match(r"^[a-zA-Z0-9_]{5,}bot$", name):
    		return await utils.answer(message, "<emoji id=5210952531676504517>❌</emoji> <b>Некорректный юзернейм. Юзернейм должен содержать только буквы, цифры, подчеркивания, иметь окончание «Bot» и быть длиной не менее 5 символов.</b>")
    	
    	await utils.answer(message, "<emoji id=5195083327597456039>🌙</emoji> <b>Создаю нового бота...</b>")
    	
    	async with fsm.Conversation(app, "@BotFather", True) as conv:
    		try:
    			await conv.ask("/cancel")
    		except errors.UserIsBlocked:
    			await app.unblock_user("@BotFather")
    		
    		await conv.get_response()
    		await asyncio.sleep(5)
    		
    		await conv.ask("/newbot")
    		response = await conv.get_response()
    		
    		if not all(phrase not in response.text for phrase in ["That I cannot do.", "Sorry"]):
    			return await utils.answer(message, f"<emoji id=5210952531676504517>❌</emoji> <b>Не удалось создать нового бота. Ответ @BotFather:</b> <code>{response.text}</code>")
    		await asyncio.sleep(5)
    		
    		await utils.answer(message, "<emoji id=5195083327597456039>🌙</emoji> <b>Настраиваю имя бота...</b>")
    		await conv.ask(f"Xioca of {utils.get_display_name(self.all_modules.me)[:45]}")
    		await conv.get_response()
    		await asyncio.sleep(5)
    		
    		await conv.ask(args)
    		response = await conv.get_response()
    		
    		search = re.search(r"(?<=<code>)(.*?)(?=</code>)", response.text.html)
    		if not search:
    			return await utils.answer(message, "<emoji id=5210952531676504517>❌</emoji> <b>Не удалось создать нового бота. Ответ @BotFather:</b> <code>{response.text}</code>")
    		
    		token = search.group(0)
    		
    		await utils.answer(message, "<emoji id=5195083327597456039>🌙</emoji> <b>Настраиваю аватарку бота...</b>")
    		await conv.ask("/setuserpic")
    		await conv.get_response()
    		await asyncio.sleep(5)
    		
    		await conv.ask("@" + args)
    		await conv.get_response()
    		await asyncio.sleep(5)
    		
    		await conv.ask_media(random.choice(["bot_avatar1.png", "bot_avatar2.png", "bot_avatar3.png"]), media_type="photo")
    		await conv.get_response()
    		await asyncio.sleep(5)
    		
    		await utils.answer(message, "<emoji id=5195083327597456039>🌙</emoji> <b>Настраиваю инлайн...</b>")
    		await conv.ask("/setinline")
    		await conv.get_response()
    		await asyncio.sleep(5)
    		
    		await utils.answer(message, "<emoji id=5195083327597456039>🌙</emoji> <b>Обновляю юзернейм бота...</b>")
    		await conv.ask("@" + args)
    		await conv.get_response()
    		await asyncio.sleep(5)
    		
    		await utils.answer(message, "<emoji id=5195083327597456039>🌙</emoji> <b>Снова настраиваю инлайн...</b>")
    		await conv.ask("xioca  команда")
    		await conv.get_response()
    		
    		logger.success("Бот успешно создан")
    		
    		self.db.set("xioca.bot", "token", token)
    		await utils.answer(message, f"<emoji id=5206607081334906820>✔️</emoji> <b>Инлайн бот <code>@{name}</code> успешно создан! Необходима перезагрузка для применения изменений</b>")
    	
    
    async def ownerlist_cmd(self, app: Client, message: types.Message):
    	"""Список пользователей, имеющих доступ к юзерботу"""
    	
    	ids = self.db.get("xioca.loader", "allow", [])
    	
    	if not ids:
    		return await utils.answer(message, f"<emoji id=5210956306952758910>👀</emoji> <b>Никто не имеет доступ к вашему юзерботу!</b>")
    	
    	make = str.maketrans({
    		'1': '<emoji id=5381828389663431280>1️⃣</emoji>',
    		'2': '<emoji id=5382051178207007027>2️⃣</emoji>',
    		'3': '<emoji id=5379910025340802255>3️⃣</emoji>',
    		'4': '<emoji id=5388624247696412237>4️⃣</emoji>',
    		'5': '<emoji id=5390859675094766802>5️⃣</emoji>',
    		'6': '<emoji id=5388691197646625260>6️⃣</emoji>',
    		'7': '<emoji id=5391035158868547187>7️⃣</emoji>',
    		'8': '<emoji id=5388710159927236114>8️⃣</emoji>',
    		'9': '<emoji id=5391071623140889606>9️⃣</emoji>',
    		'0': '<emoji id=5381817669425058178>0️⃣</emoji>'
    	})
    	
    	text = ""
    	num = 0
    	
    	for id in ids:
    		num += 1
    		try:
    			name = (await app.get_users(id)).first_name
    		except:
    			name = "Пользователь"
    		
    		text += f"{num} <a href='tg://user?id={id}'>{name}</a>\n"
    	
    	text = text.translate(make)
    	
    	await utils.answer(message, f"<emoji id=5251203410396458957>🛡</emoji> <b>Всего <code>{num}</code> пользователей имеют доступ к вашему юзерботу</b>\n\n{text}")
    
    async def ownerrm_cmd(self, app: Client, message: types.Message, args: str):
    	"""Отнять доступ к юзерботу"""
    	r = message.reply_to_message
    	
    	if not r:
    		if not args:
    			return await utils.answer(message, f"<emoji id=5210952531676504517>❌</emoji> <b>Необходим ответ на сообщение, ID или username пользователя!</b>")
    		else:
    			args = args.split()
    			if isinstance(args[0], str):
    				id = args[0].replace("@", "")
    				id = (await app.get_users(id)).id
    				name = (await app.get_users(id)).first_name
    			else:
    				id = int(args[0])
    				name = (await app.get_users(id)).first_name
    	else:
    		id = r.from_user.id
    		name = r.from_user.first_name
    	
    	if self.all_modules.me.id == id:
    		return await utils.answer(message, "<emoji id=5210952531676504517>❌</emoji> <b>Данную команду невозможно выполнить на самом себе!</b>")
    	
    	ids = self.db.get("xioca.loader", "allow", [])
    	if id not in ids:
    		return await utils.answer(message, f"<emoji id=5210952531676504517>❌</emoji> <b>У пользователя нет доступа к юзерботу!</b>")
    	
    	ids.remove(id)
    	self.db.set("xioca.loader", "allow", ids)
    	
    	await utils.answer(message, f"<emoji id=5206607081334906820>✔️</emoji> <b>Права на юзербота у <a href='tg://user?id={id}'>{name}</a> успешно отняты!</b>")

    async def owneradd_cmd(self, app: Client, message: types.Message):
    	"""Предоставить доступ к юзерботу"""
    	
    	r = message.reply_to_message
    	
    	if not r:
    		return await utils.answer(message, f"<emoji id=5210952531676504517>❌</emoji> <b>Необходим ответ на сообщение</b>")
    	
    	if self.all_modules.me.id == r.from_user.id:
    		return await utils.answer(message, "<emoji id=5210952531676504517>❌</emoji> <b>Данную команду невозможно выполнить на самом себе!</b>")
    	
    	bot_results = await app.get_inline_bot_results((await self.bot.me()).username, f"owneradd {r.from_user.id}")
    	
    	await app.send_inline_bot_result(message.chat.id, bot_results.query_id, bot_results.results[0].id)
    	return await message.delete()
    
    @loader.on_bot(lambda self, app, inline_query: True)
    async def owneradd_inline_handler(self, app: Client, inline_query: InlineQuery):
    	"""Предоставить доступ к юзерботу"""
    	
    	args = inline_query.query.split()
    	
    	if len(args) < 2:
    		return await inline_query.answer([], cache_time=0)
    	
    	message_id = utils.random_id()
    	id = int(args[1])
    	name = (await app.get_users(id)).first_name
    	
    	message = InputTextMessageContent(message_text=f"🛡 <b>Вы уверены что хотите предоставить доступ к юзерботу <a href='tg://user?id={id}'>{name}</a>?</b> Он(а) получит доступ ко всем командам вашей Xioca, это может повлечь за собой плохие последствия. Решение может быть принято на ваш страх и риск!")
    	
    	msg = await inline_query.answer([InlineQueryResultArticle(id=message_id, title="🛡 Отправить подтверждение", input_message_content=message, reply_markup=kb(id))], cache_time=0)
    	
    @loader.on_bot(lambda self, app, call: call.data.startswith("giveaccess_"))
    async def giveaccess_callback_handler(self, app: Client, call: CallbackQuery):
    	"""Подтверждение"""
    	
    	cd = call.data.split("_")
    	id = int(cd[1])
    	
    	if call.from_user.id != self.all_modules.me.id:
    		return await call.answer("❗ Эта кнопка не ваша!", True)

    	ids = self.db.get("xioca.loader", "allow", [])
    	ids.append(id)
    	self.db.set("xioca.loader", "allow", ids)
    	name = (await app.get_users(id)).first_name
    	await self.bot.edit_message_text(inline_message_id=call.inline_message_id, text=f"✅ <b>Доступ <a href='tg://user?id={id}'>{name}</a> предоставлен!</b>")
    
    @loader.on_bot(lambda self, app, call: call.data.startswith("cancel"))
    async def cancel_callback_handler(self, app: Client, call: CallbackQuery):
    	"""Отказ"""
    	
    	cd = call.data.split("_")
    	id = int(cd[1])
    	
    	if call.from_user.id != self.all_modules.me.id:
    		return await call.answer("❗ Эта кнопка не ваша!", True)
    		
    	name = (await app.get_users(id)).first_name
    	await self.bot.edit_message_text(inline_message_id=call.inline_message_id, text=f"❌ <b>Отказано в доступе для <a href='tg://user?id={id}'>{name}</a>!</b>")