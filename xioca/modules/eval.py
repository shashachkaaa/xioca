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
import sys
import io
import contextlib
from meval import meval
from pyrogram import Client, types
from .. import loader, utils

def format_text_with_entities(text, entities):
    """
    Форматирует текст с учетом сущностей (entities), но только для кастомных эмодзи и жирного текста.
    """
    formatted_text = ""
    last_offset = 0

    for entity in sorted(entities, key=lambda e: e.offset):
        formatted_text += text[last_offset:entity.offset]

        if entity.type == "bold":
            formatted_text += f"<b>{text[entity.offset:entity.offset + entity.length]}</b>"
        elif entity.type == "custom_emoji":
            formatted_text += f"<emoji id={entity.custom_emoji_id}>{text[entity.offset:entity.offset + entity.length]}</emoji>"
        else:
            formatted_text += text[entity.offset:entity.offset + entity.length]

        last_offset = entity.offset + entity.length

    formatted_text += text[last_offset:]

    return formatted_text

@loader.module(author="sh1tn3t | shashachkaaa")
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
        output_print = io.StringIO()
        result_val = None

        try:
            with contextlib.redirect_stdout(output_print):
                result_val = await meval(args, globals(), **self.getattrs(app, message))
            
            print_output = html.escape(output_print.getvalue())
            result = html.escape(str(result_val))

        except Exception:
            exc_type, exc_value, tb = sys.exc_info()
            
            error_line = "".join(traceback.format_exception_only(exc_type, exc_value)).strip()
            
            stack_summary = traceback.extract_tb(tb)
            formatted_stack = []
            
            for frame in stack_summary[2:]: 
                filename = frame.filename
                if 'lib/python' in filename:
                    filename = '.../' + '/'.join(filename.split('/')[-3:])
                elif 'xioca' in filename:
                    try:
                        filename = '/'.join(filename.split('/xioca/')[1:])
                    except Exception:
                        pass

                formatted_stack.append(f"👉 {filename}:{frame.lineno} в {frame.name}")
            
            stack_str = "\n".join(formatted_stack)
            
            output = f"{stack_str}\n\n🚫 {error_line}"

            return await utils.answer(
                message, f"""<emoji id=5339181821135431228>💻</emoji> <b>Код:</b>
<pre><code class="language-python">{args}</code></pre>

<emoji id=5210952531676504517>❌</emoji> <b>Ошибка:</b>
<pre><code class="language-error">{html.escape(output)}</code></pre>"""
            )

        if return_it:
            output = f"""<emoji id=5339181821135431228>💻</emoji> <b>Код:</b>
<pre><code class="language-python">{args}</code></pre>"""

            if result_val is not None:
                output += f"""

<emoji id=5175061663237276437>🐍</emoji> <b>Вывод:</b>
<pre><code class="language-bash">{result}</code></pre>"""

            if print_output:
                output += f"""

<emoji id=5339181821135431228>⌨️</emoji> <b>Вывод:</b>
<pre><code class="language-python">{print_output}</code></pre>"""
            
            await utils.answer(message, output)

    def getattrs(self, app: Client, message: types.Message):
        """
        Возвращает атрибуты для выполнения кода, включая форматированный текст.
        """
        reply = message.reply_to_message
        if reply and reply.text:
            formatted_text = format_text_with_entities(reply.text, reply.entities)
            return {
                "self": self,
                "db": self.db,
                "app": app,
                "message": message,
                "chat": message.chat,
                "user": message.from_user,
                "reply": reply,
                "r": reply,
                "ruser": getattr(reply, "from_user", None),
                "rtext": formatted_text
            }
        return {
            "self": self,
            "db": self.db,
            "app": app,
            "message": message,
            "chat": message.chat,
            "user": message.from_user,
            "reply": reply,
            "r": reply,
            "ruser": getattr(reply, "from_user", None)
        }