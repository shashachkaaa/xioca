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
import traceback
from typing import Union
from datetime import datetime

from loguru._better_exceptions import ExceptionFormatter
from loguru._colorizer import Colorizer
from loguru import logger
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .loader import ModulesManager
from . import utils

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
            logging.CRITICAL: "CRITICAL",
            logging.ERROR: "ERROR",
            logging.WARNING: "WARN",
            logging.INFO: "INFO",
            logging.DEBUG: "DEBUG",
        }
        self.modules_path = os.path.normpath("/root/xioca/xioca/modules/")
        self._logs_chat_id = None
        self._initialization_lock = asyncio.Lock()
        self._initialized = False
    
    async def initialize(self):
        """Инициализация обработчика с ожиданием бота"""
        if self._initialized:
            return

        for _ in range(60):
            if (hasattr(self.modules_manager, 'bot_manager') and 
                self.modules_manager.bot_manager is not None and 
                getattr(self.modules_manager.bot_manager, 'bot', None) is not None):
                break
            await asyncio.sleep(1)
            
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
   
                self.modules_manager._db.set("xioca.loader", "logs_chat", chat.id)
                self._logs_chat_id = chat.id
                logging.info(f"Создан чат для логов: {chat.id}")

                if (hasattr(self.modules_manager, 'bot_manager') and 
                    getattr(self.modules_manager.bot_manager, 'bot', None) is not None):
                    try:
                        bot_me = await self.modules_manager.bot_manager.bot.get_me()
                        await self.modules_manager._app.add_chat_members(
                            chat.id,
                            bot_me.id
                        )
                    except Exception as add_error:
                        logging.warning(f"Ошибка при добавлении бота в чат (бот запущен?): {add_error}")
                else:
                    logging.warning("Бот не был найден после ожидания. Чат логов создан без бота.")

                return chat.id
                
            except Exception as e:
                logging.error(f"Ошибка при создании чата для логов: {e}")
                self._logs_chat_id = getattr(self.modules_manager, 'me', None).id if hasattr(self.modules_manager, 'me') else None
                return self._logs_chat_id
    
    def _get_module_info(self, record):
        """Извлекает имя модуля, функцию и строку из traceback"""
        module_name = None
        func_name = record.funcName
        line_no = record.lineno

        if record.exc_info:
            _, _, tb = record.exc_info
            while tb:
                frame = tb.tb_frame
                frame_path = os.path.normpath(frame.f_code.co_filename)

                if frame_path == "<string>":
                    tb = tb.tb_next
                    continue

                if self.modules_path in frame_path:
                    rel_path = frame_path.split(self.modules_path)[1]
                    module_parts = rel_path.split(os.sep)
                    if len(module_parts) > 1:
                        module_name = module_parts[1] if module_parts[0] == "" else module_parts[0]
                    if module_name and module_name.endswith('.py'):
                        module_name = module_name[:-3]
                    
                    func_name = frame.f_code.co_name
                    line_no = tb.tb_lineno
                    return module_name, func_name, line_no
                    
                tb = tb.tb_next

        if record.pathname and record.pathname != "<string>":
            norm_path = os.path.normpath(record.pathname)
            if self.modules_path in norm_path:
                rel_path = norm_path.split(self.modules_path)[1]
                module_parts = rel_path.split(os.sep)
                if len(module_parts) > 1:
                    module_name = module_parts[1] if module_parts[0] == "" else module_parts[0]
                if module_name and module_name.endswith('.py'):
                    module_name = module_name[:-3]
                
                if module_name:
                    return module_name, func_name, line_no

        if record.name.startswith('xioca.modules.'):
            module_name = record.name.split('.')[-1]
            return module_name, func_name, line_no

        if record.exc_info and len(record.exc_info) >= 2:
            exc_value = record.exc_info[1]
            if hasattr(exc_value, '__traceback__'):
                tb = exc_value.__traceback__
                while tb:
                    frame = tb.tb_frame
                    frame_path = os.path.normpath(frame.f_code.co_filename)
                    if frame_path != "<string>" and self.modules_path in frame_path:
                        rel_path = frame_path.split(self.modules_path)[1]
                        module_parts = rel_path.split(os.sep)
                        if len(module_parts) > 1:
                            module_name = module_parts[1] if module_parts[0] == "" else module_parts[0]
                        if module_name and module_name.endswith('.py'):
                            module_name = module_name[:-3]
                        
                        func_name = frame.f_code.co_name
                        line_no = tb.tb_lineno
                        return module_name, func_name, line_no
                    
                    tb = tb.tb_next

        return None, func_name, line_no
    
    def format_log_message(self, record):
        """Форматирует сообщение лога в красивый и читаемый вид"""
        module_name, func_name, line_no = self._get_module_info(record)
        emoji = self.level_emojis.get(record.levelno, "📌")
        level_name = self.level_names.get(record.levelno, "MSG")
        
        header_parts = [f"{emoji} <b>{level_name}</b>"]
        if module_name:
            header_parts.append(f"• <code>{module_name}</code>")
        header = " ".join(header_parts)
        
        location_text = ""
        if func_name and func_name != '<module>':
            loc_str = f"{func_name}:{line_no}" if line_no else func_name
            
            url_path = None
            if record.pathname and record.pathname != "<string>":
                path = os.path.normpath(record.pathname)
                if self.modules_path in path:
                    rel_path = path.split(self.modules_path)[1]
                    url_path = f"https://xioca.ferz.live/modules{rel_path}"
            
            if url_path:
                location_text = f"📂 <a href='{url_path}'>{loc_str}</a>"
            else:
                location_text = f"📂 <code>{loc_str}</code>"

        randid = utils.random_id()
        kb = None
        
        if record.exc_info:
            exc_type, exc_value, _ = record.exc_info
            error_title = html.escape(f"{exc_type.__name__}: {exc_value}")
            message_body = f"<b>Exception occurred:</b>\n<pre>{error_title}</pre>"

            tb_text = html.escape(''.join(traceback.format_exception(*record.exc_info)))
            formatted_tb = f"🔍 <b>Traceback:</b>\n<pre>{tb_text}</pre>"
            self.modules_manager._db.set("xioca.logger", f"traceback_{randid}", formatted_tb)
            
            kb = InlineKeyboardBuilder()
            b = InlineKeyboardButton(text="🐞 Показать Traceback", callback_data=f"traceback_{randid}")
            kb.row(b)
            kb = kb.as_markup()
        else:
            raw_msg = html.escape(record.getMessage())
            message_body = f"<blockquote>{raw_msg}</blockquote>"

        lines = [header, "", message_body]
        if location_text:
            lines.extend(["", location_text])
            
        return "\n".join(lines), kb
    
    async def _send_log(self, log_message: str, kb=None):
        """Отправляет лог в чат"""
        try:
            if self._logs_chat_id is None:
                await self.initialize()
                
            if self._logs_chat_id is None:
                self.modules_manager._db.set("xioca.loader", "logs_chat", None)
                await self._get_or_create_logs_chat()
                if self._logs_chat_id is None:
                     return
            
            ignore_messages = [
                "connect",
                "networktask started",
                "pingtask started",
                "device:",
                "system:",
                "session",
                "feed_update",
                "HTTP Client says - ClientOSError",
                "polling",
                "`disable_web_page_preview` is deprecated",
                "Update id=",
                "disconnected"
            ]
            
            log_message_lower = log_message.lower()
            if any(ignore_msg.lower() in log_message_lower for ignore_msg in ignore_messages):
                return

            if (not hasattr(self.modules_manager, 'bot_manager') or 
                not hasattr(self.modules_manager.bot_manager, 'bot') or
                self.modules_manager.bot_manager.bot is None):
                return

            await self.modules_manager.bot_manager.bot.send_message(
                self._logs_chat_id,
                log_message,
                parse_mode="HTML",
                reply_markup=kb,
                disable_web_page_preview=True
            )
        except Exception as e:
            if "Flood control exceeded" in str(e) or "Too Many Requests" in str(e):
                return
            
            if any(error in str(e).lower() for error in ["chat not found", "bot was kicked from the supergroup chat"]):
                logging.error("Чат логов не найден, создаем новый...")
                
                try:
                    self.modules_manager._db.set("xioca.loader", "logs_chat", None)
                    self._logs_chat_id = None
                    await self._get_or_create_logs_chat()
                except Exception as e:
                    logging.error(f"Ошибка при создании нового чата логов: {e}")
            else:
                logging.error(f"Ошибка при отправке лога: {e}")

    def emit(self, record):
        try:
            if not hasattr(self.modules_manager, 'bot_manager') or \
               not hasattr(self.modules_manager.bot_manager, 'bot') or \
               self.modules_manager.bot_manager.bot is None:
                return
                
            if record.levelno >= logging.INFO:
                log_message, kb = self.format_log_message(record)
                asyncio.create_task(self._send_log(log_message, kb))
                
        except Exception as e:
            print(f"Ошибка в обработчике логов (emit): {e}")

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
    
    logging.basicConfig(handlers=[handler], level=level)
    
    if modules_manager is not None:
        try:
            bot_handler = BotLogHandler(modules_manager, logging.INFO)
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
