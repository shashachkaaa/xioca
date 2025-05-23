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

import io
import logging
import time

from datetime import datetime
from pyrogram import Client, types

from .. import loader, utils, logger, __start_time__


@loader.module(author="sh1tn3t | shashachkaaa")
class TesterMod(loader.Module):
    """Тест чего-то"""

    async def ping_cmd(self, app: Client, message: types.Message, args: str):
        """Пингует"""
        a = time.time()
        m = await utils.answer(message, f"<emoji id=5195083327597456039>🌙</emoji>")
        if m:
        	b = time.time()
        	uptime = datetime.now() - __start_time__
        	uptime_str = str(uptime).split('.')[0]
        	return await utils.answer(message, f'<emoji id=5195083327597456039>🌙</emoji> Пинг: <b>{round((b - a) * 1000, 3)}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Прошло времени с момента запуска: <b>{uptime_str}</b>')

    async def logs_cmd(self, app: Client, message: types.Message, args: str):
        """Отправляет логи. Использование: logs <уровень>"""
        lvl = 40  # ERROR

        if args and not (lvl := logger.get_valid_level(args)):
            return await utils.answer(
                message, "❌ Неверный уровень логов")

        handler = logging.getLogger().handlers[0]
        logs = ("\n".join(handler.dumps(lvl))).encode("utf-8")
        if not logs:
            return await utils.answer(
                message, f"❕ Нет логов на уровне {lvl} ({logging.getLevelName(lvl)})")

        logs = io.BytesIO(logs)
        logs.name = "xioca.txt"

        await message.delete()
        return await utils.answer(
            message, logs, document=True, quote=False,
            caption=f"📤 Xioca Логи с {lvl} ({logging.getLevelName(lvl)}) уровнем"
        )
