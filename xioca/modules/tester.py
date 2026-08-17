# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import io
import logging
import time

from herokutl.tl.custom import Message

from .. import loader, utils


@loader.tds
class XiocaTesterMod(loader.Module):
    """Пинг, аптайм и логи"""

    strings = {
        "name": 'XiocaTester',
        'ping_msg': '<emoji id=5195083327597456039>🌙</emoji> Ping: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Uptime: <b>{uptime_str}</b>',
        'ping_process': '<emoji id=5195083327597456039>🌙</emoji>',
        'invalid_lvl': '❌ <b>Invalid log level</b>',
        'no_logs': '📭 <b>No logs found for this level</b>',
        'logs_caption': '📋 <b>Log level:</b> <code>{lvl}</code>',
    }

    strings_ru = {
        'ping_msg': '<emoji id=5195083327597456039>🌙</emoji> Пинг: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Прошло времени с запуска: <b>{uptime_str}</b>',
        'ping_process': '<emoji id=5195083327597456039>🌙</emoji>',
        'invalid_lvl': '❌ <b>Неверный уровень логов</b>',
        'no_logs': '📭 <b>Логи за этот период отсутствуют</b>',
        'logs_caption': '📋 <b>Логи уровня:</b> <code>{lvl}</code>',
    }

    strings_be = {
        'ping_msg': '<emoji id=5195083327597456039>🌙</emoji> Пінг: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Час працы: <b>{uptime_str}</b>',
        'ping_process': '<emoji id=5195083327597456039>🌙</emoji>',
        'invalid_lvl': '❌ <b>Няправільны ўзровень логаў</b>',
        'no_logs': '📭 <b>Логі адсутнічаюць</b>',
        'logs_caption': '📋 <b>Узровень логаў:</b> <code>{lvl}</code>',
    }

    strings_de = {
        'ping_msg': '<emoji id=5195083327597456039>🌙</emoji> Ping: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Laufzeit: <b>{uptime_str}</b>',
        'ping_process': '<emoji id=5195083327597456039>🌙</emoji>',
        'invalid_lvl': '❌ <b>Ungültiges Log-Level</b>',
        'no_logs': '📭 <b>Keine Logs gefunden</b>',
        'logs_caption': '📋 <b>Log-Level:</b> <code>{lvl}</code>',
    }

    strings_es = {
        'ping_msg': '<emoji id=5195083327597456039>🌙</emoji> Ping: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Tiempo activo: <b>{uptime_str}</b>',
        'ping_process': '<emoji id=5195083327597456039>🌙</emoji>',
        'invalid_lvl': '❌ <b>Nivel de log inválido</b>',
        'no_logs': '📭 <b>No se encontraron logs</b>',
        'logs_caption': '📋 <b>Nivel de log:</b> <code>{lvl}</code>',
    }

    strings_fr = {
        'ping_msg': '<emoji id=5195083327597456039>🌙</emoji> Ping: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Uptime: <b>{uptime_str}</b>',
        'ping_process': '<emoji id=5195083327597456039>🌙</emoji>',
        'invalid_lvl': '❌ <b>Niveau de log invalide</b>',
        'no_logs': '📭 <b>Aucun log trouvé</b>',
        'logs_caption': '📋 <b>Niveau de log:</b> <code>{lvl}</code>',
    }

    strings_it = {
        'ping_msg': '<emoji id=5195083327597456039>🌙</emoji> Ping: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Attività: <b>{uptime_str}</b>',
        'ping_process': '<emoji id=5195083327597456039>🌙</emoji>',
        'invalid_lvl': '❌ <b>Livello log non valido</b>',
        'no_logs': '📭 <b>Nessun log trovato</b>',
        'logs_caption': '📋 <b>Livello log:</b> <code>{lvl}</code>',
    }

    strings_kk = {
        'ping_msg': '<emoji id=5195083327597456039>🌙</emoji> Пинг: <b>{ms}</b> мс\n<emoji id=5431449001532594346>⚡️</emoji> Жұмыс уақыты: <b>{uptime_str}</b>',
        'ping_process': '<emoji id=5195083327597456039>🌙</emoji>',
        'invalid_lvl': '❌ <b>Қате лог деңгейі</b>',
        'no_logs': '📭 <b>Логтар табылмады</b>',
        'logs_caption': '📋 <b>Лог деңгейі:</b> <code>{lvl}</code>',
    }

    strings_uz = {
        'ping_msg': '<emoji id=5195083327597456039>🌙</emoji> Ping: <b>{ms}</b> ms\n<emoji id=5431449001532594346>⚡️</emoji> Ish vaqti: <b>{uptime_str}</b>',
        'ping_process': '<emoji id=5195083327597456039>🌙</emoji>',
        'invalid_lvl': "❌ <b>Noto'g'ri log darajasi</b>",
        'no_logs': '📭 <b>Loglar topilmadi</b>',
        'logs_caption': '📋 <b>Log darajasi:</b> <code>{lvl}</code>',
    }


    @loader.command()
    async def pingcmd(self, message: Message):
        """Показать пинг и аптайм"""
        start = time.perf_counter()
        message = await utils.answer(message, self.strings("ping_process"))
        ping = (time.perf_counter() - start) * 1000

        await utils.answer(
            message,
            self.strings("ping_msg").format(
                ms=round(ping, 3),
                uptime_str=utils.formatted_uptime(),
            ),
        )

    @loader.command()
    async def logscmd(self, message: Message):
        """<уровень> - выгрузить логи указанного уровня"""
        args = utils.get_args_raw(message).strip().upper()
        level = args or "ERROR"

        # Уровень задаётся как именем, так и числом
        if level.isdigit():
            level = int(level)
        else:
            level = getattr(logging, level, None)

        if not isinstance(level, int):
            await utils.answer(message, self.strings("invalid_lvl"))
            return

        handler = next(
            (
                h
                for h in logging.getLogger().handlers
                if hasattr(h, "dumps")
            ),
            None,
        )

        if handler is None:
            await utils.answer(message, self.strings("no_logs"))
            return

        logs = handler.dumps(level, client_id=self._client.tg_id)
        if not logs:
            await utils.answer(message, self.strings("no_logs"))
            return

        payload = io.BytesIO("\n".join(logs).encode("utf-8"))
        payload.name = f"xioca-logs-{logging.getLevelName(level).lower()}.txt"

        await utils.answer_file(
            message,
            payload,
            caption=self.strings("logs_caption").format(
                lvl=logging.getLevelName(level)
            ),
        )
