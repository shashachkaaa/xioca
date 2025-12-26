# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import random
import string
import logging
import os
import ast
import time

import asyncio
import functools
import importlib.util

from pyrogram.types import Message, User, Chat
from pyrogram.file_id import FileId, PHOTO_TYPES
from fuzzywuzzy import process
from aiogram.types import Message as aio_msg
from aiogram.types import (
    InlineQuery,
    InputTextMessageContent,
    InlineQueryResultArticle
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bs4 import BeautifulSoup

from types import FunctionType
from typing import Any, List, Literal, Tuple, Union, Optional

from .db import db

CORE_STRINGS = {}

def load_languages(path="xioca/langpacks"):
    """
    Загружает языковые пакеты (.py файлы) из указанной папки.
    """
    if not os.path.exists(path):
        logging.error(f"Folder {path} not found!")
        return

    for filename in os.listdir(path):
        if filename.endswith(".py") and filename != "__init__.py":
            lang_code = filename[:-3]
            file_path = os.path.join(path, filename)
            
            try:
                spec = importlib.util.spec_from_file_location(f"langpacks.{lang_code}", file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, "STRINGS"):
                    CORE_STRINGS[lang_code] = module.STRINGS
                    logging.info(f"Language loaded: {lang_code}")
                else:
                    logging.warning(f"File {filename} does not contain the STRINGS dictionary.")
            except Exception as e:
                logging.error(f"Failed to load language file {filename}: {e}")

def sys_S(key: str, **kwargs) -> str:
    """
    Глобальная функция для перевода системных сообщений.
    """
    lang = db.get("xioca.loader", "language", "en")
    
    template = CORE_STRINGS.get(lang, {}).get(key)
    
    if not template:
        template = CORE_STRINGS.get("en", {}).get(key)
    
    if not template:
        return f"<{key}>"

    try:
        return template.format(**kwargs)
    except Exception as e:
        logging.error(f"Error formatting system string '{key}': {e}")
        return template

def find_closest_module_name(module_name: str, module_list: List[str]) -> Tuple[str, str]:
    """Ищет ближайшее название модуля к введенному аргументу.

    Параметры:
        module_name (``str``):
            Введенное название модуля

        module_list (``List[str]``):
            Список всех модулей

    Возвращает:
        Tuple[str, str]: Ближайшее название модуля и текст с предупреждением
    """
    matches = process.extract(module_name, module_list, limit=3)
    
    best_module_name = []
    
    if matches[0][1] < 100:
        for best in matches:
            best_module_name.append(best[0])
    
    try:
        module_name = best_module_name[0]
        text = sys_S("best_module_name")
    except:
        module_name = matches[0][0]
        text = ''
    
    return module_name, text

def find_mod_class_in_file(file_path: str) -> Optional[str]:
    """Ищет класс, имя которого заканчивается на 'Mod', в файле."""
    
    with open(f"xioca/modules/{file_path}.py", "r", encoding="utf-8") as file:
        file_content = file.read()

    tree = ast.parse(file_content)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name.endswith("Mod"):
            return node.name

    return None

def get_module_name_in_modules(self, args):
    module_name = args
    
    module_names = [module.__class__.__name__.replace("Mod", "") for module in self.all_modules.modules]
    
    matches = process.extract(module_name, module_names, limit=3)
    
    best_module_name = []
    
    if matches[0][1] < 100:
        for best in matches:
            best_module_name.append(best[0])
    
    try:
        module_name = best_module_name[0]
        text = sys_S("best_module_name")
    except:
        module_name = args
        text = ''
    
    return module_name, text

def get_module_name(args):
    module_name = args
    
    modules_dir = "xioca/modules"
    
    try:
        module_files = [
            f for f in os.listdir(modules_dir)
            if f.endswith(".py") and not f.startswith("_")
        ]
    except FileNotFoundError:
        return None, sys_S("file_not_found")
    
    module_names = [os.path.splitext(f)[0] for f in module_files]
    
    matches = process.extract(module_name, module_names, limit=3)
    
    best_module_name = []
    
    if matches[0][1] < 100:
        for best in matches:
            best_module_name.append(best[0])
    
    try:
        module_name = best_module_name[0]
        text = sys_S("best_module_name")
    except:
        #module_name = message.text.split()[1]
        module_name = matches[0][0]
        text = ''
    
    return module_name, text
    
def get_full_command(message: Message) -> Union[
    Tuple[Literal[""], Literal[""], Literal[""]], Tuple[str, str, str]
]:
    """Вывести кортеж из префикса, команды и аргументов
    
    Параметры:
        message (``pyrogram.types.Message``):
            Сообщение
    """
    message.text = str(message.text or message.caption)
    prefixes = db.get("xioca.loader", "prefixes", ["."])

    command = ""
    args = ""
    found_prefix = ""

    for prefix in prefixes:
        if not message.text:
            continue
         
        if message.text.startswith(prefix):
            text_part = message.text[len(prefix):]
            
            current_prefix = prefix

            if text_part.startswith(prefix):
                 text_part = text_part[len(prefix):]
                 current_prefix = prefix * 2

            if not text_part:
                continue

            split_text = text_part.split(maxsplit=1)
            command = split_text[0]
            args = split_text[1] if len(split_text) > 1 else ""
            found_prefix = current_prefix
            break
    else:
        return "", "", ""
        
    return found_prefix, command.lower(), args

async def inline(
	self,
	message: Message,
	command: str = None,
	alert: bool = True
	):
		if alert:
			if message.from_user.is_premium:
				text_alert = sys_S("create_inline_form_premium")
			else:
				text_alert = sys_S("create_inline_form")
			
			await answer(message, text_alert)
			
		bot_results = await message._client.get_inline_bot_results((await self.bot.me()).username, command)
		
		try:
		    await message._client.send_inline_bot_result(
			    message.chat.id, bot_results.query_id,
			    bot_results.results[0].id
	        )
		except:
			return await answer(message, sys_S("inline_forbidden"))
		await message.delete()

async def answer_inline(
        inline_query: InlineQuery,
        message_text: str,
        title: str = "Информация",
        reply_markup: Optional[InlineKeyboardBuilder] = None,
        thumb_url: str = None,
        cache_time: int = 0,
        parse_mode: str = 'html'
    ):
    """Генерирует и отправляет inline-результат."""
    	
    message = InputTextMessageContent(message_text=message_text, parse_mode=parse_mode)
    
    markup = reply_markup.as_markup() if hasattr(reply_markup, 'as_markup') else reply_markup
    
    return await inline_query.answer(
        [
            InlineQueryResultArticle(
                id=random_id(),
                title=title,
                input_message_content=message,
                reply_markup=markup if markup else None,
                thumb_url=thumb_url,
            )
        ],
        cache_time=cache_time
    )

async def answer(
    message: Union[Message, List[Message]],
    response: Union[str, Any],
    chat_id: Union[str, int] = None,
    document: bool = False,
    photo: bool = False,
    animation: bool = False,
    video: bool = False,
    caption: str = None,
    disable_web_page_preview=False,
    **kwargs
) -> List[Message]:

    messages: List[Message] = []

    if isinstance(message, list):
        message = message[0]

    if isinstance(response, str) and all(not arg for arg in [document, photo, animation, video]):
        outputs = [
            response[i: i + 4096]
            for i in range(0, len(response), 4096)
        ]

        if chat_id:
            messages.append(
                await message._client.send_message(
                    chat_id, outputs[0], **kwargs)
            )
            await message.delete()
        else:
            messages.append(
                await (
                    message.edit if message.outgoing
                    else message.reply
                )(outputs[0], **kwargs)
            )

        for output in outputs[1:]:
            messages.append(
                await messages[0].reply(output, **kwargs)
            )

    elif document:
        if chat_id:
            messages.append(
                await message._client.send_document(
                    chat_id, response, caption=caption, **kwargs)
            )
            await message.delete()
        else:
            messages.append(
                await message.reply_document(response, caption=caption, **kwargs)
            )
            await message.delete()

    elif photo:
        if chat_id:
            messages.append(
                await message._client.send_photo(
                    chat_id, response, caption=caption, **kwargs)
            )
            await message.delete()
        else:
            messages.append(
                await message.reply_photo(response, caption=caption, **kwargs)
            )
            await message.delete()

    elif animation:
        if chat_id:
            messages.append(
                await message._client.send_animation(
                    chat_id, response, caption=caption, **kwargs)
            )
            await message.delete()
        else:
            messages.append(
                await message.reply_animation(response, caption=caption, **kwargs)
            )
            await message.delete()

    elif video:
        if chat_id:
            messages.append(
                await message._client.send_video(
                    chat_id, response, caption=caption, **kwargs)
            )
            await message.delete()
        else:
            messages.append(
                await message.reply_video(response, caption=caption, **kwargs)
            )
            await message.delete()

    return messages


def run_sync(func: FunctionType, *args, **kwargs) -> asyncio.Future:
    """Запускает асинхронно нон-асинк функцию

    Параметры:
        func (``types.FunctionType``):
            Функция для запуска

        args (``list``):
            Аргументы к функции

        kwargs (``dict``):
            Параметры к функции
    """
    return asyncio.get_event_loop().run_in_executor(
        None, functools.partial(
            func, *args, **kwargs)
    )


def get_message_media(message: Message) -> Union[str, None]:
    """Получить медиа с сообщения, если есть

    Параметры:
        message (``pyrogram.types.Message``):
            Сообщение
    """
    return getattr(message, message.media or "", None)


def get_media_ext(message: Message) -> Union[str, None]:
    """Получить расширение файла

    Параметры:
        message (``pyrogram.types.Message``):
            Сообщение
    """
    if not (media := get_message_media(message)):
        return None

    media_mime_type = getattr(media, "mime_type", "")
    extension = message._client.mimetypes.guess_extension(media_mime_type)

    if not extension:
        extension = ".unknown"
        file_type = FileId.decode(
            media.file_id).file_type

        if file_type in PHOTO_TYPES:
            extension = ".jpg"

    return extension


def get_display_name(entity: Union[User, Chat]) -> str:
    """Получить отображаемое имя

    Параметры:
        entity (``pyrogram.types.User`` | ``pyrogram.types.Chat``):
            Сущность, для которой нужно получить отображаемое имя
    """
    return getattr(entity, "title", None) or (
        entity.first_name or "" + (
            " " + entity.last_name
            if entity.last_name else ""
        )
    )


def random_id(size: int = 10) -> str:
    """Возвращает рандомный идентификатор заданной длины

    Параметры:
        size (``int``, optional):
            Длина идентификатора
    """
    return "".join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(size)
    )
