import requests
import logging
import asyncio
import sys
import re
from typing import Union, NoReturn
from packaging import version as ver

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramAPIError, TelegramUnauthorizedError
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pyrogram import Client

from .events import Events
from .token_manager import TokenManager
from ..db import db
from .. import types, __version__, __get_version_url__, __get_commits_url__


class BotManager(Events, TokenManager):
    """Менеджер бота"""

    CRITICAL_KEYWORDS = [
        "security", "critical", "fix", "hotfix", 
        "urgent", "важно", "критично", "исправление",
        "уязвимость", "vulnerability", "фикс"
    ]

    def __init__(self, app: Client, db: db, all_modules: types.ModulesManager) -> None:
        self._app = app
        self._db = db
        self._all_modules = all_modules
        self._token = self._db.get("xioca.bot", "token", None)

    async def load(self) -> Union[bool, NoReturn]:
        """Загружает менеджер бота"""
        logging.info("Загрузка менеджера бота...")
        error_text = "Юзерботу необходим бот. Реши проблему создания бота и запускай юзербот заново"

        if not self._token:
            self._token = await self._create_bot()
            if self._token is False:
                logging.error(error_text)
                return sys.exit(1)
            self._db.set("xioca.bot", "token", self._token)

        try:
            self.bot = Bot(token=self._token, default=DefaultBotProperties(parse_mode='html'))
        except (TelegramAPIError, TelegramUnauthorizedError):
            logging.error("Неверный токен. Попытка создать новый токен...")
            result = await self._revoke_token()
            if not result:
                self._token = await self._create_bot()
                if not self._token:
                    logging.error(error_text)
                    return sys.exit(1)
                self._db.set("xioca.bot", "token", self._token)
                return await self.load()

        self._dp = Dispatcher()
        self._dp.message.register(self._message_handler)
        self._dp.inline_query.register(self._inline_handler)
        self._dp.callback_query.register(self._callback_handler)
        asyncio.create_task(self._dp.start_polling(self.bot))
        self.bot.manager = self
        
        bot_info = await self.bot.get_me()
        await self._app.unblock_user(bot_info.username)
        m = await self._app.send_message(bot_info.id, "/start")
        await m.delete()
        
        if not self._db.get("xioca.loader", "start", False):
            await self._send_start_message()
        
        await self._check_for_updates()
        
        logging.info("Менеджер бота успешно загружен")
        return True

    async def _send_start_message(self):
        """Отправляет стартовое сообщение"""
        try:
            b = InlineKeyboardButton(text="Xioca UB", url="https://t.me/XiocaUB")
            kb = InlineKeyboardBuilder()
            kb.row(b)
            await self.bot.send_message(
                self._all_modules.me.id,
                """🌙 <b>Xioca успешно установлена и уже активна на вашем аккаунте!
                
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

⭐ <i><b>Так же вы можете получить дополнительную информацию по кнопке ниже</b></i>""",
                reply_markup=kb.as_markup()
            )
            self._db.set("xioca.loader", "start", True)
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения: {e}")

    def _is_critical_update(self, commit_message: str) -> bool:
        """Проверяет, является ли обновление критическим"""
        commit_message_lower = commit_message.lower()
        return any(
            keyword in commit_message_lower
            for keyword in self.CRITICAL_KEYWORDS
        )

    async def _check_for_updates(self):
        """Проверяет наличие обновлений"""
        try:
            r = requests.get(__get_version_url__)
            match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", r.text)
            if not match:
                return

            version = match.group(1)
            if ver.parse(str(version)) == ver.parse(str(__version__)):
            	return

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
            await self.bot.send_message(self._all_modules.me.id, f"""{update_header}
Текущая версия: <code>{__version__}</code>
Новая версия: <code>{version}</code>

{chg}

🔄 Обновите командой <code>.update</code>""")
        except Exception as e:
            logging.error(f"Ошибка при проверке обновлений: {e}") 