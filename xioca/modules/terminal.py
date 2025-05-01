import subprocess
from pyrogram import Client, types
from .. import loader, utils


@loader.module(author="shashachkaaa")
class TerminalMod(loader.Module):
    """Терминал"""

    async def terminal_cmd(self, app: Client, message: types.Message, args: str):
        """Выполнение команд"""
        if not args:
            return await utils.answer(message, "❌ <b>Укажите, какую команду выполнить</b>")

        try:
            process = subprocess.Popen(args.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()

            result = (
                f"<emoji id=5339181821135431228>💻</emoji> <b>Команда:</b>\n```bash\n{args}```\n\n"
                f"<emoji id=5395444784611480792>✏️</emoji> <b>Вывод:</b>\n```bash\n{output.decode()}```"
            )

            if error:
                result += f"\n\n❌ <b>Ошибка:</b>\n```bash\n{error.decode()}```"

        except Exception as e:
            result = (
                f"<emoji id=5339181821135431228>💻</emoji> <b>Команда:</b>\n```bash\n{args}```\n\n"
                f"<emoji id=5375360100196163660>🐲</emoji> <b>Исключение:</b>\n```bash\n{e}```"
            )

        await utils.answer(message, result)