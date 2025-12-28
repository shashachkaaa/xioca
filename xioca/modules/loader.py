# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import os
import requests
import logging
from pyrogram import Client, types
from .. import loader, utils, __system_mod__

@loader.module(author="sh1tn3t | shashachkaaa")
class LoaderMod(loader.Module):
    """Загрузчик модулей"""

    strings = {
        "ru": {
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Необходимо указать ссылку или название модуля</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Загрузка модуля из {url}...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Ошибка загрузки модуля (код {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Зависимости установлены. Требуется перезагрузка</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Не удалось загрузить модуль. Подробности смотри в логах</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{module}</code>» <b>не найден</b>",
            "no_cmd_doc": "Нет описания для команды",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Автор:</b> <code>{author}</code>\n",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Версия:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Описание:</b>\n",
            "no_mod_doc": "Нет описания для модуля",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Модуль \"<code>{module}</code>\" загружен</b>\n\n{header}{commands}\n{inline}",
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
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>You must specify a link or module name</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Downloading module from {url}...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Module download error (code {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Dependencies installed. Restart required</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Failed to load module. Check logs for details</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Module</b> «<code>{module}</code>» <b>not found</b>",
            "no_cmd_doc": "No description for command",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Author:</b> <code>{author}</code>\n",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Version:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Description:</b>\n",
            "no_mod_doc": "No description for module",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Module \"<code>{module}</code>\" loaded</b>\n\n{header}{commands}\n{inline}",
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
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Неабходна пазначыць спасылку або назву модуля</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Загрузка модуля з {url}...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Памылка загрузкі модуля (код {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Залежнасці ўсталяваны. Патрабуецца перазагрузка</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Не ўдалося загрузіць модуль. Падрабязнасці ў логах</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{module}</code>» <b>не знойдзены</b>",
            "no_cmd_doc": "Няма апісання для каманды",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Аўтар:</b> <code>{author}</code>\n",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Версія:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Апісанне:</b>\n",
            "no_mod_doc": "Няма апісання для модуля",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Модуль \"<code>{module}</code>\" загружаны</b>\n\n{header}{commands}\n{inline}",
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
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Sie müssen einen Link oder Modulnamen angeben</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Modul wird von {url} heruntergeladen...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Modul-Download-Fehler (Code {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Abhängigkeiten installiert. Neustart erforderlich</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Modul konnte nicht geladen werden. Details in den Logs</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Modul</b> «<code>{module}</code>» <b>nicht gefunden</b>",
            "no_cmd_doc": "Keine Beschreibung für Befehl",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Autor:</b> <code>{author}</code>\n",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Version:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Beschreibung:</b>\n",
            "no_mod_doc": "Keine Beschreibung für Modul",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Modul \"<code>{module}</code>\" geladen</b>\n\n{header}{commands}\n{inline}",
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
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Debes especificar un enlace o nombre del módulo</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Descargando módulo desde {url}...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Error de descarga (código {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Dependencias instaladas. Reinicio requerido</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Error al cargar. Revisa los logs</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Módulo</b> «<code>{module}</code>» <b>no encontrado</b>",
            "no_cmd_doc": "Sin descripción",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Autor:</b> <code>{author}</code>\n",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Versión:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Descripción:</b>\n",
            "no_mod_doc": "Sin descripción del módulo",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Módulo \"<code>{module}</code>\" cargado</b>\n\n{header}{commands}\n{inline}",
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
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Lien ou nom de module requis</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Téléchargement depuis {url}...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Erreur (code {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Dépendances installées. Redémarrage requis</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Échec du chargement. Voir les logs</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Module</b> «<code>{module}</code>» <b>non trouvé</b>",
            "no_cmd_doc": "Pas de description",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Auteur:</b> <code>{author}</code>\n",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Version:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Description:</b>\n",
            "no_mod_doc": "Pas de description",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Module \"<code>{module}</code>\" chargé</b>\n\n{header}{commands}\n{inline}",
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
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Specifica un link o il nome del modulo</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Download modulo da {url}...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Errore download (codice {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Dipendenze installate. Riavvio richiesto</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Caricamento fallito. Controlla i log</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Modulo</b> «<code>{module}</code>» <b>non trovato</b>",
            "no_cmd_doc": "Nessuna descrizione",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Autore:</b> <code>{author}</code>\n",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Versione:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Descrizione:</b>\n",
            "no_mod_doc": "Nessuna descrizione",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>Modulo \"<code>{module}</code>\" caricato</b>\n\n{header}{commands}\n{inline}",
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
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Сілтемені немесе модуль атауын көрсету қажет</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Модульді {url} сілтемесінен жүктеу...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Жүктеу қатесі (код {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Тәуелділіктер орнатылды. Қайта жүктеу қажет</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Модульді жүктеу мүмкін болмады. Толығырақ логтарда</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>«<code>{module}</code>» модулі табылмады</b>",
            "no_cmd_doc": "Команданың сипаттамасы жоқ",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Авторы:</b> <code>{author}</code>\n",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Нұсқасы:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Сипаттамасы:</b>\n",
            "no_mod_doc": "Модульдің сипаттамасы жоқ",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>\"<code>{module}</code>\" модулі жүктелді</b>\n\n{header}{commands}\n{inline}",
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
            "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Havola yoki modul nomini ko'rsatish kerak</b>",
            "downloading": "<emoji id=5328274090262275771>⏳</emoji> <b>Modul {url} dan yuklanmoqda...</b>",
            "dl_error": "<emoji id=5210952531676504517>❌</emoji> <b>Yuklashda xato (kod {code})</b>\nURL: {url}",
            "deps_installed": "<emoji id=5206607081334906820>✔️</emoji> <b>Kutubxonalar o'rnatildi. Qayta yuklash talab qilinadi</b>",
            "load_failed": "<emoji id=5210952531676504517>❌</emoji> <b>Modulni yuklab bo'lmadi. Tafsilotlar loglarda</b>",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>«<code>{module}</code>» moduli topilmadi</b>",
            "no_cmd_doc": "Buyruq tavsifi yo'q",
            "author_str": "<b><emoji id=5237922302070367159>❤️</emoji> Muallif:</b> <code>{author}</code>\n",
            "version_str": "<b><emoji id=5226929552319594190>0️⃣</emoji> Versiya:</b> <code>{version}</code>\n",
            "desc_header": "\n<b><emoji id=5197269100878907942>✍️</emoji> Tavsif:</b>\n",
            "no_mod_doc": "Modul tavsifi yo'q",
            "loaded": "<emoji id=5206607081334906820>✔️</emoji> <b>\"<code>{module}</code>\" moduli yuklandi</b>\n\n{header}{commands}\n{inline}",
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

    @loader.command("dlm")
    async def dlmod_cmd(self, app: Client, message: types.Message, args):
        """Загрузить модуль по ссылке или из репозитория. Использование: dlmod <ссылка или название модуля>"""
        
        if not args:
            return await utils.answer(message, self.S("no_args"))
        
        repo_url = self.db.get("xioca.loader", "repo", "https://xioca.ferz.live/module/")
        
        if not args.startswith(("http://", "https://")):
            module_name = args if args.endswith(".py") else f"{args}.py"
            args = f"{repo_url}{module_name}"
        else:
            module_name = args.split("/")[-1]
            if not module_name.endswith(".py"):
                module_name = f"{module_name}.py"
        
        msg = await utils.answer(message, self.S("downloading", url=args))
        
        async def update_message(text):
            try:
                await msg.edit(text)
            except:
                pass
        
        try:
            r = await utils.run_sync(requests.get, args)
            if r.status_code != 200:
                return await utils.answer(message, self.S("dl_error", code=r.status_code, url=args))
        
            module_source = r.text
            module_content = module_source
            
            modules_dir = "modules"
            os.makedirs(modules_dir, exist_ok=True)
            file_path = os.path.join(modules_dir, module_name)

            with open(f"xioca/{file_path}", "w", encoding="utf-8") as f:
                f.write(module_content)
            
            module_name = await self.all_modules.load_module(module_source=module_source, origin=args, update_callback=update_message)
        
            if module_name is True:
                return await utils.answer(message, self.S("deps_installed"))
        
            if not module_name:
                if os.path.exists(f"xioca/{file_path}"):
                    try:
                        os.remove(f"xioca/{file_path}")
                    except Exception as e:
                        logging.error(f"Не удалось удалить файл {file_path}: {e}")
                return await utils.answer(message, self.S("load_failed"))
        
            module = self.all_modules.get_module(module_name.lower())
            if not module:
                return await utils.answer(message, self.S("mod_not_found", module=module_name))
        
            if args.startswith(("http://", "https://")):
                modules = self.db.get("xioca.loader", "modules", [])
                if args not in modules:
                    modules.append(args)
                    self.db.set("xioca.loader", "modules", modules)
        
            prefix = self.db.get("xioca.loader", "prefixes", ["."])[0]
            bot_username = (await self.bot.me()).username
        
            command_descriptions = "\n".join(
                f"<emoji id=5471978009449731768>👉</emoji> <code>{prefix + command}</code>\n"
                f"    ╰ {module.command_handlers[command].__doc__ or self.S('no_cmd_doc')}"
                for command in module.command_handlers
            )
        
            inline_descriptions = "\n".join(
                f"<emoji id=5372981976804366741>🤖</emoji> <code>@{bot_username + ' ' + command}</code>\n"
                f"    ╰ {module.inline_handlers[command].__doc__ or self.S('no_cmd_doc')}"
                for command in module.inline_handlers
            )
        
            header = (
                (self.S("author_str", author=module.author) if module.author else "") +
                (self.S("version_str", version=module.version) if module.version else "") +
                f"{self.S('desc_header')}" +
                f"    ╰ {module.__doc__ or self.S('no_mod_doc')}\n\n"
            )
        
            return await utils.answer(message, self.S("loaded", module=module_name, header=header, commands=command_descriptions, inline=("\n" + inline_descriptions)))
        except requests.exceptions.RequestException as e:
            if 'file_path' in locals() and os.path.exists(f"xioca/{file_path}"):
                 os.remove(f"xioca/{file_path}")
            return await utils.answer(message, self.S("dl_exception", error=str(e), url=args))
        except Exception as e:
            logging.exception(f"Ошибка в dlmod_cmd: {e}")
            if 'file_path' in locals() and os.path.exists(f"xioca/{file_path}"):
                 os.remove(f"xioca/{file_path}")
            return await utils.answer(message, self.S("unexpected_error"))
    
    @loader.command("lm")
    async def loadmod_cmd(self, app: Client, message: types.Message):
        """Загрузить модуль по файлу. Использование: <реплай на файл>"""
        reply = message.reply_to_message
        file = (
            message
            if message.document
            else reply
            if reply and reply.document
            else None
        )

        if not file:
            return await utils.answer(
                message, self.S("reply_needed")
            )

        modules_dir = "modules"
        original_file_name = file.document.file_name
        
        if not original_file_name.endswith(".py"):
            return await utils.answer(message, self.S("not_py"))
        
        file_path = os.path.join(modules_dir, file.document.file_name)
        await file.download(file_path)

        try:
            with open(f"xioca/{file_path}", "r", encoding="utf-8") as f:
                module_source = f.read()
            
            class_name = None
            for line in module_source.splitlines():
                if "class" in line and "Mod(loader.Module):" in line:
                    class_name = line.split("class")[1].split("(")[0].strip()
                    break
            
            if not class_name:
                os.remove(f"xioca/{file_path}")
                return await utils.answer(message, self.S("no_class"))
            
            new_class_name = class_name.lower().replace('mod', '')
            
            if new_class_name in __system_mod__:
                os.remove(f"xioca/{file_path}")
                return await utils.answer(message, self.S("system_clash"))
            
            new_file_name = f"{new_class_name}.py"
            new_file_path = os.path.join(modules_dir, new_file_name)
            os.rename(f"xioca/{file_path}", f"xioca/{new_file_path}")
            
        except UnicodeDecodeError:
            if os.path.exists(f"xioca/{file_path}"): os.remove(f"xioca/{file_path}")
            return await utils.answer(
                message, self.S("decode_error")
            )
        except Exception as e:
            logging.error(f"Ошибка при чтении файла: {e}")
            if os.path.exists(f"xioca/{file_path}"): os.remove(f"xioca/{file_path}")
            return await utils.answer(
                message, self.S("read_error")
            )
        
        msg = await utils.answer(message, self.S("loading"))
        
        async def update_message(text):
            try:
                if isinstance(msg, list):
                    if msg: 
                        await msg[0].edit(text)
                else:
                    await msg.edit(text)
            except Exception as e:
                logging.error(f"Ошибка редактирования сообщения: {e}")
        
        module_name = await self.all_modules.load_module(module_source=module_source, update_callback=update_message)
        if module_name is True:
            return await utils.answer(
                message, self.S("deps_installed")
            )

        if not module_name:
            if os.path.exists(f"xioca/{new_file_path}"):
                try:
                    os.remove(f"xioca/{new_file_path}")
                except Exception as e:
                    logging.error(f"Не удалось удалить файл {new_file_path}: {e}")
            return await utils.answer(
                message, self.S("load_failed")
            )
            
        module = self.all_modules.get_module(module_name.lower())
        if not module:
            return await utils.answer(
                message, self.S("mod_not_found", module=module_name)
            )

        prefix = self.db.get("xioca.loader", "prefixes", ["."])[0]
        bot_username = (await self.bot.me()).username

        command_descriptions = "\n".join(
            f"<emoji id=5471978009449731768>👉</emoji> <code>{prefix + command}</code>\n"
            f"    ╰ {module.command_handlers[command].__doc__ or self.S('no_cmd_doc')}"
            for command in module.command_handlers
        )
        
        inline_descriptions = "\n".join(
            f"<emoji id=5471978009449731768>👉</emoji> <code>@{bot_username + ' ' + command}</code>\n"
            f"    ╰ {module.inline_handlers[command].__doc__ or self.S('no_cmd_doc')}"
            for command in module.inline_handlers
        )

        header = (
            (
                self.S("author_str", author=module.author) if module.author else ""
            ) + (
                self.S("version_str", version=module.version) if module.version else ""
            ) + (
                f"{self.S('desc_header')}"
                f"    ╰ {module.__doc__ or self.S('no_mod_doc')}\n\n"
            )
        )

        return await utils.answer(
            message, self.S("loaded", module=module_name, header=header, commands=command_descriptions, inline=("\n" + inline_descriptions))
        )
    
    @loader.command("unlm")
    async def unloadmod_cmd(self, app: Client, message: types.Message, args: str):
        """Выгрузить модуль. Использование: unloadmod <название модуля>"""
        module_name, text = utils.get_module_name(args)
        
        if module_name.lower() in __system_mod__:
            return await utils.answer(
                message, self.S("system_unload_fail", module=module_name)
            )
        
        self.all_modules.unload_module(module_name)
        
        try:
            file_to_remove = f"xioca/modules/{module_name}.py"
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)
        except Exception as e:
            logging.error(f"Ошибка при удалении модуля {module_name}: {e}")

        return await utils.answer(
            message, self.S("unloaded", module=module_name, text=text)
        )

    async def ml_cmd(self, app: Client, message: types.Message, args: str):
        """Поделиться модулем"""
        if not args:
            return await utils.answer(
                message, self.S("no_args_short")
            )
        
        module_name, text = utils.get_module_name(args)
        
        try:
            file_path = f"xioca/modules/{module_name}.py"
            await utils.answer(
                message,
                chat_id=message.chat.id,
                document=True,
                response=file_path,
                caption=self.S("file_caption", module=module_name, text=text)
            )
        except Exception as e:
            logging.error(e)
            await utils.answer(
                message, self.S("file_mod_not_found")
            )
