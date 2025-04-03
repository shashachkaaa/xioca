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
import inspect

from aiogram.types import (
    Message,
    CallbackQuery,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from .types import Item
from .. import utils


class Events(Item):
    """Обработчик событий"""

    async def _message_handler(self, message: Message) -> Message:
        """Обработчик сообщений"""
        for func in self._all_modules.message_handlers.values():
            if not await self._check_filters(func, func.__self__, message):
                continue

            try:
                await func(self._app, message)
            except Exception as error:
                logging.exception(error)

        return message

    async def _callback_handler(self, call: CallbackQuery) -> CallbackQuery:
        """Обработчик каллбек-хендлеров"""
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
                        	title="🚫 Доступ запрещен",
                        	input_message_content=InputTextMessageContent(
                            	message_text=(
	                                "😎 Это - <code>Xioca</code>. Отличный юзербот с большим количеством команд и модулей к нему.\n\n"
                                "❓ 	<b>Как установить?</b>\n"
                                	"Для <b>установки</b> воспользуйтесь <a href='https://xioca.live'>сайтом</a>.\n\n"
                                	"🌟 <b>Особенности:</b>\n"
                                	"- Удобное управление через команды.\n"
                                	"- Поддержка инлайн-режима.\n"
                                	"- Модульная архитектура для расширения функционала.\n"
                                	"- Регулярные обновления и поддержка.\n\n"
                                	"📚 <b>Документация:</b>\n"
                                	"Подробнее о возможностях и настройке можно узнать в <a href='https://github.com/shashachkaaa/Xioca'>документации</a>.\n\n"
                                	"🛠 <b>Поддержка:</b>\n"
                                	"Если у вас возникли вопросы, обратитесь в <a href='https://t.me/XiocaUB'>чат поддержки</a>."
                            	),
                            	parse_mode="HTML",
                            	disable_web_page_preview=True
                        	),
                        	description="Узнайте больше о Xioca и как ее установить.",
                        	thumb_url="https://api.fl1yd.su/emoji/1f6ab.png"
                    	)
                	], cache_time=0
            	)

        if not (query := inline_query.query):
            commands = ""
            for command, func in self._all_modules.inline_handlers.items():
                if await self._check_filters(func, func.__self__, inline_query):
                    commands += f"\n💬 <code>@{(await self.bot.me()).username} {command}</code>"

            message = InputTextMessageContent(
                message_text=f"👇 <b>Доступные команды</b>\n{commands}",
                parse_mode="HTML"
            )

            return await inline_query.answer(
                [
                    InlineQueryResultArticle(
                        id=utils.random_id(),
                        title="Доступные команды",
                        input_message_content=message,
                        thumb_url="https://api.fl1yd.su/emoji/1f4ac.png",
                    )
                ], cache_time=0
            )

        query_ = query.split()

        cmd = query_[0]
        args = " ".join(query_[1:])

        func = self._all_modules.inline_handlers.get(cmd)
        if not func:
            return await inline_query.answer(
                [
                    InlineQueryResultArticle(
                        id=utils.random_id(),
                        title="Ошибка",
                        input_message_content=InputTextMessageContent(
                            message_text="❌ Такой инлайн-команды нет"
                        ),
                        thumb_url="https://api.fl1yd.su/emoji/274c.png"
                    )
                ], cache_time=0
            )

        if not await self._check_filters(func, func.__self__, inline_query):
            return

        try:
            if (
                len(vars_ := inspect.getfullargspec(func).args) > 3
                and vars_[3] == "args"
            ):
                await func(self._app, inline_query, args)
            else:
                await func(self._app, inline_query)
        except Exception as error:
            logging.exception(error)

        return inline_query