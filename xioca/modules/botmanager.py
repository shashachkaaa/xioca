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
from .. import loader, utils, logger, __version__, __start_time__, __system_mod__, __get_version_url__, __get_commits_url__

back = InlineKeyboardButton(text="◀ Назад", callback_data="userbot_back")

def start_kb():
	b1 = InlineKeyboardButton(text="🎛 Управление юзерботом", callback_data="userbot_control")
	b2 = InlineKeyboardButton(text="⚙ Настройка юзербота", callback_data="userbot_settings")
	b3 = InlineKeyboardButton(text="ℹ Информация", callback_data="userbot_info")
	
	kb = InlineKeyboardBuilder()
	kb.row(b1)
	kb.row(b2)
	kb.row(b3)
	return kb.as_markup()

def control(status):
	if status:
		b1 = InlineKeyboardButton(text="🔴 Выключить юзербота", callback_data="userbot_stop")
	else:
		b1 = InlineKeyboardButton(text="🟢 Включить юзербота", callback_data="userbot_start")
	
	b2 = InlineKeyboardButton(text="🔄 Перезагрузить юзербота", callback_data="userbot_restart")
	b3 = InlineKeyboardButton(text="🆕 Проверить наличие обновлений", callback_data="userbot_checkupdate")
	b4 = InlineKeyboardButton(text="📤 Получить логи", callback_data="userbot_logs")
	
	kb = InlineKeyboardBuilder()
	kb.row(b1, b2)
	kb.row(b3)
	kb.row(b4)
	kb.row(back)
	return kb.as_markup()

def logs_kb():
	b1 = InlineKeyboardButton(text="📜 NOTSET", callback_data="userbot_logs_NOTSET")
	b2 = InlineKeyboardButton(text="🐛 DEBUG", callback_data="userbot_logs_DEBUG")
	b3 = InlineKeyboardButton(text="ℹ INFO", callback_data="userbot_logs_INFO")
	b4 = InlineKeyboardButton(text="⚠ WARNING", callback_data="userbot_logs_WARNING")
	b5 = InlineKeyboardButton(text="❌ ERROR", callback_data="userbot_logs_ERROR")
	b6 = InlineKeyboardButton(text="⛔ CRITICAL", callback_data="userbot_logs_CRITICAL")
	
	kb = InlineKeyboardBuilder()
	kb.row(b1, b2)
	kb.row(b3, b4)
	kb.row(b5, b6)
	kb.row(back)
	
	return kb.as_markup()

def settings():
	b1 = InlineKeyboardButton(text="🌙 Модульный менеджер", callback_data="userbot_modulemanager")
	b2 = InlineKeyboardButton(text="🗂 База данных", callback_data="userbot_dbsettings")
	
	kb = InlineKeyboardBuilder()
	kb.row(b1)
	kb.row(b2)
	kb.row(back)
	
	return kb.as_markup()

def dbsettings():
	b1 = InlineKeyboardButton(text="⚙ Выполнить SQL запрос", callback_data="userbot_sqlquery")
	b2 = InlineKeyboardButton(text="📤 Скачать базу данных", callback_data="userbot_getdb")
	
	kb = InlineKeyboardBuilder()
	kb.row(b1)
	kb.row(b2)
	kb.row(back)
	
	return kb.as_markup()

def back_kb():
	kb = InlineKeyboardBuilder()
	kb.row(back)
	
	return kb.as_markup()

def info_kb():
	b1 = InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/xiocaub")
	b2 = InlineKeyboardButton(text="🗃 Модули", url="https://xioca.live/mods")
	
	kb = InlineKeyboardBuilder()
	kb.row(b1, b2)
	kb.row(back)
	
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
    
    kb.row(back)
    
    return kb.as_markup()

def module_settings_kb(name, actions: bool = True):
	b1 = InlineKeyboardButton(text="🗑 Удалить", callback_data=f"userbot_deletemodule_{name}")
	
	kb = InlineKeyboardBuilder()
	if actions:
		kb.row(b1)

	kb.row(back)

	return kb.as_markup()

