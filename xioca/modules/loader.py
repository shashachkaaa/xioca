# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import os
import requests
import logging
import re
import html
from pyrogram import Client, types
from pyrogram.enums import ChatType
from aiogram.types import (
    InlineQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .. import loader, utils, __system_mod__

@loader.module(author="sh1tn3t | shashachkaaa")
class LoaderMod(loader.Module):
    """Загрузчик модулей"""

    def _canonical_filename_from_source(self, source: str):
        """Best-effort filename from module class: ClassNameMod -> ClassName.py.

        Uses regex only (no AST/compile), so it won't break on `from __future__` placement.
        """
        try:
            prefer = re.search(
                r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)Mod\s*\(\s*(?:loader\.)?Module\s*[\),]",
                source,
                flags=re.M,
            )
            if prefer:
                return prefer.group(1) + ".py"

            any_cls = re.search(
                r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)Mod\s*\(",
                source,
                flags=re.M,
            )
            if any_cls:
                return any_cls.group(1) + ".py"
        except Exception:
            pass
        return None

    strings = {
        "ru": {
            "btn_sub": "💬 Подписаться",
            "btn_no_sub": "🚫 Не подписываться",
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Необходимо указать ссылку или название модуля</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Загрузка модуля из {url}...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Ошибка загрузки модуля (код {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Зависимости установлены. Требуется перезагрузка</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Не удалось загрузить модуль. Подробности смотри в логах</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{module}</code>» <b>не найден</b>",
            "no_cmd_doc": "Нет описания для команды",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Автор:</b> <code>{author}</code>\n",
            "author_channel_ask": "\n❤️ <b>Модуль был разработан в @{author}. Подписаться на канал чтобы поддержать разработчика?</b>",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Версия:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Описание:</b>\n",
            "no_mod_doc": "Нет описания для модуля",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Модуль \"<code>{module}</code>\" загружен</b>\n{header}{commands}\n{inline}",
            "dl_exception": "<emoji id=5210952531676504517>❌</emoji> <b>Ошибка при загрузке модуля:</b> {error}\nURL: {url}",
            "unexpected_error": "<emoji id=5210952531676504517>❌</emoji> <b>Произошла непредвиденная ошибка. Подробности в логах</b>",
            "reply_needed": "<emoji id=5210952531676504517>❌</emoji> <b>Необходим ответ на файл</b>",
            "not_py": "<emoji id=5210952531676504517>❌</emoji> <b>Это не python файл!</b>",
            "no_class": "<emoji id=5210952531676504517>❌</emoji> <b>Не удалось определить класс модуля (должен заканчиваться на Mod)</b>",
            "system_clash": "<emoji id=5210952531676504517>❌</emoji> <b>класс этого модуля соответствует встроенному!</b>",
            "decode_error": "<emoji id=5210952531676504517>❌</emoji> <b>Неверная кодировка файла</b>",
            "read_error": "<emoji id=5210952531676504517>❌</emoji> <b>Не удалось прочитать файл</b>",
            "loading": "<emoji id=5328274090262275771>⏳</emoji> <b>Загрузка модуля...</b>",
            "system_unload_fail": "<emoji id=5210952531676504517>❌</emoji> <code>{module}</code> <b>является системным модулем, его выгрузить невозможно!</b>",
            "unloaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Модуль \"<code>{module}</code>\" выгружен</b>\n\n{text}",
            "no_args_short": "<emoji id=5210952531676504517>❌</emoji> <b>Нет аргументов</b>",
            "file_caption": "<emoji id=5433653135799228968>📁</emoji> <b>Файл</b> <code>{module}</code>\n\n<emoji id=5195083327597456039>🌙</emoji> <code>.loadmod</code> <b>в ответ на это сообщение, чтобы установить модуль</b>\n\n{text}",
            "file_mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль не найден</b>"
        },
        "en": {
            "btn_sub": "💬 Subscribe",
            "btn_no_sub": "🚫 Do not subscribe",
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>You must specify a link or module name</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Downloading module from {url}...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Module download error (code {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Dependencies installed. Restart required</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Failed to load module. Check logs for details</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Module</b> «<code>{module}</code>» <b>not found</b>",
            "no_cmd_doc": "No description for command",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Author:</b> <code>{author}</code>\n",
            "author_channel_ask": "\n❤️ <b>The module was developed in @{author}. Subscribe to the channel to support the developer?</b>",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Version:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Description:</b>\n",
            "no_mod_doc": "No description for module",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Module \"<code>{module}</code>\" loaded</b>\n{header}{commands}\n{inline}",
            "dl_exception": "<emoji id=5210952531676504517>❌</emoji> <b>Error loading module:</b> {error}\nURL: {url}",
            "unexpected_error": "<emoji id=5210952531676504517>❌</emoji> <b>Unexpected error occurred. Check logs</b>",
            "reply_needed": "<emoji id=5210952531676504517>❌</emoji> <b>Reply to a file is required</b>",
            "not_py": "<emoji id=5210952531676504517>❌</emoji> <b>This is not a python file!</b>",
            "no_class": "<emoji id=5210952531676504517>❌</emoji> <b>Failed to determine module class (must end with Mod)</b>",
            "system_clash": "<emoji id=5210952531676504517>❌</emoji> <b>this module's class corresponds to a built-in one!</b>",
            "decode_error": "<emoji id=5210952531676504517>❌</emoji> <b>Invalid file encoding</b>",
            "read_error": "<emoji id=5210952531676504517>❌</emoji> <b>Failed to read file</b>",
            "loading": "<emoji id=5328274090262275771>⏳</emoji> <b>Loading module...</b>",
            "system_unload_fail": "<emoji id=5210952531676504517>❌</emoji> <code>{module}</code> <b>is a system module, it cannot be unloaded!</b>",
            "unloaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Module \"<code>{module}</code>\" unloaded</b>\n\n{text}",
            "no_args_short": "<emoji id=5210952531676504517>❌</emoji> <b>No arguments</b>",
            "file_caption": "<emoji id=5433653135799228968>📁</emoji> <b>File</b> <code>{module}</code>\n\n<emoji id=5195083327597456039>🌙</emoji> <code>.loadmod</code> <b>in reply to this message to install the module</b>\n\n{text}",
            "file_mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Module not found</b>"
        },
        "be": {
            "btn_sub": "💬 Падпісацца",
            "btn_no_sub": "🚫 Не падпісвацца",
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Неабходна пазначыць спасылку або назву модуля</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Загрузка модуля з {url}...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Памылка загрузкі модуля (код {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Залежнасці ўсталяваны. Патрабуецца перазагрузка</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Не ўдалося загрузіць модуль. Падрабязнасці ў логах</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{module}</code>» <b>не знойдзены</b>",
            "no_cmd_doc": "Няма апісання для каманды",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Аўтар:</b> <code>{author}</code>\n",
            "author_channel_ask": "\n❤️ <b>Модуль быў распрацаваны ў @{author}. Падпісацца на канал, каб падтрымаць распрацоўшчыка?</b>",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Версія:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Апісанне:</b>\n",
            "no_mod_doc": "Няма апісання для модуля",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Модуль \"<code>{module}</code>\" загружаны</b>\n{header}{commands}\n{inline}",
            "dl_exception": "<emoji id=5210952531676504517>❌</emoji> <b>Памылка пры загрузцы модуля:</b> {error}\nURL: {url}",
            "unexpected_error": "<emoji id=5210952531676504517>❌</emoji> <b>Адбылася непрадбачаная памылка. Падрабязнасці ў логах</b>",
            "reply_needed": "<emoji id=5210952531676504517>❌</emoji> <b>Неабходны адказ на файл</b>",
            "not_py": "<emoji id=5210952531676504517>❌</emoji> <b>Гэта не python файл!</b>",
            "no_class": "<emoji id=5210952531676504517>❌</emoji> <b>Не ўдалося вызначыць клас модуля (павінен заканчвацца на Mod)</b>",
            "system_clash": "<emoji id=5210952531676504517>❌</emoji> <b>клас гэтага модуля адпавядае ўбудаванаму!</b>",
            "decode_error": "<emoji id=5210952531676504517>❌</emoji> <b>Няправільная кадыроўка файла</b>",
            "read_error": "<emoji id=5210952531676504517>❌</emoji> <b>Не ўдалося прачытаць файл</b>",
            "loading": "<emoji id=5328274090262275771>⏳</emoji> <b>Загрузка модуля...</b>",
            "system_unload_fail": "<emoji id=5210952531676504517>❌</emoji> <code>{module}</code> <b>з'яўляецца сістэмным модулем, яго немагчыма выгрузіць!</b>",
            "unloaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Модуль \"<code>{module}</code>\" выгружаны</b>\n\n{text}",
            "no_args_short": "<emoji id=5210952531676504517>❌</emoji> <b>Няма аргументаў</b>",
            "file_caption": "<emoji id=5433653135799228968>📁</emoji> <b>Файл</b> <code>{module}</code>\n\n<emoji id=5195083327597456039>🌙</emoji> <code>.loadmod</code> <b>у адказ на гэта паведамленне, каб усталяваць модуль</b>\n\n{text}",
            "file_mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль не знойдзены</b>"
        },
        "de": {
            "btn_sub": "💬 Abonnieren",
            "btn_no_sub": "🚫 Nicht abonnieren",
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Sie müssen einen Link oder Modulnamen angeben</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Modul wird von {url} heruntergeladen...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Modul-Download-Fehler (Code {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Abhängigkeiten installiert. Neustart erforderlich</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Modul konnte nicht geladen werden. Details in den Logs</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Modul</b> «<code>{module}</code>» <b>nicht gefunden</b>",
            "no_cmd_doc": "Keine Beschreibung für Befehl",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Autor:</b> <code>{author}</code>\n",
            "author_channel_ask": "\n❤️ <b>Das Modul wurde in @{author} entwickelt. Kanal abonnieren, um den Entwickler zu unterstützen?</b>",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Version:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Beschreibung:</b>\n",
            "no_mod_doc": "Keine Beschreibung für Modul",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Modul \"<code>{module}</code>\" geladen</b>\n{header}{commands}\n{inline}",
            "dl_exception": "<emoji id=5210952531676504517>❌</emoji> <b>Fehler beim Laden des Moduls:</b> {error}\nURL: {url}",
            "unexpected_error": "<emoji id=5210952531676504517>❌</emoji> <b>Unerwarteter Fehler aufgetreten. Siehe Logs</b>",
            "reply_needed": "<emoji id=5210952531676504517>❌</emoji> <b>Antwort auf eine Datei erforderlich</b>",
            "not_py": "<emoji id=5210952531676504517>❌</emoji> <b>Dies ist keine Python-Datei!</b>",
            "no_class": "<emoji id=5210952531676504517>❌</emoji> <b>Modulklasse konnte nicht bestimmt werden (muss auf Mod enden)</b>",
            "system_clash": "<emoji id=5210952531676504517>❌</emoji> <b>Modulklasse entspricht einem System-Modul!</b>",
            "decode_error": "<emoji id=5210952531676504517>❌</emoji> <b>Ungültige Dateikodierung</b>",
            "read_error": "<emoji id=5210952531676504517>❌</emoji> <b>Datei konnte nicht gelesen werden</b>",
            "loading": "<emoji id=5328274090262275771>⏳</emoji> <b>Modul wird geladen...</b>",
            "system_unload_fail": "<emoji id=5210952531676504517>❌</emoji> <code>{module}</code> <b>ist ein Systemmodul, Entladen nicht möglich!</b>",
            "unloaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Modul \"<code>{module}</code>\" entladen</b>\n\n{text}",
            "no_args_short": "<emoji id=5210952531676504517>❌</emoji> <b>Keine Argumente</b>",
            "file_caption": "<emoji id=5433653135799228968>📁</emoji> <b>Datei</b> <code>{module}</code>\n\n<emoji id=5195083327597456039>🌙</emoji> <code>.loadmod</code> <b>als Antwort, um das Modul zu installieren</b>\n\n{text}",
            "file_mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Modul nicht gefunden</b>"
        },
        "es": {
            "btn_sub": "💬 Suscribirse",
            "btn_no_sub": "🚫 No suscribirse",
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Debes especificar un enlace o nombre del módulo</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Descargando módulo desde {url}...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Error de descarga (código {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Dependencias instaladas. Reinicio requerido</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Error al cargar. Revisa los logs</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Módulo</b> «<code>{module}</code>» <b>no encontrado</b>",
            "no_cmd_doc": "Sin descripción",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Autor:</b> <code>{author}</code>\n",
            "author_channel_ask": "\n❤️ <b>El módulo fue desarrollado en @{author}. ¿Suscribirse al canal para apoyar al desarrollador?</b>",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Versión:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Descripción:</b>\n",
            "no_mod_doc": "Sin descripción del módulo",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Módulo \"<code>{module}</code>\" cargado</b>\n{header}{commands}\n{inline}",
            "dl_exception": "<emoji id=5210952531676504517>❌</emoji> <b>Error:</b> {error}\nURL: {url}",
            "unexpected_error": "<emoji id=5210952531676504517>❌</emoji> <b>Error inesperado. Revisa los logs</b>",
            "reply_needed": "<emoji id=5210952531676504517>❌</emoji> <b>Responde a un archivo</b>",
            "not_py": "<emoji id=5210952531676504517>❌</emoji> <b>¡No es un archivo Python!</b>",
            "no_class": "<emoji id=5210952531676504517>❌</emoji> <b>Clase no válida (debe terminar en Mod)</b>",
            "system_clash": "<emoji id=5210952531676504517>❌</emoji> <b>¡Clase del sistema en conflicto!</b>",
            "decode_error": "<emoji id=5210952531676504517>❌</emoji> <b>Codificación no válida</b>",
            "read_error": "<emoji id=5210952531676504517>❌</emoji> <b>Error al leer el archivo</b>",
            "loading": "<emoji id=5328274090262275771>⏳</emoji> <b>Cargando módulo...</b>",
            "system_unload_fail": "<emoji id=5210952531676504517>❌</emoji> <b>¡Módulo del sistema, no se puede descargar!</b>",
            "unloaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Módulo \"<code>{module}</code>\" descargado</b>\n\n{text}",
            "no_args_short": "<emoji id=5210952531676504517>❌</emoji> <b>Sin argumentos</b>",
            "file_caption": "<emoji id=5433653135799228968>📁</emoji> <b>Archivo</b> <code>{module}</code>\n\n<emoji id=5195083327597456039>🌙</emoji> <code>.loadmod</code> <b>en respuesta para instalar</b>\n\n{text}",
            "file_mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Módulo no encontrado</b>"
        },
        "fr": {
            "btn_sub": "💬 S'abonner",
            "btn_no_sub": "🚫 Ne pas s'abonner",
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Lien ou nom de module requis</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Téléchargement depuis {url}...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Erreur (code {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Dépendances installées. Redémarrage requis</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Échec du chargement. Voir les logs</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Module</b> «<code>{module}</code>» <b>non trouvé</b>",
            "no_cmd_doc": "Pas de description",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Auteur:</b> <code>{author}</code>\n",
            "author_channel_ask": "\n❤️ <b>Le module a été développé dans @{author}. S'abonner à la chaîne pour soutenir le développeur ?</b>",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Version:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Description:</b>\n",
            "no_mod_doc": "Pas de description",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Module \"<code>{module}</code>\" chargé</b>\n{header}{commands}\n{inline}",
            "dl_exception": "<emoji id=5210952531676504517>❌</emoji> <b>Erreur:</b> {error}",
            "unexpected_error": "<emoji id=5210952531676504517>❌</emoji> <b>Erreur inattendue</b>",
            "reply_needed": "<emoji id=5210952531676504517>❌</emoji> <b>Répondez à un fichier</b>",
            "not_py": "<emoji id=5210952531676504517>❌</emoji> <b>Pas un fichier Python!</b>",
            "no_class": "<emoji id=5210952531676504517>❌</emoji> <b>Classe invalide (doit finir par Mod)</b>",
            "system_clash": "<emoji id=5210952531676504517>❌</emoji> <b>Conflit système!</b>",
            "decode_error": "<emoji id=5210952531676504517>❌</emoji> <b>Codage invalide</b>",
            "read_error": "<emoji id=5210952531676504517>❌</emoji> <b>Erreur de lecture</b>",
            "loading": "<emoji id=5328274090262275771>⏳</emoji> <b>Chargement...</b>",
            "system_unload_fail": "<emoji id=5210952531676504517>❌</emoji> <b>Module système indéchargeable!</b>",
            "unloaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Module \"<code>{module}</code>\" déchargé</b>\n\n{text}",
            "no_args_short": "<emoji id=5210952531676504517>❌</emoji> <b>Pas d'arguments</b>",
            "file_caption": "<emoji id=5433653135799228968>📁</emoji> <b>Fichier</b> <code>{module}</code>\n\n<emoji id=5195083327597456039>🌙</emoji> <code>.loadmod</code> <b>en réponse pour installer</b>\n\n{text}",
            "file_mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Module non trouvé</b>"
        },
        "it": {
            "btn_sub": "💬 Iscriviti",
            "btn_no_sub": "🚫 Non iscriverti",
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Specifica un link o il nome del modulo</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Download modulo da {url}...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Errore download (codice {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Dipendenze installate. Riavvio richiesto</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Caricamento fallito. Controlla i log</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Modulo</b> «<code>{module}</code>» <b>non trovato</b>",
            "no_cmd_doc": "Nessuna descrizione",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Autore:</b> <code>{author}</code>\n",
            "author_channel_ask": "\n❤️ <b>Il modulo è stato sviluppato in @{author}. Iscriversi al canale per sostenere lo sviluppatore?</b>",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Versione:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Descrizione:</b>\n",
            "no_mod_doc": "Nessuna descrizione",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Modulo \"<code>{module}</code>\" caricato</b>\n{header}{commands}\n{inline}",
            "dl_exception": "<emoji id=5210952531676504517>❌</emoji> <b>Errore:</b> {error}",
            "unexpected_error": "<emoji id=5210952531676504517>❌</emoji> <b>Errore imprevisto</b>",
            "reply_needed": "<emoji id=5210952531676504517>❌</emoji> <b>Rispondi a un file</b>",
            "not_py": "<emoji id=5210952531676504517>❌</emoji> <b>Non è un file Python!</b>",
            "no_class": "<emoji id=5210952531676504517>❌</emoji> <b>Classe non trovata (deve finire in Mod)</b>",
            "system_clash": "<emoji id=5210952531676504517>❌</emoji> <b>Conflitto con modulo di sistema!</b>",
            "decode_error": "<emoji id=5210952531676504517>❌</emoji> <b>Codifica non valida</b>",
            "read_error": "<emoji id=5210952531676504517>❌</emoji> <b>Errore di lettura</b>",
            "loading": "<emoji id=5328274090262275771>⏳</emoji> <b>Caricamento...</b>",
            "system_unload_fail": "<emoji id=5210952531676504517>❌</emoji> <b>Modulo di sistema, impossibile scaricare!</b>",
            "unloaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Modulo \"<code>{module}</code>\" scaricato</b>\n\n{text}",
            "no_args_short": "<emoji id=5210952531676504517>❌</emoji> <b>Senza argomenti</b>",
            "file_caption": "<emoji id=5433653135799228968>📁</emoji> <b>File</b> <code>{module}</code>\n\n<emoji id=5195083327597456039>🌙</emoji> <code>.loadmod</code> <b>in risposta per installare</b>\n\n{text}",
            "file_mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Modulo non trovato</b>"
        },
        "kk": {
            "btn_sub": "💬 Жазылу",
            "btn_no_sub": "🚫 Жазылмау",
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Сілтемені немесе модуль атауын көрсету қажет</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Модульді {url} сілтемесінен жүктеу...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Жүктеу қатесі (код {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Тәуелділіктер орнатылды. Қайта жүктеу қажет</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Модульді жүктеу мүмкін болмады. Толығырақ логтарда</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>«<code>{module}</code>» модулі табылмады</b>",
            "no_cmd_doc": "Команданың сипаттамасы жоқ",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Авторы:</b> <code>{author}</code>\n",
            "author_channel_ask": "\n❤️ <b>Модуль @{author} арнасында жасақталды. Әзірлеушіні қолдау үшін арнаға жазыласыз ба?</b>",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Нұсқасы:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Сипаттамасы:</b>\n",
            "no_mod_doc": "Модульдің сипаттамасы жоқ",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>\"<code>{module}</code>\" модулі жүктелді</b>\n{header}{commands}\n{inline}",
            "dl_exception": "<emoji id=5210952531676504517>❌</emoji> <b>Жүктеу қатесі:</b> {error}\nURL: {url}",
            "unexpected_error": "<emoji id=5210952531676504517>❌</emoji> <b>Күтпеген қате орын алды. Толығырақ логтарда</b>",
            "reply_needed": "<emoji id=5210952531676504517>❌</emoji> <b>Файлға жауап (reply) қажет</b>",
            "not_py": "<emoji id=5210952531676504517>❌</emoji> <b>Бұл python файлы емес!</b>",
            "no_class": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль класын анықтау мүмкін болмады (Mod-пен аяқталуы тиіс)</b>",
            "system_clash": "<emoji id=5210952531676504517>❌</emoji> <b>Бұл модуль класы жүйелік модульмен сәйкес келеді!</b>",
            "decode_error": "<emoji id=5210952531676504517>❌</emoji> <b>Файл кодтауы қате</b>",
            "read_error": "<emoji id=5210952531676504517>❌</emoji> <b>Файлды оқу мүмкін болмады</b>",
            "loading": "<emoji id=5328274090262275771>⏳</emoji> <b>Модуль жүктелуде...</b>",
            "system_unload_fail": "<emoji id=5210952531676504517>❌</emoji> <code>{module}</code> <b>жүйелік модуль, оны өшіру мүмкін емес!</b>",
            "unloaded": "<emoji id=5206607081334906820>✔️</emoji> <b>\"<code>{module}</code>\" модулі өшірілді</b>\n\n{text}",
            "no_args_short": "<emoji id=5210952531676504517>❌</emoji> <b>Аргументтер жоқ</b>",
            "file_caption": "<emoji id=5433653135799228968>📁</emoji> <b>Файл</b> <code>{module}</code>\n\n<emoji id=5195083327597456039>🌙</emoji> <b>Модульді орнату үшін осы хабарламаға</b> <code>.loadmod</code> <b>деп жауап беріңіз</b>\n\n{text}",
            "file_mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль табылмады</b>"
        },
        "uz": {
            "btn_sub": "💬 Obuna bo'lish",
            "btn_no_sub": "🚫 Obuna bo'lmaslik",
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Havola yoki modul nomini ko'rsatish kerak</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Modul {url} dan yuklanmoqda...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Yuklashda xato (kod {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Kutubxonalar o'rnatildi. Qayta yuklash talab qilinadi</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Modulni yuklab bo'lmadi. Tafsilotlar loglarda</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>«<code>{module}</code>» moduli topilmadi</b>",
            "no_cmd_doc": "Buyruq tavsifi yo'q",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Muallif:</b> <code>{author}</code>\n",
            "author_channel_ask": "\n❤️ <b>Modul @{author}-da ishlab chiqilgan. Dasturchini qo'llab-quvvatlash uchun kanalga obuna bo'lasizmi?</b>",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Versiya:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Tavsif:</b>\n",
            "no_mod_doc": "Modul tavsifi yo'q",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>\"<code>{module}</code>\" moduli yuklandi</b>\n{header}{commands}\n{inline}",
            "dl_exception": "<emoji id=5210952531676504517>❌</emoji> <b>Xatolik:</b> {error}\nURL: {url}",
            "unexpected_error": "<emoji id=5210952531676504517>❌</emoji> <b>Kutilmagan xato. Tafsilotlar loglarda</b>",
            "reply_needed": "<emoji id=5210952531676504517>❌</emoji> <b>Faylga javob (reply) berish kerak</b>",
            "not_py": "<emoji id=5210952531676504517>❌</emoji> <b>Bu python fayli emas!</b>",
            "no_class": "<emoji id=5210952531676504517>❌</emoji> <b>Modul klassini aniqlab bo'lmadi (Mod bilan tugashi kerak)</b>",
            "system_clash": "<emoji id=5210952531676504517>❌</emoji> <b>Bu klass tizim moduli bilan bir xil!</b>",
            "decode_error": "<emoji id=5210952531676504517>❌</emoji> <b>Fayl kodirovkasi noto'g'ri</b>",
            "read_error": "<emoji id=5210952531676504517>❌</emoji> <b>Faylni o'qib bo'lmadi</b>",
            "loading": "<emoji id=5328274090262275771>⏳</emoji> <b>Modul yuklanmoqda...</b>",
            "system_unload_fail": "<emoji id=5210952531676504517>❌</emoji> <code>{module}</code> <b>tizim moduli, uni o'chirib bo'lmaydi!</b>",
            "unloaded": "<emoji id=5206607081334906820>✔️</emoji> <b>\"<code>{module}</code>\" moduli o'chirildi</b>\n\n{text}",
            "no_args_short": "<emoji id=5210952531676504517>❌</emoji> <b>Argumentlar yo'q</b>",
            "file_caption": "<emoji id=5433653135799228968>📁</emoji> <b>Fayl</b> <code>{module}</code>\n\n<emoji id=5195083327597456039>🌙</emoji> <b>O'rnatish uchun ushbu xabarga</b> <code>.loadmod</code> <b>deb javob bering</b>\n\n{text}",
            "file_mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Modul topilmadi</b>"
        }
    }

    async def _get_bot_username(self):
        """Получает юзернейм бота (для инлайн команд)"""
        try:
            me = await self.bot.get_me()
            return me.username
        except:
            return "bot"

    async def _is_channel_author(self, app, author: str) -> bool:
        """Проверяет, является ли автор каналом"""
        if not author or " " in author:
            return False
        try:
            chat = await app.get_chat(author.replace("@", ""))
            return chat.type == ChatType.CHANNEL
        except:
            return False

    async def _generate_module_text(self, module, mod_name, bot_username):
        """Генерирует текст успешной загрузки (общий для inline и answer)"""
        prefix = self.db.get("xioca.loader", "prefixes", ["."])[0]
        
        cmds = ""
        for cmd, func in module.command_handlers.items():
            raw_doc = func.__doc__ or self.S("no_cmd_doc")
            doc = html.escape(raw_doc)
            cmds += f"\n👉 <code>{prefix}{cmd}</code>\n    ╰ {doc}"
        
        if hasattr(module, "inline_handlers"):
            for cmd, func in module.inline_handlers.items():
                raw_doc = func.__doc__ or self.S("no_cmd_doc")
                doc = html.escape(raw_doc)
                cmds += f"\n🤖 <code>@{bot_username} {cmd}</code>\n    ╰ {doc}"

        description = module.__doc__ or self.S("no_mod_doc")
        header = self.S("desc_header") + f"    ╰ {description}\n"
        
        return self.S("loaded", module=mod_name, header=header, commands=cmds, inline="").strip()

    async def _finalize_loading(self, app, message, loaded_name, module):
        """Финальная логика: решает, отправлять инлайн или редактировать сообщение"""
        author = getattr(module, "author", "Unknown")
        
        if await self._is_channel_author(app, author):
            return await utils.inline(self, message, f"lm_res {loaded_name}")
        else:
            bot_username = await self._get_bot_username()
            text_body = await self._generate_module_text(module, loaded_name, bot_username)
            
            author_str = self.S("author_str", author=author)
            
            full_text = f"{text_body}\n\n{author_str}"
            
            return await utils.answer(message, full_text)

    @loader.command("dlm")
    async def dlmod_cmd(self, app: Client, message: types.Message, args):
        """Загрузить модуль по ссылке"""
        if not args:
            return await utils.answer(message, self.S("no_args"))
        
        repo_url = self.db.get("xioca.loader", "repo", "https://xioca.ferz.live/module/")
        if not args.startswith(("http://", "https://")):
            module_name = args if args.endswith(".py") else f"{args}.py"
            args = f"{repo_url}{module_name}"
        else:
            module_name = args.split("/")[-1]
            if not module_name.endswith(".py"): module_name = f"{module_name}.py"
        
        await utils.answer(message, self.S("downloading", url=args))
        
        async def status_updater(text):
        	await utils.answer(message, f"{text}")
        
        try:
            r = await utils.run_sync(requests.get, args)
            if r.status_code != 200:
                return await utils.answer(message, self.S("dl_error", code=r.status_code, url=args))
        
            module_source = r.text
            canonical = self._canonical_filename_from_source(module_source)
            if canonical:
                module_name = canonical
            file_path = f"modules/{module_name}"

            with open(f"xioca/{file_path}", "w", encoding="utf-8") as f:
                f.write(module_source)
            
            loaded_name = await self.all_modules.load_module(module_source=module_source, origin=args, update_callback=status_updater)
            
            if loaded_name:
                module = self.all_modules.get_module(loaded_name)
                return await self._finalize_loading(app, message, loaded_name, module)
            else:
                return await utils.answer(message, self.S("load_failed"))

        except Exception as e:
            return await utils.answer(message, self.S("dl_exception", error=str(e), url=args))

    @loader.command("lm")
    async def loadmod_cmd(self, app: Client, message: types.Message):
        """Загрузить модуль по файлу"""
        reply = message.reply_to_message
        file = message if message.document else reply if reply and reply.document else None

        if not file: return await utils.answer(message, self.S("reply_needed"))
        if not file.document.file_name.endswith(".py"): return await utils.answer(message, self.S("not_py"))

        file_path = f"modules/{file.document.file_name}"
        await file.download(file_path)

        with open(f"xioca/{file_path}", "r", encoding="utf-8") as f:
            source = f.read()
       
        async def status_updater(text):
        	await utils.answer(message, f"{text}")
        
        loaded_name = await self.all_modules.load_module(module_source=source, update_callback=status_updater)
        if loaded_name:
            module = self.all_modules.get_module(loaded_name)
            return await self._finalize_loading(app, message, loaded_name, module)
            
        return await utils.answer(message, self.S("load_failed"))

    @loader.inline("lm_res", True)
    async def load_res_inline(self, app: Client, query: InlineQuery, args):
        """Отображение результата установки (только для каналов или если вызвано принудительно)"""
        mod_name = args
        module = self.all_modules.get_module(mod_name.lower())
        if not module: return

        def clean(text):
            return re.sub(r"<emoji[^>]*>(.*?)</emoji>", r"\1", text)

        bot_username = await self._get_bot_username()
        author = getattr(module, "author", "Unknown")
        
        text_body = await self._generate_module_text(module, mod_name, bot_username)
        
        is_channel = await self._is_channel_author(app, author)

        builder = InlineKeyboardBuilder()

        if is_channel:
            clean_author = author.replace('@', '')
            inline_text = clean(self.S("author_channel_ask", author=clean_author))
            builder.row(
                InlineKeyboardButton(text=self.S("btn_sub"), callback_data=f"loader_sub_{author}"),
                InlineKeyboardButton(text=self.S("btn_no_sub"), callback_data="loader_close_lm")
            )
        else:
            inline_text = clean(self.S("author_str", author=author))
            builder.row(InlineKeyboardButton(text="❌", callback_data="loader_close_lm"))

        full_text = f"{text_body}\n{inline_text}"
        full_text = clean(full_text)

        loaded_title = self.strings.get("ru", {}).get("loaded_title", "Module Loaded") 
        
        await utils.answer_inline(query, full_text, loaded_title, builder.as_markup())

    
    @loader.callback("loader_sub")
    async def loader_sub_callback(self, app: Client, call: CallbackQuery):
        await app.join_chat(call.data.split("_")[2])
        
        await call.answer("✅")
    
    @loader.callback("loader_close_lm")
    async def close_callback(self, app: Client, call: CallbackQuery):
        await self.bot.edit_message_reply_markup(
            inline_message_id=call.inline_message_id,
            reply_markup=None
        )

    @loader.command("unlm")
    async def unloadmod_cmd(self, app: Client, message: types.Message, args: str):
        """Выгрузить модуль"""
        module_name, text = utils.get_module_name(args)

        if module_name.lower() in __system_mod__:
            return await utils.answer(
                message,
                self.S("system_unload_fail", module=module_name)
            )
 
        unloaded = self.all_modules.unload_module(module_name)
        if not unloaded:
            return await utils.answer(
                message,
                self.S("mod_not_found", module=module_name)
            )

        return await utils.answer(
            message,
            self.S("unloaded", module=unloaded, text=text)
        )

    @loader.command("ml")
    async def ml_cmd(self, app: Client, message: types.Message, args: str):
        """Поделиться модулем"""
        if not args: return await utils.answer(message, self.S("no_args_short"))
        module_name, text = utils.get_module_name(args)
        file_path = f"xioca/modules/{module_name}.py"
        if os.path.exists(file_path):
            await app.send_document(message.chat.id, file_path, caption=self.S("file_caption", module=module_name, text=text))
            await message.delete()
        else:
            await utils.answer(message, self.S("file_mod_not_found"))
