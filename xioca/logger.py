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

import logging
import asyncio
import html
import os
import inspect
import traceback
from typing import Union
from datetime import datetime

from loguru._better_exceptions import ExceptionFormatter
from loguru._colorizer import Colorizer
from loguru import logger

from .loader import ModulesManager

FORMAT_FOR_FILES = (
    "{time:%Y-%m-%d %H:%M:%S} | "
    "{level: <8} | "
    "{name}:{function}:{line} - {message}"
)

def get_valid_level(level: Union[str, int]):
    return (
        int(level) if level.isdigit()
        else getattr(logging, level.upper(), None)
    )

class LogFilter(logging.Filter):
    def filter(self, record):
        # Игнорируем логи обработки обновлений aiogram
        if record.name == "aiogram.dispatcher.dispatcher" and \
           record.funcName == "feed_update" and \
           "Update id=" in record.getMessage():
            return False
            
        # Игнорируем логи подключения Pyrogram
        pyrogram_ignore_messages = [
            "Connecting...",
            "Connected! Production",
            "NetworkTask started",
            "PingTask started",
            "Session started",
            "Device:",
            "System:",
            "Session initialized:"
        ]
        
        if record.name.startswith("pyrogram.") and \
           any(msg in record.getMessage() for msg in pyrogram_ignore_messages):
            return False
            
        return True

