# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import io
import logging
import time

from datetime import datetime
from pyrogram import Client, types

from .. import loader, utils, logger, __start_time__


@loader.module(author="sh1tn3t | shashachkaaa")
class TesterMod(loader.Module):
    """Модуль для тестирования и логов"""
    
    strings = {
        "ru": {
            "ping_msg": "<emoji id=5195083327597456039>🌙</emoji> Пинг: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Прошло времени с запуска: <b>{uptime_str}</b>",
            "ping_process": "<emoji id=5195083327597456039>🌙</emoji>",
            "invalid_lvl": "❌ <b>Неверный уровень логов</b>",
            "no_logs": "📭 <b>Логи за этот период отсутствуют</b>",
            "logs_caption": "📋 <b>Логи уровня:</b> <code>{lvl}</code>"
        },
        "en": {
            "ping_msg": "<emoji id=5195083327597456039>🌙</emoji> Ping: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Uptime: <b>{uptime_str}</b>",
            "ping_process": "<emoji id=5195083327597456039>🌙</emoji>",
            "invalid_lvl": "❌ <b>Invalid log level</b>",
            "no_logs": "📭 <b>No logs found for this level</b>",
            "logs_caption": "📋 <b>Log level:</b> <code>{lvl}</code>"
        },
        "be": {
            "ping_msg": "<emoji id=5195083327597456039>🌙</emoji> Пінг: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Час працы: <b>{uptime_str}</b>",
            "ping_process": "<emoji id=5195083327597456039>🌙</emoji>",
            "invalid_lvl": "❌ <b>Няправільны ўзровень логаў</b>",
            "no_logs": "📭 <b>Логі адсутнічаюць</b>",
            "logs_caption": "📋 <b>Узровень логаў:</b> <code>{lvl}</code>"
        },
        "de": {
            "ping_msg": "<emoji id=5195083327597456039>🌙</emoji> Ping: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Laufzeit: <b>{uptime_str}</b>",
            "ping_process": "<emoji id=5195083327597456039>🌙</emoji>",
            "invalid_lvl": "❌ <b>Ungültiges Log-Level</b>",
            "no_logs": "📭 <b>Keine Logs gefunden</b>",
            "logs_caption": "📋 <b>Log-Level:</b> <code>{lvl}</code>"
        },
        "es": {
            "ping_msg": "<emoji id=5195083327597456039>🌙</emoji> Ping: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Tiempo activo: <b>{uptime_str}</b>",
            "ping_process": "<emoji id=5195083327597456039>🌙</emoji>",
            "invalid_lvl": "❌ <b>Nivel de log inválido</b>",
            "no_logs": "📭 <b>No se encontraron logs</b>",
            "logs_caption": "📋 <b>Nivel de log:</b> <code>{lvl}</code>"
        },
        "fr": {
            "ping_msg": "<emoji id=5195083327597456039>🌙</emoji> Ping: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Uptime: <b>{uptime_str}</b>",
            "ping_process": "<emoji id=5195083327597456039>🌙</emoji>",
            "invalid_lvl": "❌ <b>Niveau de log invalide</b>",
            "no_logs": "📭 <b>Aucun log trouvé</b>",
            "logs_caption": "📋 <b>Niveau de log:</b> <code>{lvl}</code>"
        },
        "it": {
            "ping_msg": "<emoji id=5195083327597456039>🌙</emoji> Ping: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Attività: <b>{uptime_str}</b>",
            "ping_process": "<emoji id=5195083327597456039>🌙</emoji>",
            "invalid_lvl": "❌ <b>Livello log non valido</b>",
            "no_logs": "📭 <b>Nessun log trovato</b>",
            "logs_caption": "📋 <b>Livello log:</b> <code>{lvl}</code>"
        },
        "kk": {
            "ping_msg": "<emoji id=5195083327597456039>🌙</emoji> Пинг: <b>{ms}</b> мс\n<emoji id=5431449001532594346>⚡️</emoji> Жұмыс уақыты: <b>{uptime_str}</b>",
            "ping_process": "<emoji id=5195083327597456039>🌙</emoji>",
            "invalid_lvl": "❌ <b>Қате лог деңгейі</b>",
            "no_logs": "📭 <b>Логтар табылмады</b>",
            "logs_caption": "📋 <b>Лог деңгейі:</b> <code>{lvl}</code>"
        },
        "uz": {
            "ping_msg": "<emoji id=5195083327597456039>🌙</emoji> Ping: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Ish vaqti: <b>{uptime_str}</b>",
            "ping_process": "<emoji id=5195083327597456039>🌙</emoji>",
            "invalid_lvl": "❌ <b>Noto'g'ri log darajasi</b>",
            "no_logs": "📭 <b>Loglar topilmadi</b>",
            "logs_caption": "📋 <b>Log darajasi:</b> <code>{lvl}</code>"
        }
    }

    async def ping_cmd(self, app: Client, message: types.Message, args: str):
        """Пингует и показывает аптайм"""
        start = time.time()
        m = await utils.answer(message, self.S("ping_process"))
        
        if m:
            end = time.time()
            uptime = datetime.now() - __start_time__
            uptime_str = str(uptime).split('.')[0]

            response = self.S(
                "ping_msg", 
                ms=round((end - start) * 1000, 3), 
                uptime_str=uptime_str
            )
            return await utils.answer(message, response)

    async def logs_cmd(self, app: Client, message: types.Message, args: str):
        """Отправляет логи. Использование: .logs <уровень>"""
        lvl_name = args.strip().upper() if args else "ERROR"
        lvl = logger.get_valid_level(lvl_name)

        if not lvl:
            return await utils.answer(message, self.S("invalid_lvl"))

        handler = logging.getLogger().handlers[0]
        logs_list = handler.dumps(lvl)
        
        if not logs_list:
            return await utils.answer(message, self.S("no_logs"))

        logs = ("\n".join(logs_list)).encode("utf-8")
        
        with io.BytesIO(logs) as out:
            out.name = f"logs_{lvl_name}.txt"
            await app.send_document(
                message.chat.id, 
                out, 
                caption=self.S("logs_caption", lvl=lvl_name)
            )
            await message.delete()