@loader.module("shashachkaaa", __version__)
class BotManagerMod(loader.Module):
	"""Бот менеджер. Используется для системных команд бота."""
	
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
				await asyncio.sleep(100)
			else:
				await asyncio.sleep(7200)
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
			
			response = requests.get(__get_commits_url__, params={"per_page": 1})
			response.raise_for_status()
			commits = response.json()
			
			if not commits:
				changes = ["ℹ Нет данных о последних изменениях"]
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
					f"📌 <b>Последнее изменение <code>{commit_sha[:7]}</code>:</b>",
					f"💬 <code>{commit_message}</code>"
				]
				
				if files:
					changes.append("📂 <b>Измененные файлы:</b>")
					changes.extend(f"  - <code>{file}</code>" for file in files[:5])
					if len(files) > 5:
						changes.append(f"  ... и ещё {len(files)-5} файлов")
			update_header = (
				"🚨 <b>КРИТИЧЕСКОЕ ОБНОВЛЕНИЕ!</b>\n"
				if is_critical else
				"🔔 <b>Доступна новая версия!</b>"
			)
			chg = "\n".join(changes)
			
			update_kb = InlineKeyboardBuilder()
			upd = InlineKeyboardButton(text="🔄 Установить обновление", callback_data="update")
			update_kb.row(upd)
			await self.bot.send_message(self.all_modules.me.id, f"""{update_header}
Текущая версия: <code>{__version__}</code>
Новая версия: <code>{version}</code>

{chg}""", reply_markup=update_kb.as_markup())
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
				upt = f'⌚ <b>Прошло времени с момента запуска:</b> {uptime_str}\n' if status else '\n'
				try:
					await self.bot.edit_message_text(chat_id=int(id[0]), message_id=int(id[1]), text=f"""🎛 С помощью этого меню вы сможете <b>управлять юзерботом</b>.

<b>{'🟢 Юзербот активен' if status else '🔴 Юзербот выключен'}
🌙 Установлено модулей:</b> {len(self.all_modules.modules)}
✏ <b>Префикс(ы):</b> ({prefix})
{upt}
👇 <i>Жми любую кнопку ниже что бы выполнить какое либо действие с юзерботом.</i>""", reply_markup=control(status))
				except:
					pass
		
		if not self.db.get("xioca.loader", "start", False):
			try:
				b = InlineKeyboardButton(text="Xioca UB", url="https://t.me/XiocaUB")
				kb = InlineKeyboardBuilder()
				kb.row(b)
				await self.bot.send_message(self.all_modules.me.id, """🌙 <b>Xioca успешно установлена и уже активна на вашем аккаунте!
                
ℹ Быстрый гайд по командам:</b>
<code>.help</code> - Показать все доступные команды
<code>.help</code> [команда / модуль] - Получить справку по конкретной команде.
<code>.loadmod</code> [в ответ на файл] - Загрузить модуль из файла.
<code>.unloadmod</code> [модуль] - Выгрузить модуль.
<code>.ping</code> - Проверить, работает ли бот.
<code>.restart</code> - Перезапустить бота.
<code>.update</code> - Обновить бота.
<code>.logs</code> - Получить логи бота.
<code>.terminal</code> [команда] - Выполнить команду.

⭐ <i><b>Так же вы можете получить дополнительную информацию по кнопке ниже</b></i>""", reply_markup=kb.as_markup())
				self.db.set("xioca.loader", "start", True)
			except Exception as e:
				logging.error(f"Ошибка при отправке стартового сообщения: {e}")
		asyncio.create_task(self.auto_check_update())
		await self._check_update()
		self.db.set("xioca.bot", "sql_status", False)
		logging.info(f"Менеджер по командам бота загружен!")
	
	@loader.on_bot(lambda self, app, m: m.text == "/start")
	async def start_message_handler(self, app: Client, message: Message):
		"""Меню"""
    
		if self.all_modules.me.id != message.from_user.id:
			return await message.answer("""😎 Это - <code>Xioca</code>. Отличный юзербот с большим количеством команд и модулей к нему.
			
❓ <b>Как установить?</b>
Для <b>установки</b> воспользуйтесь <a href='https://xioca.live'>сайтом</a>.

🌟 <b>Особенности:</b>
- Удобное управление через команды.
- Поддержка инлайн-режима.
- Модульная архитектура для расширения функционала.
- Регулярные обновления и поддержка.

📚 <b>Документация:</b>
Подробнее о возможностях и настройке можно узнать в <a href='https://github.com/shashachkaaa/Xioca'>документации</a>.

🛠 <b>Поддержка:</b>
Если у вас возникли вопросы, обратитесь в <a href='https://t.me/XiocaUB'>чат поддержки</a>.""")
		await message.answer(f"""👋 <b>Приветствую</b>, я - часть твоего юзербота <code>Xioca</code>, тут ты можешь найти настройки юзербота, информацию и прочее.

👇 <i>Жми любую кнопку ниже что бы узнать подробности.</i>""", reply_markup=start_kb())
	
	@loader.on_bot(lambda self, app, call: call.data.startswith("userbot_"))
	async def userbot_callback_handler(self, app, callback):
		if self.all_modules.me.id != callback.from_user.id:
			return await callback.answer(f"Кнопка не ваша!")
		
		cd = callback.data.split("_")
		data = cd[1]
		
		if data == "back":
			self.db.set("xioca.bot", "sql_status", False)
			await callback.message.delete()
			await callback.message.answer(f"""👋 <b>Приветствую</b>, я - часть твоего юзербота <code>Xioca</code>, тут ты можешь найти настройки юзербота, информацию и прочее.

👇 <i>Жми любую кнопку ниже что бы узнать подробности.</i>""", reply_markup=start_kb())
		
		elif data == "control":
			status = self.db.get("xioca.loader", "status", True)
			prefixes = self.db.get("xioca.loader", "prefixes", ["."])
			prefix = " | ".join(prefixes)
			uptime = datetime.now() - __start_time__
			uptime_str = str(uptime).split('.')[0]
			upt = f'⌚ <b>Прошло времени с момента запуска:</b> {uptime_str}\n' if status else '\n'
			
			await callback.message.edit_text(f"""🎛 С помощью этого меню вы сможете <b>управлять юзерботом</b>.

<b>{'🟢 Юзербот активен' if status else '🔴 Юзербот выключен'}
🌙 Установлено модулей:</b> {len(self.all_modules.modules)}
✏ <b>Префикс(ы):</b> ({prefix})
{upt}
👇 <i>Жми любую кнопку ниже что бы выполнить какое либо действие с юзерботом.</i>""", reply_markup=control(status))

		elif data == "stop":
			await app.stop()
			status = self.db.set("xioca.loader", "status", False)
			status = self.db.get("xioca.loader", "status", True)
			prefixes = self.db.get("xioca.loader", "prefixes", ["."])
			prefix = " | ".join(prefixes)
			uptime = datetime.now() - __start_time__
			uptime_str = str(uptime).split('.')[0]
			upt = f'\n⌚ <b>Прошло времени с момента запуска:</b> {uptime_str}\n' if status else '\n'
			
			await callback.message.edit_text(f"""🎛 С помощью этого меню вы сможете <b>управлять юзерботом</b>.

<b>{'🟢 Юзербот активен' if status else '🔴 Юзербот выключен'}
🌙 Установлено модулей:</b> {len(self.all_modules.modules)}
✏ <b>Префикс(ы):</b> ({prefix}){upt}
👇 <i>Жми любую кнопку ниже что бы выполнить какое либо действие с юзерботом.</i>""", reply_markup=control(status))

		elif data == "start":
			atexit.register(self._start)
			
			self.db.set(
				"xioca.loader", "restart", {
					"msg": f"{callback.message.chat.id}:{callback.message.message_id}",
					"type": "bot_restart",
					"time": time.time()
				}
			)
			
			await callback.answer(f"🚀 Xioca включается, ожидайте...", True)
			prefixes = self.db.get("xioca.loader", "prefixes", ["."])
			prefix = " | ".join(prefixes)
			status = self.db.get("xioca.loader", "status", True)
			await callback.message.edit_text(f"""🎛 С помощью этого меню вы сможете <b>управлять юзерботом</b>.

<b>🚀 Юзербот включается...
🌙 Установлено модулей:</b> {len(self.all_modules.modules)}
✏ <b>Префикс(ы):</b> ({prefix})

👇 <i>Жми любую кнопку ниже что бы выполнить какое либо действие с юзерботом.</i>""", reply_markup=control(status))
			sys.exit(0)
			
		elif data == "restart":
			atexit.register(self._start)
			status = self.db.get("xioca.loader", "status", True)
			
			if not status:
				return await callback.answer(f"❌ Юзербота необходимо сначала включить!")
			
			self.db.set(
				"xioca.loader", "restart", {
					"msg": f"{callback.message.chat.id}:{callback.message.message_id}",
					"type": "bot_restart",
					"time": time.time()
				}
			)
			
			status = self.db.set("xioca.loader", "status", True)
			await callback.answer(f"🔄 Xioca перезагружается, ожидайте...", True)
			prefixes = self.db.get("xioca.loader", "prefixes", ["."])
			prefix = " | ".join(prefixes)
			await callback.message.edit_text(f"""🎛 С помощью этого меню вы сможете <b>управлять юзерботом</b>.

<b>🔄 Юзербот перезагружается...
🌙 Установлено модулей:</b> {len(self.all_modules.modules)}
✏ <b>Префикс(ы):</b> ({prefix})

👇 <i>Жми любую кнопку ниже что бы выполнить какое либо действие с юзерботом.</i>""", reply_markup=control(status))
			sys.exit(0)
		
		elif data == "checkupdate":
			status = self.db.get("xioca.loader", "status", True)
			
			if not status:
				return await callback.answer(f"❌ Юзербота необходимо сначала включить!")
				
			cu = await self._check_update()
			if not cu:
				return await callback.answer(f"✅ У вас установлена последняя версия Xioca!", True)
			await callback.answer()
			
		elif data == "logs":
			if len(cd) < 3:
				await callback.message.edit_text(f'👇 Выберите уровень логов', reply_markup=logs_kb())
			else:
				lvl = logger.get_valid_level(cd[2])
				handler = logging.getLogger().handlers[0]
				logs = ("\n".join(handler.dumps(lvl))).encode("utf-8")
				if not logs:
					return await callback.answer(f"❕ Нет логов на уровне {lvl} ({logging.getLevelName(lvl)})", True)
				
				logs = io.BytesIO(logs)
				logs.name = f"xioca_{cd[2]}.txt"
				document = BufferedInputFile(logs.read(), filename=f"xioca_{cd[2]}.txt")
				await self.bot.send_document(callback.from_user.id, document=document)
				logs.close()
				await callback.answer()
				
		elif data == "settings":
			await callback.message.edit_text(f"""⚙ Это <b>меню настроек</b> Xioca. Тут можно полноценно управлять юзерботом и выполнять функции, которые не доступны в юзерботе.

👇 <i>Выберай ниже, что необходимо настроить.</i>""", reply_markup=settings())

		elif data == "modulemanager":
			await callback.message.edit_text("""🌙 Это <b>модульный менеджер</b> всех твоих модулей. Тут ты имеешь полную власть над ними. Это меню может часто пригодится при неполадках с юзерботом.

👇 <i>Выбери модуль ниже, что бы выполнить какое либо действие с ним.</i>""", reply_markup=modules_kb(self, page=0))
		
		elif data == "modulespage":
			await callback.message.edit_text("""🌙 Это <b>модульный менеджер</b> всех твоих модулей. Тут ты имеешь полную власть над ними. Это меню может часто пригодится при неполадках с юзерботом.

👇 <i>Выбери модуль ниже, что бы выполнить какое либо действие с ним.</i>""", reply_markup=modules_kb(self, page=int(cd[2])))

		elif data == "module":
			name = cd[2]
			
			if name in __system_mod__:
				actions = False
			else:
				actions = True
			
			module = self.all_modules.get_module(name)
			prefix = self.db.get("xioca.loader", "prefixes", ["."])[0]
			author = f"<b>❤️ Автор:</b> <code>{module.author}</code>\n" if module.author else ""
			vers = f"<b>0️⃣ Версия:</b> <code>{module.version}</code>\n" if module.version else ""
			desc = f"""\n<b>✍️ Описание:</b>
    ╰ {module.__doc__ or 'Нет описания для модуля'}\n"""
			
			await callback.message.edit_text(f"""<b>🌙 Модуль:</b> <code>{module.name}</code>
{author}{vers}{desc}
{'👇 <i>Выбери, какое действие выполнить с модулем.</i>' if actions else '🙅‍♂ <i>Это системный модуль, невозможно выполнить какие либо действия с ним.</i>'}""", reply_markup=module_settings_kb(name, actions))
		
		elif data == "deletemodule":
			mod = cd[2].lower()
			
			self.all_modules.unload_module(mod)
			os.remove(f"xioca/modules/{mod}.py")
			
			await callback.answer(f'✅ Модуль "{mod}" успешно выгружен!', True)
			return await callback.message.edit_text("""🌙 Это <b>модульный менеджер</b> всех твоих модулей. Тут ты имеешь полную власть над ними. Это меню может часто пригодится при неполадках с юзерботом.

👇 <i>Выбери модуль ниже, что бы выполнить какое либо действие с ним.</i>""", reply_markup=modules_kb(self, page=0))
		
		elif data == "dbsettings":
			return await callback.message.edit_text("""🗂 Это меню с настройками <b>базы данных</b> (SQLite3). Будь очень оккуратен с этим меню, одно лишнее действие может повлечь за собой очень плохие последствия.

👇 <i>Выберай следующее действие, которое необходимо выполнить.</i>""", reply_markup=dbsettings())
		
		elif data == "sqlquery":
			self.db.set("xioca.bot", "sql_status", True)
			return await callback.message.edit_text(f"""⚙ Вводи сюда SQL запрос с <b>большой осторожностью</b>. Даже одна маленькая ошибка в запросе может повлечь последствия.

ℹ Пример запроса: <code>db.get(...)</code>""", reply_markup=back_kb())
		
		elif data == "getdb":
			await callback.answer()
			await self.bot.send_document(chat_id=callback.message.chat.id, document=FSInputFile("db.db"), caption=f'🗂 <b>База данных Xioca за</b> <code>{(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")}</code>')
		
		elif data == "info":
			return await callback.message.edit_text(f"""🌙 <b>Xioca userbot</b> <code>{__version__}</code>
🧑‍💻 <b>Разработчик:</b> <a href='https://t.me/shashachkaaa'>Илья Евгеньевич</a>""", disable_web_page_preview=True, reply_markup=info_kb())

	@loader.on_bot(lambda _, m: True)
	async def watcher(self, app, message):
		status = self.db.get("xioca.bot", "sql_status", True)
		
		if not status:
			return
		
		if message.from_user.id != self.all_modules.me.id:
			return
		
		chat_id = message.from_user.id
		
		if not message.text.startswith("self.db.") and not message.text.startswith("db."):
			return await self.bot.send_message(chat_id, f"❌ <b>Это не SQL запрос!</b>")
		
		try:
			result = html.escape(str(await meval(message.text, globals(), **self.getattrs(app, message))))
		except:
			return await self.bot.send_message(chat_id, f"❌ <b>Произошла ошибка:</b> <code>{html.escape(traceback.format_exc())}</code>")
		
		output = (f"""✅ <b>SQL запрос успешно выполнен:</b>
<code>{result}</code>""")
		outputs = [output[i: i + 4083] for i in range(0, len(output), 4083)]
		await self.bot.send_message(chat_id, f"{outputs[0]}")
		for output in outputs[1:]:
			await self.bot.send_message(chat_id, f"<code>{output}</code>")
	
	def getattrs(self, app: Client, message: types.Message):
		return {
			"self": self,
			"db": self.db
			}	