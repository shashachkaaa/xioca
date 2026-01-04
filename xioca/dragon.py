# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import sys
import os
import traceback
import asyncio
import importlib
import subprocess
import logging
from PIL import Image
from .db import db

from io import BytesIO
from pyrogram import Client, types, errors

modules_help = {}

requirements_list = []
interact_with_to_delete = []

git_id = "Custom"

class PrefixWrapper(str):
    def __new__(cls):
        current_prefix = db.get("xioca.loader", "prefixes", ["."])[0]
        return super().__new__(cls, current_prefix)

    def __repr__(self):
        return self

    def __str__(self):
        return self

prefix = PrefixWrapper()

def import_library(library_name: str, package_name: str = None):
    """
    Эмуляция функции import_library из Dragon.
    """
    package_name = package_name or library_name
    try:
        return importlib.import_module(library_name)
    except ImportError:
        logging.info(f"[DragonCompat] Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            importlib.invalidate_caches()
            return importlib.import_module(library_name)
        except Exception as e:
            logging.error(f"[DragonCompat] Failed to install {package_name}: {e}")
            return None

def resize_image(
    input_img, output=None, img_type="PNG", size: int = 512, size2: int = None
):
    if output is None:
        output = BytesIO()
        output.name = f"sticker.{img_type.lower()}"

    with Image.open(input_img) as img:
        if size2 is not None:
            size = (size, size2)
        elif img.width == img.height:
            size = (size, size)
        elif img.width < img.height:
            size = (max(size * img.width // img.height, 1), size)
        else:
            size = (size, max(size * img.height // img.width, 1))

        img.resize(size).save(output, img_type)

    return output

def text(message: types.Message) -> str:
    """Find text in `types.Message` object"""
    return message.text if message.text else message.caption


def restart() -> None:
    if "LAVHOST" in os.environ:
        os.system("lavhost restart")
    else:
        os.execvp(sys.executable, [sys.executable, "main.py"])


def format_exc(e: Exception, suffix="") -> str:
    traceback.print_exc()
    if isinstance(e, errors.RPCError):
        return (
            f"<b>Telegram API error!</b>\n"
            f"<code>[{e.CODE} {e.ID or e.NAME}] — {e.MESSAGE.format(value=e.value)}</code>\n\n<b>{suffix}</b>"
        )
    return (
        f"<b>Error!</b>\n"
        f"<code>{e.__class__.__name__}: {e}</code>\n\n<b>{suffix}</b>"
    )


def with_reply(func):
    async def wrapped(client: Client, message: types.Message):
        if not message.reply_to_message:
            await message.edit("<b>Reply to message is required</b>")
        else:
            return await func(client, message)

    return wrapped


async def interact_with(message: types.Message) -> types.Message:
    """
    Check history with bot and return bot's response

    Example:
    .. code-block:: python
        bot_msg = await interact_with(await bot.send_message("@BotFather", "/start"))
    :param message: already sent message to bot
    :return: bot's response
    """

    await asyncio.sleep(1)
    response = [
        msg
        async for msg in message._client.get_chat_history(
            message.chat.id, limit=1
        )
    ]
    seconds_waiting = 0

    while response[0].from_user.is_self:
        seconds_waiting += 1
        if seconds_waiting >= 5:
            raise RuntimeError("bot didn't answer in 5 seconds")

        await asyncio.sleep(1)
        response = [
            msg
            async for msg in message._client.get_chat_history(
                message.chat.id, limit=1
            )
        ]

    interact_with_to_delete.append(message.id)
    interact_with_to_delete.append(response[0].id)

    return response[0]

def register_compat():
    """
    Регистрирует текущий файл как 'utils.misc', 'utils.scripts' и 'utils.db'.
    """
    if "utils" not in sys.modules:
        sys.modules["utils"] = sys.modules[__name__]
    
    sys.modules["utils.misc"] = sys.modules[__name__]
    sys.modules["utils.scripts"] = sys.modules[__name__]
    sys.modules["utils.db"] = sys.modules[__name__]