class BotLogHandler(logging.Handler):
    """Обработчик для отправки логов через бота"""
    
    def __init__(self, modules_manager: ModulesManager, level=logging.NOTSET):
        super().__init__(level)
        self.modules_manager = modules_manager
        self.level_emojis = {
            logging.CRITICAL: "🚨",
            logging.ERROR: "⛔", 
            logging.WARNING: "⚠️",
            logging.INFO: "ℹ️",
            logging.DEBUG: "🐛",
        }
        self.level_names = {
            logging.CRITICAL: "КРИТИЧЕСКАЯ ОШИБКА",
            logging.ERROR: "ОШИБКА",
            logging.WARNING: "ПРЕДУПРЕЖДЕНИЕ",
            logging.INFO: "ИНФОРМАЦИЯ",
            logging.DEBUG: "ОТЛАДКА",
        }
        self.modules_path = os.path.normpath("/root/xioca/xioca/modules/")
        self._logs_chat_id = None
        self._initialization_lock = asyncio.Lock()
        self._initialized = False
    
    async def initialize(self):
        """Инициализация обработчика"""
        if self._initialized:
            return
            
        try:
            await self._get_or_create_logs_chat()
            self._initialized = True
        except Exception as e:
            logging.error(f"Ошибка инициализации BotLogHandler: {e}")
            self._logs_chat_id = getattr(self.modules_manager, 'me', None).id if hasattr(self.modules_manager, 'me') else None
    
    async def _get_or_create_logs_chat(self):
        """Получает или создает чат для логов"""
        async with self._initialization_lock:
            if self._logs_chat_id is not None:
                return self._logs_chat_id
                
            logs_chat = self.modules_manager._db.get("xioca.loader", "logs_chat", None)
            
            if logs_chat is not None:
                self._logs_chat_id = logs_chat
                return self._logs_chat_id
                
            try:
                if not hasattr(self.modules_manager, '_app'):
                    raise RuntimeError("App not initialized")
                    
                chat = await self.modules_manager._app.create_supergroup(
                    f"Xioca Logs [{self.modules_manager.me.id}]"
                )
                if not hasattr(self.modules_manager, 'bot_manager') or not hasattr(self.modules_manager.bot_manager, 'bot'):
                    raise RuntimeError("Bot not initialized")
                    
                bot_me = await self.modules_manager.bot_manager.bot.get_me()
                try:
                    await self.modules_manager._app.add_chat_members(
                        chat.id,
                        bot_me.id
                    )
                except Exception as add_error:
                    logging.error(f"Ошибка при добавлении бота в чат: {add_error}")
                self.modules_manager._db.set("xioca.loader", "logs_chat", chat.id)
                self._logs_chat_id = chat.id
                
                logging.info(f"Создан чат для логов: {chat.id}")
                return chat.id
                
            except Exception as e:
                logging.error(f"Ошибка при создании чата для логов: {e}")
                self._logs_chat_id = getattr(self.modules_manager, 'me', None).id if hasattr(self.modules_manager, 'me') else None
                return self._logs_chat_id
    
    def _get_module_name(self, record):
        """Извлекает имя модуля из записи лога"""
        if record.name.startswith('xioca.modules.'):
            return record.name.split('.')[-1]
        
        if record.pathname:
            norm_path = os.path.normpath(record.pathname)
            if self.modules_path in norm_path:
                rel_path = norm_path.split(self.modules_path)[1]
                module_name = rel_path.split(os.sep)[0]
                if module_name.endswith('.py'):
                    return module_name[:-3]
                return module_name
        
        if record.exc_info:
            tb = record.exc_info[2]
            while tb and tb.tb_next:
                tb = tb.tb_next
            
            if tb:
                frame = tb.tb_frame
                if 'self' in frame.f_locals:
                    instance = frame.f_locals['self']
                    module = getattr(instance, '__module__', '')
                    if module.startswith('xioca.modules.'):
                        return module.split('.')[-1]
                
                tb_path = os.path.normpath(tb.tb_frame.f_code.co_filename)
                if self.modules_path in tb_path:
                    rel_path = tb_path.split(self.modules_path)[1]
                    module_name = rel_path.split(os.sep)[0]
                    if module_name.endswith('.py'):
                        return module_name[:-3]
                    return module_name
        
        return None
    
    def format_log_message(self, record):
        """Форматирует сообщение лога в красивый вид"""
        module_name = self._get_module_name(record)
        emoji = self.level_emojis.get(record.levelno, "📌")
        level_name = self.level_names.get(record.levelno, "СООБЩЕНИЕ")
        
        lines = [
            f"{emoji} <b>{level_name}</b>",
        ]
        
        if module_name:
            lines.append(f"📦 <b>Модуль:</b> <code>{module_name}</code>")
        elif record.pathname:
            path = os.path.normpath(record.pathname)
            lines.append(f"📁 <b>Файл:</b>\n<code>{html.escape(path)}</code>")
        
        if record.funcName and record.funcName != '<module>':
            lines.append(f"🔧 <b>Функция:</b> <code>{record.funcName}</code>")
        
        if record.lineno:
            lines.append(f"🎯 <b>Строка:</b> <code>{record.lineno}</code>")
        
        message = html.escape(record.getMessage())
        lines.append(f"📝 <b>Сообщение:</b>\n<code>{message}</code>")
        
        if record.exc_info:
            exc_type, exc_value, _ = record.exc_info
            exc_text = html.escape(f"{exc_type.__name__}: {exc_value}")
            lines.append(f"💥 <b>Ошибка:</b>\n<code>{exc_text}</code>")
            tb_text = html.escape(''.join(traceback.format_exception(*record.exc_info)))
            lines.append(f"🔍 <b>Traceback:</b>\n<code>{tb_text}</code>")
        
        return "\n".join(lines)
    
    async def _send_log(self, log_message: str):
        """Отправляет лог в чат"""
        try:
            if self._logs_chat_id is None:
                await self.initialize()
                
            if self._logs_chat_id is None:
                logging.error("Не удалось определить чат для логов")
                return
                
            await self.modules_manager.bot_manager.bot.send_message(
                self._logs_chat_id,
                log_message,
                parse_mode="HTML"
            )
        except Exception as e:
            if "Flood control exceeded" in str(e) or "Too Many Requests" in str(e):
            	return
            logging.error(f"Ошибка при отправке лога: {e}")

    def emit(self, record):
        try:
            if not hasattr(self.modules_manager, 'bot_manager') or \
               not hasattr(self.modules_manager.bot_manager, 'bot') or \
               self.modules_manager.bot_manager.bot is None:
                return
                
            if record.levelno >= logging.INFO:
                log_message = self.format_log_message(record)
                asyncio.create_task(self._send_log(log_message))
                
        except Exception as e:
            logging.error(f"Ошибка в обработчике логов: {e}")

