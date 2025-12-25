# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import subprocess
from pyrogram import Client, types
from .. import loader, utils


@loader.module(author="shashachkaaa")
class TerminalMod(loader.Module):
    """Терминал"""

    strings = {
        "ru": {
            "no_args": "❌ <b>Укажите, какую команду выполнить</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Команда:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Вывод:</b>\n```bash\n{out}```",
            "error": "\n\n❌ <b>Ошибка:</b>\n```bash\n{err}```",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Исключение:</b>\n```bash\n{e}```"
        },
        "en": {
            "no_args": "❌ <b>Specify which command to execute</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Command:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Output:</b>\n```bash\n{out}```",
            "error": "\n\n❌ <b>Error:</b>\n```bash\n{err}```",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Exception:</b>\n```bash\n{e}```"
        },
        "be": {
            "no_args": "❌ <b>Укажыце, якую каманду выканаць</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Каманда:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Вывад:</b>\n```bash\n{out}```",
            "error": "\n\n❌ <b>Памылка:</b>\n```bash\n{err}```",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Выключэнне:</b>\n```bash\n{e}```"
        },
        "de": {
            "no_args": "❌ <b>Geben Sie an, welcher Befehl ausgeführt werden soll</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Befehl:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Ausgabe:</b>\n```bash\n{out}```",
            "error": "\n\n❌ <b>Fehler:</b>\n```bash\n{err}```",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Ausnahme:</b>\n```bash\n{e}```"
        },
        "es": {
            "no_args": "❌ <b>Especifique qué comando ejecutar</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Comando:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Salida:</b>\n```bash\n{out}```",
            "error": "\n\n❌ <b>Error:</b>\n```bash\n{err}```",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Excepción:</b>\n```bash\n{e}```"
        },
        "fr": {
            "no_args": "❌ <b>Précisez quelle commande exécuter</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Commande:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Sortie:</b>\n```bash\n{out}```",
            "error": "\n\n❌ <b>Erreur:</b>\n```bash\n{err}```",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Exception:</b>\n```bash\n{e}```"
        },
        "it": {
            "no_args": "❌ <b>Specifica quale comando eseguire</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Comando:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Output:</b>\n```bash\n{out}```",
            "error": "\n\n❌ <b>Errore:</b>\n```bash\n{err}```",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Eccezione:</b>\n```bash\n{e}```"
        },
        "kk": {
            "no_args": "❌ <b>Орындалатын команданы көрсетіңіз</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Команда:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Нәтиже:</b>\n```bash\n{out}```",
            "error": "\n\n❌ <b>Қате:</b>\n```bash\n{err}```",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Ерекшелік:</b>\n```bash\n{e}```"
        },
        "uz": {
            "no_args": "❌ <b>Qaysi buyruqni bajarishni ko'rsating</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Buyruq:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Natija:</b>\n```bash\n{out}```",
            "error": "\n\n❌ <b>Xato:</b>\n```bash\n{err}```",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Istisno:</b>\n```bash\n{e}```"
        }
    }

    async def terminal_cmd(self, app: Client, message: types.Message, args: str):
        """Выполнение команд"""
        if not args:
            return await utils.answer(message, self.S("no_args"))

        try:
            process = subprocess.Popen(args.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()

            result = (
                self.S("command", args=args) +
                self.S("output", out=output.decode())
            )

            if error:
                result += self.S("error", err=error.decode())

        except Exception as e:
            result = (
                self.S("command", args=args) +
                self.S("exception", e=e)
            )

        await utils.answer(message, result)