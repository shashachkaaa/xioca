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

import random
import string
import logging
import os
import ast
import time

import asyncio
import functools

from pyrogram.types import Message, User, Chat
from pyrogram.file_id import FileId, PHOTO_TYPES
from fuzzywuzzy import process

from types import FunctionType
from typing import Any, List, Literal, Tuple, Union, Optional

from .db import db

import os
from fuzzywuzzy import process

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
        text = '<emoji id=5312383351217201533>⚠️</emoji> <b>Точного совпадения не найдено, поэтому применен ближайший результат</b>'
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

def get_module_name_in_modules(self, message: Message):
    module_name = message.text.split()[1]
    
    module_names = [module.__class__.__name__.replace("Mod", "") for module in self.all_modules.modules]
    
    matches = process.extract(module_name, module_names, limit=3)
    
    best_module_name = []
    
    if matches[0][1] < 100:
        for best in matches:
            best_module_name.append(best[0])
    
    try:
        module_name = best_module_name[0]
        text = '<emoji id=5312383351217201533>⚠️</emoji> <b>Точного совпадения не найдено, поэтому применен ближайший результат</b>'
    except:
        module_name = message.text.split()[1]
        text = ''
    
    return module_name, text

def get_module_name(message: Message):
    module_name = message.text.split()[1]
    
    modules_dir = "xioca/modules"
    
    try:
        module_files = [
            f for f in os.listdir(modules_dir)
            if f.endswith(".py") and not f.startswith("_")
        ]
    except FileNotFoundError:
        return None, "<emoji id=5210952531676504517>❌</emoji> <b>Папка modules не найдена</b>"
    
    module_names = [os.path.splitext(f)[0] for f in module_files]
    
    matches = process.extract(module_name, module_names, limit=3)
    
    best_module_name = []
    
    if matches[0][1] < 100:
        for best in matches:
            best_module_name.append(best[0])
    
    try:
        module_name = best_module_name[0]
        text = '<emoji id=5312383351217201533>⚠️</emoji> <b>Точного совпадения не найдено, поэтому применен ближайший результат</b>'
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

    for prefix in prefixes:
        if (
            message.text
            and len(message.text) > len(prefix)
            and message.text.startswith(prefix)
        ):
            command, *args = message.text[len(prefix):].split(maxsplit=1)
            break
    else:
        return "", "", ""

    return prefixes[0], command.lower(), args[-1] if args else ""


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
