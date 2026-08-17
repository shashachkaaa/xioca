# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import asyncio

from herokutl.tl.custom import Message

from .. import loader, utils


@loader.tds
class XiocaTerminalMod(loader.Module):
    """Терминал с живым выводом"""

    strings = {
        "name": 'XiocaTerminal',
        'no_args': '❌ <b>Specify which command to execute</b>',
        'command': '<emoji id=5339181821135431228>💻</emoji> <b>Command:</b>\n<pre><code class="language-bash">{args}</code></pre>\n\n',
        'output': '<emoji id=5395444784611480792>✏️</emoji> <b>Output (tail):</b>\n<pre><code class="language-bash">{out}</code></pre>',
        'killed': '\n\n🚫 <b>Process killed (timeout)</b>',
        'exception': '<emoji id=5375360100196163660>🐲</emoji> <b>Exception:</b>\n<pre><code class="language-bash">{e}</code></pre>',
    }

    strings_ru = {
        'no_args': '❌ <b>Укажите, какую команду выполнить</b>',
        'command': '<emoji id=5339181821135431228>💻</emoji> <b>Команда:</b>\n<pre><code class="language-bash">{args}</code></pre>\n\n',
        'output': '<emoji id=5395444784611480792>✏️</emoji> <b>Вывод (последние строки):</b>\n<pre><code class="language-bash">{out}</code></pre>',
        'killed': '\n\n🚫 <b>Процесс остановлен (timeout)</b>',
        'exception': '<emoji id=5375360100196163660>🐲</emoji> <b>Исключение:</b>\n<pre><code class="language-bash">{e}</code></pre>',
    }

    strings_be = {
        'no_args': '❌ <b>Укажыце, якую каманду выканаць</b>',
        'command': '<emoji id=5339181821135431228>💻</emoji> <b>Каманда:</b>\n<pre><code class="language-bash">{args}</code></pre>\n\n',
        'output': '<emoji id=5395444784611480792>✏️</emoji> <b>Вывад (апошнія радкі):</b>\n<pre><code class="language-bash">{out}</code></pre>',
        'killed': '\n\n🚫 <b>Працэс спынены (timeout)</b>',
        'exception': '<emoji id=5375360100196163660>🐲</emoji> <b>Выключэнне:</b>\n<pre><code class="language-bash">{e}</code></pre>',
    }

    strings_de = {
        'no_args': '❌ <b>Geben Sie an, welcher Befehl ausgeführt werden soll</b>',
        'command': '<emoji id=5339181821135431228>💻</emoji> <b>Befehl:</b>\n<pre><code class="language-bash">{args}</code></pre>\n\n',
        'output': '<emoji id=5395444784611480792>✏️</emoji> <b>Ausgabe (Ende):</b>\n<pre><code class="language-bash">{out}</code></pre>',
        'killed': '\n\n🚫 <b>Prozess getötet (timeout)</b>',
        'exception': '<emoji id=5375360100196163660>🐲</emoji> <b>Ausnahme:</b>\n<pre><code class="language-bash">{e}</code></pre>',
    }

    strings_es = {
        'no_args': '❌ <b>Especifique qué comando ejecutar</b>',
        'command': '<emoji id=5339181821135431228>💻</emoji> <b>Comando:</b>\n<pre><code class="language-bash">{args}</code></pre>\n\n',
        'output': '<emoji id=5395444784611480792>✏️</emoji> <b>Salida (últimas líneas):</b>\n<pre><code class="language-bash">{out}</code></pre>',
        'killed': '\n\n🚫 <b>Proceso terminado (timeout)</b>',
        'exception': '<emoji id=5375360100196163660>🐲</emoji> <b>Excepción:</b>\n<pre><code class="language-bash">{e}</code></pre>',
    }

    strings_fr = {
        'no_args': '❌ <b>Précisez quelle commande exécuter</b>',
        'command': '<emoji id=5339181821135431228>💻</emoji> <b>Commande:</b>\n<pre><code class="language-bash">{args}</code></pre>\n\n',
        'output': '<emoji id=5395444784611480792>✏️</emoji> <b>Sortie (fin):</b>\n<pre><code class="language-bash">{out}</code></pre>',
        'killed': '\n\n🚫 <b>Processus terminé (timeout)</b>',
        'exception': '<emoji id=5375360100196163660>🐲</emoji> <b>Exception:</b>\n<pre><code class="language-bash">{e}</code></pre>',
    }

    strings_it = {
        'no_args': '❌ <b>Specifica quale comando eseguire</b>',
        'command': '<emoji id=5339181821135431228>💻</emoji> <b>Comando:</b>\n<pre><code class="language-bash">{args}</code></pre>\n\n',
        'output': '<emoji id=5395444784611480792>✏️</emoji> <b>Output (coda):</b>\n<pre><code class="language-bash">{out}</code></pre>',
        'killed': '\n\n🚫 <b>Processo terminato (timeout)</b>',
        'exception': '<emoji id=5375360100196163660>🐲</emoji> <b>Eccezione:</b>\n<pre><code class="language-bash">{e}</code></pre>',
    }

    strings_kk = {
        'no_args': '❌ <b>Орындалатын команданы көрсетіңіз</b>',
        'command': '<emoji id=5339181821135431228>💻</emoji> <b>Команда:</b>\n<pre><code class="language-bash">{args}</code></pre>\n\n',
        'output': '<emoji id=5395444784611480792>✏️</emoji> <b>Нәтиже (соңы):</b>\n<pre><code class="language-bash">{out}</code></pre>',
        'killed': '\n\n🚫 <b>Процесс тоқтатылды (timeout)</b>',
        'exception': '<emoji id=5375360100196163660>🐲</emoji> <b>Ерекшелік:</b>\n<pre><code class="language-bash">{e}</code></pre>',
    }

    strings_uz = {
        'no_args': "❌ <b>Qaysi buyruqni bajarishni ko'rsating</b>",
        'command': '<emoji id=5339181821135431228>💻</emoji> <b>Buyruq:</b>\n<pre><code class="language-bash">{args}</code></pre>\n\n',
        'output': '<emoji id=5395444784611480792>✏️</emoji> <b>Natija (oxiri):</b>\n<pre><code class="language-bash">{out}</code></pre>',
        'killed': "\n\n🚫 <b>Jarayon to'xtatildi (timeout)</b>",
        'exception': '<emoji id=5375360100196163660>🐲</emoji> <b>Istisno:</b>\n<pre><code class="language-bash">{e}</code></pre>',
    }


    # Обновляем сообщение не чаще, чем раз в это число секунд: правка на
    # каждый чанк вывода мгновенно упирается во FloodWait
    _EDIT_INTERVAL = 2.0
    _MAX_CHARS = 3000
    _TIMEOUT = 300

    def _render(self, command: str, output: str) -> str:
        return self.strings("command").format(
            args=utils.escape_html(command)
        ) + self.strings("output").format(out=utils.escape_html(output))

    @loader.command()
    async def terminalcmd(self, message: Message):
        """<команда> - выполнить команду в шелле"""
        command = utils.get_args_raw(message)
        if not command:
            await utils.answer(message, self.strings("no_args"))
            return

        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )
        except Exception as error:
            await utils.answer(
                message,
                self.strings("command").format(args=utils.escape_html(command))
                + self.strings("exception").format(e=utils.escape_html(str(error))),
            )
            return

        message = await utils.answer(message, self._render(command, "..."))

        output = ""
        killed = False
        loop = asyncio.get_running_loop()
        started = loop.time()
        last_edit = 0.0
        last_shown = None

        while True:
            try:
                chunk = await asyncio.wait_for(process.stdout.read(4096), timeout=1.0)
            except asyncio.TimeoutError:
                if process.returncode is not None:
                    break
                if loop.time() - started > self._TIMEOUT:
                    process.kill()
                    killed = True
                    break
                continue

            if not chunk:
                break

            output += chunk.decode("utf-8", errors="replace")
            output = output[-self._MAX_CHARS:]

            now = loop.time()
            if now - last_edit < self._EDIT_INTERVAL or output == last_shown:
                continue

            # Правку намеренно глушим: FloodWait или MessageNotModified посреди
            # стрима не должны ронять команду - финальный вывод всё равно уйдёт
            try:
                message = await utils.answer(message, self._render(command, output))
                last_edit, last_shown = now, output
            except Exception:
                last_edit = now

        await process.wait()

        text = self._render(command, output)
        if killed:
            text += self.strings("killed")

        await utils.answer(message, text)
