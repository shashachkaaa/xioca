# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import asyncio
import html
from pyrogram import Client, types, errors
from .. import loader, utils


@loader.module(author="shashachkaaa")
class TerminalMod(loader.Module):
    """Терминал"""

    strings = {
        "ru": {
            "no_args": "❌ <b>Укажите, какую команду выполнить</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Команда:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Вывод (последние строки):</b>\n```bash\n{out}```",
            "killed": "\n\n🚫 <b>Процесс остановлен (timeout)</b>",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Исключение:</b>\n```bash\n{e}```"
        },
        "en": {
            "no_args": "❌ <b>Specify which command to execute</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Command:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Output (tail):</b>\n```bash\n{out}```",
            "killed": "\n\n🚫 <b>Process killed (timeout)</b>",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Exception:</b>\n```bash\n{e}```"
        },
        "be": {
            "no_args": "❌ <b>Укажыце, якую каманду выканаць</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Каманда:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Вывад (апошнія радкі):</b>\n```bash\n{out}```",
            "killed": "\n\n🚫 <b>Працэс спынены (timeout)</b>",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Выключэнне:</b>\n```bash\n{e}```"
        },
        "de": {
            "no_args": "❌ <b>Geben Sie an, welcher Befehl ausgeführt werden soll</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Befehl:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Ausgabe (Ende):</b>\n```bash\n{out}```",
            "killed": "\n\n🚫 <b>Prozess getötet (timeout)</b>",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Ausnahme:</b>\n```bash\n{e}```"
        },
        "es": {
            "no_args": "❌ <b>Especifique qué comando ejecutar</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Comando:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Salida (últimas líneas):</b>\n```bash\n{out}```",
            "killed": "\n\n🚫 <b>Proceso terminado (timeout)</b>",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Excepción:</b>\n```bash\n{e}```"
        },
        "fr": {
            "no_args": "❌ <b>Précisez quelle commande exécuter</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Commande:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Sortie (fin):</b>\n```bash\n{out}```",
            "killed": "\n\n🚫 <b>Processus terminé (timeout)</b>",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Exception:</b>\n```bash\n{e}```"
        },
        "it": {
            "no_args": "❌ <b>Specifica quale comando eseguire</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Comando:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Output (coda):</b>\n```bash\n{out}```",
            "killed": "\n\n🚫 <b>Processo terminato (timeout)</b>",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Eccezione:</b>\n```bash\n{e}```"
        },
        "kk": {
            "no_args": "❌ <b>Орындалатын команданы көрсетіңіз</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Команда:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Нәтиже (соңы):</b>\n```bash\n{out}```",
            "killed": "\n\n🚫 <b>Процесс тоқтатылды (timeout)</b>",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Ерекшелік:</b>\n```bash\n{e}```"
        },
        "uz": {
            "no_args": "❌ <b>Qaysi buyruqni bajarishni ko'rsating</b>",
            "command": "<emoji id=5339181821135431228>💻</emoji> <b>Buyruq:</b>\n```bash\n{args}```\n\n",
            "output": "<emoji id=5395444784611480792>✏️</emoji> <b>Natija (oxiri):</b>\n```bash\n{out}```",
            "killed": "\n\n🚫 <b>Jarayon to'xtatildi (timeout)</b>",
            "exception": "<emoji id=5375360100196163660>🐲</emoji> <b>Istisno:</b>\n```bash\n{e}```"
        }
    }

    async def terminal_cmd(self, app: Client, message: types.Message, args: str):
        """<команда> - Выполнение команд (живой вывод)"""
        if not args:
            return await utils.answer(message, self.S("no_args"))

        try:
            process = await asyncio.create_subprocess_shell(
                args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )

            output_buffer = ""
            
            update_interval = 2.0
            last_update = 0
            MAX_CHARS = 3000
            
            await utils.answer(message, self.S("command", args=html.escape(args)) + 
                                        self.S("output", out="..."))

            start_time = asyncio.get_running_loop().time()
            timeout = 300

            while True:
                try:
                    chunk = await asyncio.wait_for(process.stdout.read(4096), timeout=1.0)
                except asyncio.TimeoutError:
                    if process.returncode is not None:
                        break
                    if asyncio.get_running_loop().time() - start_time > timeout:
                        process.kill()
                        output_buffer += self.S("killed")
                        break
                    continue
                
                if not chunk:
                    break

                decoded_chunk = chunk.decode('utf-8', errors='replace')
                
                output_buffer += decoded_chunk
                
                if len(output_buffer) > MAX_CHARS:
                    output_buffer = output_buffer[-MAX_CHARS:]
                
                current_time = asyncio.get_running_loop().time()
                if current_time - last_update > update_interval:
                    try:
                        await utils.answer(message, 
                            self.S("command", args=html.escape(args)) +
                            self.S("output", out=html.escape(output_buffer))
                        )
                        last_update = current_time
                    except errors.MessageNotModified:
                        pass
                    except errors.FloodWait:
                        pass

            final_text = (
                self.S("command", args=html.escape(args)) +
                self.S("output", out=html.escape(output_buffer))
            )
            await utils.answer(message, final_text)

        except Exception as e:
            result = (
                self.S("command", args=html.escape(args)) +
                self.S("exception", e=html.escape(str(e)))
            )
            await utils.answer(message, result)