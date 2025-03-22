import os
import re
import sys
import time
import asyncio
import atexit
import logging

from git import Repo
from git.exc import GitCommandError

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
    """Управление юзерботом"""
    
    async def restart_cmd(self, app: Client, message: types.Message, update: bool = False):
        """Перезагрузка юзербота"""
        def restart() -> None:
            """Запускает загрузку юзербота"""
            if "LAVHOST" in os.environ:
                os.system("lavhost restart")
            else:
                os.execl(sys.executable, sys.executable, "-m", "xioca")

        atexit.register(restart)
        self.db.set(
            "xioca.loader", "restart", {
                "msg": f"{message.chat.id}:{message.id}",
                "type": "restart" if not update else "update",
                "time": time.time()
            }
        )

        await utils.answer(message, "<emoji id=5462965767903396238>🔥</emoji> <b>Перезагрузка...</b>")

        logging.info("Перезагрузка...")
        return sys.exit(0)

    async def update_cmd(self, app: Client, message: types.Message):
        """Обновление юзербота"""
        await utils.answer(message, "<emoji id=5375338737028841420>🔄</emoji> <b>Обновление...</b>")

        if "LAVHOST" in os.environ:
            os.system("lavhost update")
        else:
            repo = Repo(".")
            origin = repo.remote("origin")

            try:
                origin.pull()
            except GitCommandError:
                repo.git.reset("--hard")
                return await self.update_cmd(app, message)

            pip = await asyncio.create_subprocess_exec(
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                "requirements.txt",
                "--user",
            )

            result = await pip.wait()
            if result != 0:
                await utils.answer(
                    message, "<emoji id=5210952531676504517>❌</emoji> <b>Ошибка при установке зависимостей. Подробности смотри в логах</b>")
                return sys.exit(1)

        return await self.restart_cmd(app, message, True)