class StreamHandler(logging.Handler):
    """Обработчик логирования в поток"""

    def __init__(self, lvl: int = logging.INFO):
        super().__init__(lvl)

    def format(self, record: logging.LogRecord):
        """Форматирует логи под нужный формат"""
        exception_lines = ""
        stripped_formatter = Colorizer.prepare_format(
            FORMAT_FOR_FILES + "{exception}"
        ).strip()

        if record.exc_info:
            exception_formatter = ExceptionFormatter(
                encoding="utf8", backtrace=True, prefix="\n",
                hidden_frames_filename=logger.catch.__code__.co_filename
            )

            type_, value, tb = record.exc_info
            exception_list = exception_formatter.format_exception(type_, value, tb)
            exception_lines = "".join(exception_list)

        return stripped_formatter.format(
            time=datetime.fromtimestamp(record.created), level=record.levelname,
            name=record.name, function=record.funcName, message=record.msg,
            line=record.lineno, exception=exception_lines
        )

class MemoryHandler(logging.Handler):
    """Обработчик логирования в память"""

    def __init__(self, lvl: int = logging.INFO):
        super().__init__(0)
        self.target = StreamHandler(lvl)
        self.lvl = lvl

        self.capacity = 500
        self.buffer = []
        self.handled_buffer = []

    def dumps(self, lvl: int):
        """Возвращает список всех входящих логов по минимальному уровню"""
        sorted_logs = list(
            filter(
                lambda record: record.levelno >= lvl, self.handled_buffer)
        )
        self.handled_buffer = list(set(self.handled_buffer) ^ set(sorted_logs))
        return map(self.target.format, sorted_logs)

    def emit(self, record: logging.LogRecord):
        """Логирует"""
        if len(self.buffer + self.handled_buffer) >= self.capacity:
            if self.handled_buffer:
                del self.handled_buffer[0]
            else:
                del self.buffer[0]

        self.buffer.append(record)
        if record.levelno >= self.lvl >= 0:
            self.acquire()
            try:
                try:
                    level = logger.level(record.levelname).name
                except ValueError:
                    level = record.levelno

                frame, depth = logging.currentframe(), 2
                while frame.f_code.co_filename == logging.__file__:
                    frame = frame.f_back
                    depth += 1

                logger.opt(depth=depth, exception=record.exc_info).log(
                    level, record.getMessage())

                self.handled_buffer = self.handled_buffer[-(self.capacity - len(self.buffer)):] + self.buffer
                self.buffer = []
            finally:
                self.release()

def setup_logger(level: Union[str, int], modules_manager: ModulesManager = None):
    """Установка логирования"""
    level = get_valid_level(level) or 20
    handler = MemoryHandler(level)
    
    handler.addFilter(LogFilter())
    logging.basicConfig(handlers=[handler], level=level)
    
    if modules_manager is not None and hasattr(modules_manager, 'bot_manager'):
        try:
            bot_handler = BotLogHandler(modules_manager, logging.INFO)
            bot_handler.addFilter(LogFilter())
            logging.getLogger().addHandler(bot_handler)
            asyncio.create_task(bot_handler.initialize())
        except Exception as e:
            logging.error(f"Ошибка при инициализации BotLogHandler: {e}")

    for ignore in [
        "pyrogram.session",
        "pyrogram.connection", 
        "pyrogram.methods.utilities.idle"
    ]:
        logger.disable(ignore)