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

import sys
import time
import json
import logging
import requests

from pyrogram.methods.utilities.idle import idle
from .db import db
from . import auth, loader, logger

async def main():
    """Основной цикл юзербота"""
    me, app = await auth.Auth().authorize()
    await app.initialize()

    modules = loader.ModulesManager(app, db, me)
    
    logger.setup_logger(logging.getLevelName(logging.getLogger().level), modules)
    
    await modules.load(app)

    if (restart := db.get("xioca.restart", "restart")):
        try:
            last_time = restart["time"]
            end_time = time.time() - last_time
            hours, rem = divmod(end_time, 3600)
            minutes, seconds = divmod(rem, 60)
            text = f"<emoji id=5195083327597456039>🌙</emoji> <code>Xioca</code> <b>полностью перезагружена!</b>\n<emoji id=5386367538735104399>⌛</emoji> <b>Перезагрузка заняла <code>{int(seconds):2d}</code> сек.</b>" if restart["type"] == "restart" else f"<emoji id=5195083327597456039>🌙</emoji> <b>Xioca успешно обновлена!</b>\n<emoji id=5386367538735104399>⌛</emoji> <b>Обновление заняло <code>{int(seconds):2d}</code> сек.</b>"
            id = restart["msg"].split(":")
            await app.edit_message_text(int(id[0]), int(id[1]), text)
            
        except Exception as e:
            logging.warning(f"Неудалось изменить сообщение после перезагрузки: {e}")
            pass
        
        db.drop_table("xioca.restart")

    prefix = db.get("xioca.loader", "prefixes", ["."])[0]
    bot_info = await modules.bot_manager.bot.me()
    requests.get(f"https://xioca.live/api/addstat?user_id={modules.me.id}")
    logging.info(f"Стартовал для [ID: {modules.me.id}] успешно, введи {prefix}help в чате для получения списка команд\nТвой бот: @{bot_info.username} [ID: {bot_info.id}]")

    await idle()

    logging.info("Завершение работы...")
    return True