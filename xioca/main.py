# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import sys
import time
import json
import logging
import requests

from pyrogram.methods.utilities.idle import idle
from .db import db
from . import auth, loader, logger, utils

async def main():
    """Основной цикл юзербота"""
    me, app = await auth.Auth().authorize()
    await app.initialize()

    modules = loader.ModulesManager(app, db, me)
    utils.load_languages()
    
    logger.setup_logger(logging.getLevelName(logging.getLogger().level), modules)
    
    await modules.load(app)

    if (restart := db.get("xioca.restart", "restart")):
        try:
            last_time = restart["time"]
            end_time = time.time() - last_time
            hours, rem = divmod(end_time, 3600)
            minutes, seconds = divmod(rem, 60)
            text = utils.sys_S("restart_msg", sec=f"{int(seconds):2d}") if restart["type"] == "restart" else utils.sys_S("update_msg", sec=f"{int(seconds):2d}")
            id = restart["msg"].split(":")
            
            try:
            	async for dialog in app.get_dialogs(limit=20):
            		if dialog.chat.id == int(id[0]):
            			break
            except Exception as e:
            	logging.warning(e)
            
            await app.edit_message_text(int(id[0]), int(id[1]), text)
            
        except Exception as e:
            logging.warning(f"Неудалось изменить сообщение после перезагрузки: {e}")
            pass
        
        db.drop_table("xioca.restart")

    prefix = db.get("xioca.loader", "prefixes", ["."])[0]
    bot_info = await modules.bot_manager.bot.me()
    #requests.get(f"https://xioca.live/api/addstat?user_id={modules.me.id}")
    logging.info(f"Стартовал для [ID: {modules.me.id}] успешно, введи {prefix}help в чате для получения списка команд\nТвой бот: @{bot_info.username} [ID: {bot_info.id}]")

    await idle()

    logging.info("Завершение работы...")

    return True
