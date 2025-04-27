import os
import re
import sys
import time
import asyncio
import atexit
import logging
from pathlib import Path

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

from aiogram.types import (
    InlineQuery,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from pyrogram import Client, types
from .. import loader, utils

VALID_URL = r"[-[\]_.~:/?#@!$&'()*+,;%<=>a-zA-Z0-9]+"
VALID_PIP_PACKAGES = re.compile(
    r"^\s*# required:(?: ?)((?:{url} )*(?:{url}))\s*$".format(url=VALID_URL),
    re.MULTILINE,
)
GIT_REGEX = re.compile(
    r"^https?://github\.com((?:/[a-z0-9-]+){2})(?:/tree/([a-z0-9-]+)((?:/[a-z0-9-]+)*))?/?$",
    flags=re.IGNORECASE,
)

@loader.module(name="Updater", author="shashachkaaa")
class UpdaterMod(loader.Module):
    """Управление обновлениями и перезагрузкой юзербота"""

    async def restart_cmd(self, app: Client, message: types.Message, update: bool = False):
        """Перезагрузить юзербота. Использование: restart"""
        try:
            def restart():
                """Функция для перезагрузки"""
                if "LAVHOST" in os.environ:
                    os.system("lavhost restart")
                else:
                    os.execl(sys.executable, sys.executable, "-m", "xioca")

            atexit.register(restart)
            self.db.set(
                "xioca.restart", "restart", {
                    "msg": f"{message.chat.id}:{message.id}",
                    "type": "restart" if not update else "update",
                    "time": time.time()
                }
            )
            if message.from_user.is_premium:
            	restart_text = "<b>Ваша <emoji id=5199885066674661599>🌙</emoji><emoji id=5199427893175807183>🌙</emoji><emoji id=5199518289352486689>🌙</emoji> перезагружается...</b>"
            else:
            	restart_text = "<b>🌙 Xioca перезагружается...</b>"
            	
            await utils.answer(message, restart_text)
            logging.info("Инициирована перезагрузка юзербота")
            sys.exit(0)
            
        except Exception as e:
            logging.exception(f"Ошибка при перезагрузке: {e}")
            await utils.answer(
                message, 
                "<emoji id=5210952531676504517>❌</emoji> <b>Ошибка при перезагрузке. Проверьте логи</b>"
            )

    async def update_cmd(self, app: Client, message: types.Message, calldata = False):
        """Обновить юзербота. Использование: update"""
        if calldata:
        	message = await app.send_message(self.bot.id, "<emoji id=5375338737028841420>🔄</emoji>")
        
        try:
            await utils.answer(message, "<emoji id=5375338737028841420>🔄</emoji> <b>Проверка обновлений...</b>")

            if "LAVHOST" in os.environ:
                os.system("lavhost update")
                return await self.restart_cmd(app, message, True)

            repo_path = Path(".").absolute()
            
            try:
                repo = Repo(repo_path)
            except InvalidGitRepositoryError:
                return await utils.answer(
                    message,
                    "<emoji id=5210952531676504517>❌</emoji> <b>Текущая директория не является git репозиторием</b>"
                )

            origin = repo.remote("origin")
            current_hash = repo.head.commit.hexsha

            repo.git.reset("--hard")
            
            try:
                origin.fetch()
                new_hash = repo.commit("origin/main" if "main" in repo.heads else "origin/master").hexsha
                
                if current_hash == new_hash:
                    return await utils.answer(
                        message,
                        "<emoji id=5206607081334906820>✔️</emoji> <b>У вас уже установлена последняя версия</b>"
                    )

                repo.git.reset("--hard", "origin/main" if "main" in repo.heads else "origin/master")

            except GitCommandError as e:
                logging.error(f"Git error: {e}")
                return await utils.answer(
                    message,
                    "<emoji id=5210952531676504517>❌</emoji> <b>Ошибка при получении обновлений. Проверьте логи</b>"
                )

            await utils.answer(message, "<emoji id=5375338737028841420>🔄</emoji> <b>Установка зависимостей...</b>")
            
            requirements = repo_path / "requirements.txt"
            if requirements.exists():
                pip = await asyncio.create_subprocess_exec(
                    sys.executable, "-m", "pip", "install", "-r", str(requirements), "--user",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await pip.communicate()
                
                if pip.returncode != 0:
                    error_msg = stderr.decode().strip() if stderr else "Unknown error"
                    logging.error(f"Ошибка установки зависимостей: {error_msg}")
                    return await utils.answer(
                        message,
                        "<emoji id=5210952531676504517>❌</emoji> <b>Ошибка установки зависимостей. Проверьте логи</b>"
                    )

            return await self.restart_cmd(app, message, True)

        except Exception as e:
            logging.exception(f"Ошибка при обновлении: {e}")
            await utils.answer(
                message,
                "<emoji id=5210952531676504517>❌</emoji> <b>Критическая ошибка при обновлении. Проверьте логи</b>"
            )

    async def version_cmd(self, app: Client, message: types.Message):
        """Показать версию юзербота. Использование: version"""
        try:
            repo = Repo(Path(".").absolute())
            commit = repo.head.commit
            version = commit.hexsha[:7]
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(commit.committed_date))
            author = commit.author.name
            
            await utils.answer(
                message,
                f"<emoji id=5226929552319594190>ℹ️</emoji> <b>Версия юзербота:</b>\n\n"
                f"<b>Хэш:</b> <code>{version}</code>\n"
                f"<b>Дата:</b> <code>{date}</code>\n"
                f"<b>Автор:</b> <code>{author}</code>\n"
            )
        except Exception as e:
            logging.exception(f"Ошибка получения версии: {e}")
            await utils.answer(
                message,
                "<emoji id=5210952531676504517>❌</emoji> <b>Не удалось получить информацию о версии</b>"
            )
    
    @loader.on_bot(lambda self, app, call: call.data == "update")
    async def update_callback_handler(self, app: Client, call: CallbackQuery):
    	"""Обновление по кнопке"""
    	message = types.Message(
        	id=call.message.message_id,
        	chat=call.message.chat,
        	from_user=call.from_user,
        	date=call.message.date,
        	client=app
    	)
    	
    	await call.answer(f"🔄 Обновляюсь...")
    	
    	await self.update_cmd(app, message, True)