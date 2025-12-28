# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

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

@loader.module(author="shashachkaaa")
class UpdaterMod(loader.Module):
    """Управление обновлениями и перезагрузкой юзербота"""

    strings = {
        "ru": {
            "restart_premium": "<b>Ваша <emoji id=5199885066674661599>🌙</emoji><emoji id=5199427893175807183>🌙</emoji><emoji id=5199518289352486689>🌙</emoji> перезагружается...</b>",
            "restart_normal": "<b>🌙 Xioca перезагружается...</b>",
            "restart_error": "<emoji id=5210952531676504517>❌</emoji> <b>Ошибка при перезагрузке. Проверьте логи</b>",
            "update_emoji": "<emoji id=5375338737028841420>🔄</emoji>",
            "checking_updates": "<emoji id=5375338737028841420>🔄</emoji> <b>Проверка обновлений...</b>",
            "no_git_repo": "<emoji id=5210952531676504517>❌</emoji> <b>Текущая директория не является git репозиторием</b>",
            "already_latest": "<emoji id=5206607081334906820>✔️</emoji> <b>У вас уже установлена последняя версия</b>",
            "fetch_error": "<emoji id=5210952531676504517>❌</emoji> <b>Ошибка при получении обновлений. Проверьте логи</b>",
            "installing_deps": "<emoji id=5375338737028841420>🔄</emoji> <b>Установка зависимостей...</b>",
            "deps_error": "<emoji id=5210952531676504517>❌</emoji> <b>Ошибка установки зависимостей. Проверьте логи</b>",
            "critical_update_error": "<emoji id=5210952531676504517>❌</emoji> <b>Критическая ошибка при обновлении. Проверьте логи</b>",
            "version_info": (
                "<emoji id=5226929552319594190>ℹ️</emoji> <b>Версия юзербота:</b>\n\n"
                "<b>Хэш:</b> <code>{version}</code>\n"
                "<b>Дата:</b> <code>{date}</code>\n"
                "<b>Автор:</b> <code>{author}</code>\n"
            ),
            "version_error": "<emoji id=5210952531676504517>❌</emoji> <b>Не удалось получить информацию о версии</b>",
            "updating_alert": "🔄 Обновляюсь..."
        },
        "en": {
            "restart_premium": "<b>Your <emoji id=5199885066674661599>🌙</emoji><emoji id=5199427893175807183>🌙</emoji><emoji id=5199518289352486689>🌙</emoji> is restarting...</b>",
            "restart_normal": "<b>🌙 Xioca is restarting...</b>",
            "restart_error": "<emoji id=5210952531676504517>❌</emoji> <b>Error during restart. Check logs</b>",
            "update_emoji": "<emoji id=5375338737028841420>🔄</emoji>",
            "checking_updates": "<emoji id=5375338737028841420>🔄</emoji> <b>Checking for updates...</b>",
            "no_git_repo": "<emoji id=5210952531676504517>❌</emoji> <b>Current directory is not a git repository</b>",
            "already_latest": "<emoji id=5206607081334906820>✔️</emoji> <b>You already have the latest version</b>",
            "fetch_error": "<emoji id=5210952531676504517>❌</emoji> <b>Error fetching updates. Check logs</b>",
            "installing_deps": "<emoji id=5375338737028841420>🔄</emoji> <b>Installing dependencies...</b>",
            "deps_error": "<emoji id=5210952531676504517>❌</emoji> <b>Error installing dependencies. Check logs</b>",
            "critical_update_error": "<emoji id=5210952531676504517>❌</emoji> <b>Critical error during update. Check logs</b>",
            "version_info": (
                "<emoji id=5226929552319594190>ℹ️</emoji> <b>Userbot version:</b>\n\n"
                "<b>Hash:</b> <code>{version}</code>\n"
                "<b>Date:</b> <code>{date}</code>\n"
                "<b>Author:</b> <code>{author}</code>\n"
            ),
            "version_error": "<emoji id=5210952531676504517>❌</emoji> <b>Failed to get version info</b>",
            "updating_alert": "🔄 Updating..."
        },
        "be": {
            "restart_premium": "<b>Ваша <emoji id=5199885066674661599>🌙</emoji><emoji id=5199427893175807183>🌙</emoji><emoji id=5199518289352486689>🌙</emoji> перазагружаецца...</b>",
            "restart_normal": "<b>🌙 Xioca перазагружаецца...</b>",
            "restart_error": "<emoji id=5210952531676504517>❌</emoji> <b>Памылка пры перазагрузцы. Праверце логі</b>",
            "update_emoji": "<emoji id=5375338737028841420>🔄</emoji>",
            "checking_updates": "<emoji id=5375338737028841420>🔄</emoji> <b>Праверка абнаўленняў...</b>",
            "no_git_repo": "<emoji id=5210952531676504517>❌</emoji> <b>Бягучая дырэкторыя не з'яўляецца git-рэпазіторыем</b>",
            "already_latest": "<emoji id=5206607081334906820>✔️</emoji> <b>У вас ужо ўсталявана апошняя версія</b>",
            "fetch_error": "<emoji id=5210952531676504517>❌</emoji> <b>Памылка пры атрыманні абнаўленняў. Праверце логі</b>",
            "installing_deps": "<emoji id=5375338737028841420>🔄</emoji> <b>Усталяванне залежнасцяў...</b>",
            "deps_error": "<emoji id=5210952531676504517>❌</emoji> <b>Памылка ўсталявання залежнасцяў. Праверце логі</b>",
            "critical_update_error": "<emoji id=5210952531676504517>❌</emoji> <b>Крытычная памылка пры абнаўленні. Праверце логі</b>",
            "version_info": (
                "<emoji id=5226929552319594190>ℹ️</emoji> <b>Версія юзербота:</b>\n\n"
                "<b>Хэш:</b> <code>{version}</code>\n"
                "<b>Дата:</b> <code>{date}</code>\n"
                "<b>Аўтар:</b> <code>{author}</code>\n"
            ),
            "version_error": "<emoji id=5210952531676504517>❌</emoji> <b>Не атрымалася даведацца інфармацыю пра версію</b>",
            "updating_alert": "🔄 Абнаўляюся..."
        },
        "de": {
            "restart_premium": "<b>Ihr <emoji id=5199885066674661599>🌙</emoji><emoji id=5199427893175807183>🌙</emoji><emoji id=5199518289352486689>🌙</emoji> startet neu...</b>",
            "restart_normal": "<b>🌙 Xioca startet neu...</b>",
            "restart_error": "<emoji id=5210952531676504517>❌</emoji> <b>Fehler beim Neustart. Protokolle prüfen</b>",
            "update_emoji": "<emoji id=5375338737028841420>🔄</emoji>",
            "checking_updates": "<emoji id=5375338737028841420>🔄</emoji> <b>Suche nach Updates...</b>",
            "no_git_repo": "<emoji id=5210952531676504517>❌</emoji> <b>Das aktuelle Verzeichnis ist kein Git-Repository</b>",
            "already_latest": "<emoji id=5206607081334906820>✔️</emoji> <b>Sie haben bereits die neueste Version</b>",
            "fetch_error": "<emoji id=5210952531676504517>❌</emoji> <b>Fehler beim Abrufen von Updates. Protokolle prüfen</b>",
            "installing_deps": "<emoji id=5375338737028841420>🔄</emoji> <b>Abhängigkeiten werden installiert...</b>",
            "deps_error": "<emoji id=5210952531676504517>❌</emoji> <b>Fehler beim Installieren von Abhängigkeiten. Protokolle prüfen</b>",
            "critical_update_error": "<emoji id=5210952531676504517>❌</emoji> <b>Kritischer Fehler beim Update. Protokolle prüfen</b>",
            "version_info": (
                "<emoji id=5226929552319594190>ℹ️</emoji> <b>Userbot-Version:</b>\n\n"
                "<b>Hash:</b> <code>{version}</code>\n"
                "<b>Datum:</b> <code>{date}</code>\n"
                "<b>Autor:</b> <code>{author}</code>\n"
            ),
            "version_error": "<emoji id=5210952531676504517>❌</emoji> <b>Fehler beim Abrufen der Versionsinfo</b>",
            "updating_alert": "🔄 Update läuft..."
        },
        "es": {
            "restart_premium": "<b>Tu <emoji id=5199885066674661599>🌙</emoji><emoji id=5199427893175807183>🌙</emoji><emoji id=5199518289352486689>🌙</emoji> se está reiniciando...</b>",
            "restart_normal": "<b>🌙 Xioca se está reiniciando...</b>",
            "restart_error": "<emoji id=5210952531676504517>❌</emoji> <b>Error al reiniciar. Revisa los registros</b>",
            "update_emoji": "<emoji id=5375338737028841420>🔄</emoji>",
            "checking_updates": "<emoji id=5375338737028841420>🔄</emoji> <b>Buscando actualizaciones...</b>",
            "no_git_repo": "<emoji id=5210952531676504517>❌</emoji> <b>El directorio actual no es un repositorio git</b>",
            "already_latest": "<emoji id=5206607081334906820>✔️</emoji> <b>Ya tienes la última versión</b>",
            "fetch_error": "<emoji id=5210952531676504517>❌</emoji> <b>Error al obtener actualizaciones. Revisa los registros</b>",
            "installing_deps": "<emoji id=5375338737028841420>🔄</emoji> <b>Instalando dependencias...</b>",
            "deps_error": "<emoji id=5210952531676504517>❌</emoji> <b>Error instalando dependencias. Revisa los registros</b>",
            "critical_update_error": "<emoji id=5210952531676504517>❌</emoji> <b>Error crítico durante la actualización. Revisa los registros</b>",
            "version_info": (
                "<emoji id=5226929552319594190>ℹ️</emoji> <b>Versión del userbot:</b>\n\n"
                "<b>Hash:</b> <code>{version}</code>\n"
                "<b>Fecha:</b> <code>{date}</code>\n"
                "<b>Autor:</b> <code>{author}</code>\n"
            ),
            "version_error": "<emoji id=5210952531676504517>❌</emoji> <b>No se pudo obtener la información de la versión</b>",
            "updating_alert": "🔄 Actualizando..."
        },
        "fr": {
            "restart_premium": "<b>Votre <emoji id=5199885066674661599>🌙</emoji><emoji id=5199427893175807183>🌙</emoji><emoji id=5199518289352486689>🌙</emoji> redémarre...</b>",
            "restart_normal": "<b>🌙 Xioca redémarre...</b>",
            "restart_error": "<emoji id=5210952531676504517>❌</emoji> <b>Erreur lors du redémarrage. Vérifiez les logs</b>",
            "update_emoji": "<emoji id=5375338737028841420>🔄</emoji>",
            "checking_updates": "<emoji id=5375338737028841420>🔄</emoji> <b>Recherche de mises à jour...</b>",
            "no_git_repo": "<emoji id=5210952531676504517>❌</emoji> <b>Le répertoire actuel n'est pas un dépôt git</b>",
            "already_latest": "<emoji id=5206607081334906820>✔️</emoji> <b>Vous avez déjà la dernière version</b>",
            "fetch_error": "<emoji id=5210952531676504517>❌</emoji> <b>Erreur lors de la récupération des mises à jour. Vérifiez les logs</b>",
            "installing_deps": "<emoji id=5375338737028841420>🔄</emoji> <b>Installation des dépendances...</b>",
            "deps_error": "<emoji id=5210952531676504517>❌</emoji> <b>Erreur d'installation des dépendances. Vérifiez les logs</b>",
            "critical_update_error": "<emoji id=5210952531676504517>❌</emoji> <b>Erreur critique lors de la mise à jour. Vérifiez les logs</b>",
            "version_info": (
                "<emoji id=5226929552319594190>ℹ️</emoji> <b>Version du userbot :</b>\n\n"
                "<b>Hash :</b> <code>{version}</code>\n"
                "<b>Date :</b> <code>{date}</code>\n"
                "<b>Auteur :</b> <code>{author}</code>\n"
            ),
            "version_error": "<emoji id=5210952531676504517>❌</emoji> <b>Impossible d'obtenir les infos de version</b>",
            "updating_alert": "🔄 Mise à jour..."
        },
        "it": {
            "restart_premium": "<b>Il tuo <emoji id=5199885066674661599>🌙</emoji><emoji id=5199427893175807183>🌙</emoji><emoji id=5199518289352486689>🌙</emoji> si sta riavviando...</b>",
            "restart_normal": "<b>🌙 Xioca si sta riavviando...</b>",
            "restart_error": "<emoji id=5210952531676504517>❌</emoji> <b>Errore durante il riavvio. Controlla i log</b>",
            "update_emoji": "<emoji id=5375338737028841420>🔄</emoji>",
            "checking_updates": "<emoji id=5375338737028841420>🔄</emoji> <b>Controllo aggiornamenti...</b>",
            "no_git_repo": "<emoji id=5210952531676504517>❌</emoji> <b>La directory corrente non è un repository git</b>",
            "already_latest": "<emoji id=5206607081334906820>✔️</emoji> <b>Hai già l'ultima versione</b>",
            "fetch_error": "<emoji id=5210952531676504517>❌</emoji> <b>Errore durante il recupero degli aggiornamenti. Controlla i log</b>",
            "installing_deps": "<emoji id=5375338737028841420>🔄</emoji> <b>Installazione delle dipendenze...</b>",
            "deps_error": "<emoji id=5210952531676504517>❌</emoji> <b>Errore installazione dipendenze. Controlla i log</b>",
            "critical_update_error": "<emoji id=5210952531676504517>❌</emoji> <b>Errore critico durante l'aggiornamento. Controlla i log</b>",
            "version_info": (
                "<emoji id=5226929552319594190>ℹ️</emoji> <b>Versione userbot:</b>\n\n"
                "<b>Hash:</b> <code>{version}</code>\n"
                "<b>Data:</b> <code>{date}</code>\n"
                "<b>Autore:</b> <code>{author}</code>\n"
            ),
            "version_error": "<emoji id=5210952531676504517>❌</emoji> <b>Impossibile ottenere informazioni sulla versione</b>",
            "updating_alert": "🔄 Aggiornamento in corso..."
        },
        "kk": {
            "restart_premium": "<b>Сіздің <emoji id=5199885066674661599>🌙</emoji><emoji id=5199427893175807183>🌙</emoji><emoji id=5199518289352486689>🌙</emoji> қайта қосылуда...</b>",
            "restart_normal": "<b>🌙 Xioca қайта қосылуда...</b>",
            "restart_error": "<emoji id=5210952531676504517>❌</emoji> <b>Қайта қосу қатесі. Логтарды тексеріңіз</b>",
            "update_emoji": "<emoji id=5375338737028841420>🔄</emoji>",
            "checking_updates": "<emoji id=5375338737028841420>🔄</emoji> <b>Жаңартуларды тексеру...</b>",
            "no_git_repo": "<emoji id=5210952531676504517>❌</emoji> <b>Ағымдағы каталог git репозиторийі емес</b>",
            "already_latest": "<emoji id=5206607081334906820>✔️</emoji> <b>Сізде ең соңғы нұсқа орнатылған</b>",
            "fetch_error": "<emoji id=5210952531676504517>❌</emoji> <b>Жаңартуларды алу қатесі. Логтарды тексеріңіз</b>",
            "installing_deps": "<emoji id=5375338737028841420>🔄</emoji> <b>Тәуелділіктерді орнату...</b>",
            "deps_error": "<emoji id=5210952531676504517>❌</emoji> <b>Тәуелділіктерді орнату қатесі. Логтарды тексеріңіз</b>",
            "critical_update_error": "<emoji id=5210952531676504517>❌</emoji> <b>Жаңарту кезіндегі сыни қате. Логтарды тексеріңіз</b>",
            "version_info": (
                "<emoji id=5226929552319594190>ℹ️</emoji> <b>Юзербот нұсқасы:</b>\n\n"
                "<b>Хэш:</b> <code>{version}</code>\n"
                "<b>Күні:</b> <code>{date}</code>\n"
                "<b>Авторы:</b> <code>{author}</code>\n"
            ),
            "version_error": "<emoji id=5210952531676504517>❌</emoji> <b>Нұсқа туралы ақпаратты алу мүмкін емес</b>",
            "updating_alert": "🔄 Жаңартылуда..."
        },
        "uz": {
            "restart_premium": "<b>Sizning <emoji id=5199885066674661599>🌙</emoji><emoji id=5199427893175807183>🌙</emoji><emoji id=5199518289352486689>🌙</emoji> qayta ishga tushmoqda...</b>",
            "restart_normal": "<b>🌙 Xioca qayta ishga tushmoqda...</b>",
            "restart_error": "<emoji id=5210952531676504517>❌</emoji> <b>Qayta ishga tushirishda xatolik. Loglarni tekshiring</b>",
            "update_emoji": "<emoji id=5375338737028841420>🔄</emoji>",
            "checking_updates": "<emoji id=5375338737028841420>🔄</emoji> <b>Yangilanishlar tekshirilmoqda...</b>",
            "no_git_repo": "<emoji id=5210952531676504517>❌</emoji> <b>Joriy katalog git repozitoriyasi emas</b>",
            "already_latest": "<emoji id=5206607081334906820>✔️</emoji> <b>Sizda allaqachon so'nggi versiya o'rnatilgan</b>",
            "fetch_error": "<emoji id=5210952531676504517>❌</emoji> <b>Yangilanishlarni olishda xatolik. Loglarni tekshiring</b>",
            "installing_deps": "<emoji id=5375338737028841420>🔄</emoji> <b>Bog'liqliklar o'rnatilmoqda...</b>",
            "deps_error": "<emoji id=5210952531676504517>❌</emoji> <b>Bog'liqliklarni o'rnatishda xatolik. Loglarni tekshiring</b>",
            "critical_update_error": "<emoji id=5210952531676504517>❌</emoji> <b>Yangilanish vaqtida jiddiy xatolik. Loglarni tekshiring</b>",
            "version_info": (
                "<emoji id=5226929552319594190>ℹ️</emoji> <b>Yuzerbot versiyasi:</b>\n\n"
                "<b>Xesh:</b> <code>{version}</code>\n"
                "<b>Sana:</b> <code>{date}</code>\n"
                "<b>Muallif:</b> <code>{author}</code>\n"
            ),
            "version_error": "<emoji id=5210952531676504517>❌</emoji> <b>Versiya ma'lumotlarini olib bo'lmadi</b>",
            "updating_alert": "🔄 Yangilanmoqda..."
        }
    }

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
                restart_text = self.S("restart_premium")
            else:
                restart_text = self.S("restart_normal")

            await utils.answer(message, restart_text)
            logging.info("Инициирована перезагрузка юзербота")
            sys.exit(0)

        except Exception as e:
            logging.exception(f"Ошибка при перезагрузке: {e}")
            await utils.answer(
                message,
                self.S("restart_error")
            )
    
    @loader.command("upd")
    async def update_cmd(self, app: Client, message: types.Message, calldata=False):
        """Обновить юзербота. Использование: update"""
        if calldata:
            message = await app.send_message(self.bot.id, self.S("update_emoji"))

        try:
            await utils.answer(message, self.S("checking_updates"))

            if "LAVHOST" in os.environ:
                os.system("lavhost update")
                return await self.restart_cmd(app, message, True)

            repo_path = Path(".").absolute()

            try:
                repo = Repo(repo_path)
            except InvalidGitRepositoryError:
                return await utils.answer(
                    message,
                    self.S("no_git_repo")
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
                        self.S("already_latest")
                    )

                repo.git.reset("--hard", "origin/main" if "main" in repo.heads else "origin/master")

            except GitCommandError as e:
                logging.error(f"Git error: {e}")
                return await utils.answer(
                    message,
                    self.S("fetch_error")
                )

            await utils.answer(message, self.S("installing_deps"))

            requirements = repo_path / "requirements.txt"
            if requirements.exists():
                if sys.version_info >= (3, 11):
                    pip = await asyncio.create_subprocess_exec(
                        sys.executable, "-m", "pip", "install", "-r", str(requirements), "--break-system-packages",
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                else:
                    pip = await asyncio.create_subprocess_exec(
                        sys.executable, "-m", "pip", "install", "-r", str(requirements),
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )

                stdout, stderr = await pip.communicate()

                if pip.returncode != 0:
                    error_msg = stderr.decode().strip() if stderr else "Unknown error"
                    logging.error(f"Ошибка установки зависимостей: {error_msg}")
                    return await utils.answer(
                        message,
                        self.S("deps_error")
                    )
            self.db.set("xioca.loader", "new_update", False)
            return await self.restart_cmd(app, message, True)

        except Exception as e:
            logging.exception(f"Ошибка при обновлении: {e}")
            await utils.answer(
                message,
                self.S("critical_update_error")
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
                self.S("version_info", version=version, date=date, author=author)
            )
        except Exception as e:
            logging.exception(f"Ошибка получения версии: {e}")
            await utils.answer(
                message,
                self.S("version_error")
            )

    @loader.callback("update")
    async def update_callback_handler(self, app: Client, call: CallbackQuery):
        """Обновление по кнопке"""
        message = types.Message(
            id=call.message.message_id,
            chat=call.message.chat,
            from_user=call.from_user,
            date=call.message.date,
            client=app
        )

        await call.answer(self.S("updating_alert"))

        await self.update_cmd(app, message, True)
