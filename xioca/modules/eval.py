# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import contextlib
import io
import sys
import traceback

from herokutl.tl.custom import Message
from meval import meval

from .. import loader, utils


@loader.tds
class XiocaEvalMod(loader.Module):
    """Выполняет python-код"""

    strings = {
        "name": "XiocaEval",
        "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Nothing to execute</b>",
        "code": (
            "<emoji id=5339181821135431228>💻</emoji> <b>Code:</b>\n"
            '<pre><code class="language-python">{code}</code></pre>'
        ),
        "result": (
            "\n\n<emoji id=5175061663237276437>🐍</emoji> <b>Result:</b>\n"
            '<pre><code class="language-python">{result}</code></pre>'
        ),
        "stdout": (
            "\n\n<emoji id=5339181821135431228>⌨️</emoji> <b>Output:</b>\n"
            '<pre><code class="language-python">{output}</code></pre>'
        ),
        "error": (
            "\n\n<emoji id=5210952531676504517>❌</emoji> <b>Error:</b>\n"
            '<pre><code class="language-python">{error}</code></pre>'
        ),
    }

    strings_ru = {
        "no_args": "<emoji id=5210952531676504517>❌</emoji> <b>Нечего выполнять</b>",
        "code": (
            "<emoji id=5339181821135431228>💻</emoji> <b>Код:</b>\n"
            '<pre><code class="language-python">{code}</code></pre>'
        ),
        "result": (
            "\n\n<emoji id=5175061663237276437>🐍</emoji> <b>Результат:</b>\n"
            '<pre><code class="language-python">{result}</code></pre>'
        ),
        "stdout": (
            "\n\n<emoji id=5339181821135431228>⌨️</emoji> <b>Вывод:</b>\n"
            '<pre><code class="language-python">{output}</code></pre>'
        ),
        "error": (
            "\n\n<emoji id=5210952531676504517>❌</emoji> <b>Ошибка:</b>\n"
            '<pre><code class="language-python">{error}</code></pre>'
        ),
    }

    def _globals(self, message: Message) -> dict:
        """Что доступно внутри выполняемого кода"""
        reply = None

        return {
            "self": self,
            "message": message,
            "client": self._client,
            "app": self._client,
            "db": self._db,
            "chat": message.chat if hasattr(message, "chat") else None,
            "utils": utils,
            "loader": loader,
            "reply": reply,
            "r": reply,
        }

    async def _run(self, message: Message, show_result: bool):
        code = utils.get_args_raw(message)
        if not code:
            await utils.answer(message, self.strings("no_args"))
            return

        text = self.strings("code").format(code=utils.escape_html(code))

        env = self._globals(message)
        reply = await message.get_reply_message()
        env["reply"] = env["r"] = reply
        env["ruser"] = getattr(reply, "sender", None)

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                result = await meval(code, globals(), **env)
        except Exception:
            # Кадры самого исполнителя пользователю не нужны - показываем
            # только то, что относится к его коду
            exc_type, exc_value, tb = sys.exc_info()
            frames = traceback.extract_tb(tb)[1:]

            trace = "\n".join(
                f"👉 {frame.filename}:{frame.lineno} in {frame.name}"
                for frame in frames
            )
            reason = "".join(
                traceback.format_exception_only(exc_type, exc_value)
            ).strip()

            await utils.answer(
                message,
                text
                + self.strings("error").format(
                    error=utils.escape_html(f"{trace}\n\n{reason}" if trace else reason)
                ),
            )
            return

        if not show_result:
            return

        output = stdout.getvalue()

        if result is not None:
            text += self.strings("result").format(
                result=utils.escape_html(str(result))
            )

        if output:
            text += self.strings("stdout").format(output=utils.escape_html(output))

        await utils.answer(message, text)

    @loader.command()
    async def execcmd(self, message: Message):
        """<код> - выполнить python-код без вывода результата"""
        await self._run(message, show_result=False)

    @loader.command()
    async def evalcmd(self, message: Message):
        """<код> - выполнить python-код и показать результат"""
        await self._run(message, show_result=True)
