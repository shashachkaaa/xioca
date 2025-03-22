#    Sh1t-UB (telegram userbot by sh1tn3t)
#    Copyright (C) 2021-2022 Sh1tN3t

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import traceback
import html

from meval import meval
from pyrogram import Client, types

from .. import loader, utils


@loader.module(name="Executor", author="sh1tn3t | shashachkaaa")
class EvaluatorMod(loader.Module):
    """Выполняет python-код"""

    async def exec_cmd(self, app: Client, message: types.Message, args: str):
        """Выполнить python-код"""
        return await self.execute(app, message, args)

    async def eval_cmd(self, app: Client, message: types.Message, args: str):
        """Выполнить python-код и возвратить результат"""
        return await self.execute(app, message, args, True)

    async def execute(
        self,
        app: Client,
        message: types.Message,
        args: str,
        return_it: bool = False
    ):
        """Выполняет код"""
        try:
            result = html.escape(
                str(
                    await meval(args, globals(), **self.getattrs(app, message)))
            )
        except Exception:
            return await utils.answer(
                message, f"""<emoji id=5339181821135431228>💻</emoji> <b>Код:</b>
<code>{args}</code>

<emoji id=5210952531676504517>❌</emoji> <b>Вывод:</b>
<code>{html.escape(traceback.format_exc())}</code>"""
            )

        if return_it:
            output = (f"""<emoji id=5339181821135431228>💻</emoji> <b>Код:</b>
<code>{args}</code>

<emoji id=5175061663237276437>🐍</emoji> <b>Вывод:</b>
<code>{result}</code>"""
            )
            outputs = [output[i: i + 4083] for i in range(0, len(output), 4083)]

            await utils.answer(message, f"{outputs[0]}</code>")
            for output in outputs[1:]:
                await message.reply(f"<code>{output}</code>")

    def getattrs(self, app: Client, message: types.Message):
        return {
            "self": self,
            "db": self.db,
            "app": app,
            "message": message,
            "chat": message.chat,
            "user": message.from_user,
            "reply": message.reply_to_message,
            "r": message.reply_to_message,
            "ruser": getattr(message.reply_to_message, "from_user", None)
        }
