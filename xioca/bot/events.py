# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import logging
import inspect

from aiogram.types import (
    Message,
    CallbackQuery,
    InlineQuery,
    ChosenInlineResult,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InlineQueryResultVideo,
    InlineQueryResultGif,
    InlineQueryResultDocument,
    InputTextMessageContent,
    InlineKeyboardButton,
)

from aiogram.utils.keyboard import InlineKeyboardBuilder


from .types import Item
from .. import utils, inline_stash


class Events(Item):
    """Обработчик событий"""

    async def _message_handler(self, message: Message) -> Message:
        """Обработчик сообщений"""
        for name, func in self._all_modules.message_handlers.items():
            if name == "chosen_inline_result":
                continue

            if not await self._check_filters(func, func.__self__, message):
                continue

            try:
                await func(self._app, message)
            except Exception as error:
                logging.exception(error)

        return message

    async def _callback_handler(self, call: CallbackQuery):
        """Обработчик каллбек-хендлеров"""

        allowed = set(self._db.get("xioca.loader", "allow", []))
        try:
            allowed = {int(x) for x in allowed}
        except Exception:
            allowed = set()

        owner_id = self._all_modules.me.id
        user_id = call.from_user.id if call.from_user else None

        if user_id not in {owner_id, *allowed}:
            try:
                await call.answer("⛔", show_alert=True)
            except Exception:
                pass
            return None

        for func in self._all_modules.callback_handlers.values():
            if not await self._check_filters(func, func.__self__, call):
                continue

            try:
                await func(self._app, call)
            except Exception as error:
                logging.exception(error)

        return call

    async def _inline_handler(self, inline_query: InlineQuery) -> InlineQuery:
        """Обработчик инлайн-хендеров"""
        ids = self._db.get("xioca.loader", "allow", [])
        if inline_query.from_user.id != self._all_modules.me.id:
            if inline_query.from_user.id not in ids:
                return await inline_query.answer(
                    [
                        InlineQueryResultArticle(
                            id=utils.random_id(),
                            title=utils.sys_S("inline_bot_forbidden"),
                            input_message_content=InputTextMessageContent(
                                message_text=utils.sys_S("inline_info"),
                                parse_mode="HTML",
                                disable_web_page_preview=True,
                            ),
                            description=utils.sys_S("inline_description"),
                            thumb_url="https://api.fl1yd.su/emoji/1f6ab.png",
                        )
                    ],
                    cache_time=0,
                )

        if not (query := inline_query.query):
            commands = ""
            for command, func in self._all_modules.inline_handlers.items():
                if await self._check_filters(func, func.__self__, inline_query):
                    commands += f"\n💬 <code>@{(await self.bot.me()).username} {command}</code>"

            message = InputTextMessageContent(
                message_text=utils.sys_S("inline_commands", commands=commands),
                parse_mode="HTML",
            )

            return await inline_query.answer(
                [
                    InlineQueryResultArticle(
                        id=utils.random_id(),
                        title=utils.sys_S("commands_title"),
                        input_message_content=message,
                        thumb_url="https://api.fl1yd.su/emoji/1f4ac.png",
                    )
                ],
                cache_time=0,
            )

        query_ = query.split()

        cmd = query_[0]
        args = " ".join(query_[1:])

        if cmd == "xiocaform":
            token = (args or "").strip()
            payload = inline_stash.pop(token) if token else None

            if not payload:
                return await inline_query.answer(
                    [
                        InlineQueryResultArticle(
                            id=utils.random_id(),
                            title=utils.sys_S("inline_error"),
                            input_message_content=InputTextMessageContent(
                                message_text=utils.sys_S("inline_not_found"),
                                parse_mode="HTML",
                                disable_web_page_preview=True,
                            ),
                            thumb_url="https://api.fl1yd.su/emoji/274c.png",
                        )
                    ],
                    cache_time=0,
                )
            kb = None
            buttons = payload.get("buttons") or []
            if buttons:
                if isinstance(buttons, dict):
                    buttons = [[buttons]]
                elif isinstance(buttons, list) and buttons and isinstance(buttons[0], dict):
                    buttons = [[b] for b in buttons]

                builder = InlineKeyboardBuilder()
                for row in buttons:
                    if isinstance(row, dict):
                        row = [row]
                    row_buttons = []
                    for btn in (row or []):
                        if not isinstance(btn, dict):
                            continue
                        text = btn.get("text") or btn.get("label") or ""
                        if not text:
                            continue

                        url = btn.get("url")
                        cb = btn.get("callback") or btn.get("callback_data") or btn.get("data")

                        siq = btn.get("switch_inline_query")
                        siqcc = btn.get("switch_inline_query_current_chat")

                        if url:
                            row_buttons.append(InlineKeyboardButton(text=text, url=url))
                        elif siqcc is not None:
                            row_buttons.append(
                                InlineKeyboardButton(
                                    text=text,
                                    switch_inline_query_current_chat=str(siqcc),
                                )
                            )
                        elif siq is not None:
                            row_buttons.append(
                                InlineKeyboardButton(
                                    text=text,
                                    switch_inline_query=str(siq),
                                )
                            )
                        else:
                            row_buttons.append(
                                InlineKeyboardButton(
                                    text=text,
                                    callback_data=str(cb or "noop"),
                                )
                            )

                    if row_buttons:
                        builder.row(*row_buttons)

                kb = builder.as_markup()

            title = payload.get("title") or "Xioca"
            description = payload.get("description") or ""

            text = payload.get("text") or ""
            disable_wpp = bool(payload.get("disable_web_page_preview", True))

            photo = payload.get("photo")
            video = payload.get("video")
            animation = payload.get("animation")
            document = payload.get("document")
            caption = payload.get("caption") or text

            result_id = utils.random_id()

            if photo:
                result = InlineQueryResultPhoto(
                    id=result_id,
                    title=title,
                    description=description,
                    photo_url=photo,
                    thumbnail_url=photo,
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=kb,
                )
            elif video:
                result = InlineQueryResultVideo(
                    id=result_id,
                    title=title,
                    description=description,
                    video_url=video,
                    mime_type="video/mp4",
                    thumbnail_url=payload.get("thumb") or "https://api.fl1yd.su/emoji/1f39e.png",
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=kb,
                )
            elif animation:
                result = InlineQueryResultGif(
                    id=result_id,
                    title=title,
                    gif_url=animation,
                    thumbnail_url=payload.get("thumb") or "https://api.fl1yd.su/emoji/1f39e.png",
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=kb,
                )
            elif document:
                result = InlineQueryResultDocument(
                    id=result_id,
                    title=title,
                    document_url=document,
                    mime_type=payload.get("mime_type") or "application/octet-stream",
                    description=description,
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=kb,
                )
            else:
                result = InlineQueryResultArticle(
                    id=result_id,
                    title=title,
                    description=description,
                    input_message_content=InputTextMessageContent(
                        message_text=text,
                        parse_mode="HTML",
                        disable_web_page_preview=disable_wpp,
                    ),
                    reply_markup=kb,
                    thumb_url=payload.get("thumb") or "https://api.fl1yd.su/emoji/1f4dd.png",
                )

            return await inline_query.answer([result], cache_time=0)


        func = self._all_modules.inline_handlers.get(cmd)
        if not func:
            return await inline_query.answer(
                [
                    InlineQueryResultArticle(
                        id=utils.random_id(),
                        title=utils.sys_S("inline_error"),
                        input_message_content=InputTextMessageContent(
                            message_text=utils.sys_S("inline_not_found")
                        ),
                        thumb_url="https://api.fl1yd.su/emoji/274c.png",
                    )
                ],
                cache_time=0,
            )

        if not await self._check_filters(func, func.__self__, inline_query):
            return inline_query

        try:
            if len(vars_ := inspect.getfullargspec(func).args) > 3 and vars_[3] == "args":
                await func(self._app, inline_query, args)
            else:
                await func(self._app, inline_query)
        except Exception as error:
            logging.exception(error)

        return inline_query

    async def _chosen_inline_result_handler(self, chosen: ChosenInlineResult) -> ChosenInlineResult:
        """
        Обработчик выбранного inline-результата (ChosenInlineResult)
        """
        try:
            logging.warning(
                "[chosen_inline_result] from=%s result_id=%s query=%r",
                getattr(getattr(chosen, "from_user", None), "id", None),
                getattr(chosen, "result_id", None),
                getattr(chosen, "query", None),
            )

            ids = self._db.get("xioca.loader", "allow", [])
            uid = getattr(getattr(chosen, "from_user", None), "id", None)

            if uid != self._all_modules.me.id and uid not in ids:
                return chosen

            for name, func in list(self._all_modules.message_handlers.items()):
                if name == "chosen_inline_result" or getattr(func, "__name__", "") == "chosen_inline_result_message_handler":
                    try:
                        await func(self._app, chosen)
                    except Exception as error:
                        logging.exception(error)

            return chosen

        except Exception as error:
            logging.exception(error)
            return chosen