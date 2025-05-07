#    Sh1t-UB (telegram userbot by sh1tn3t)
#    Copyright (C) 2021-2022 Sh1tN3t

import logging
from typing import Optional, Tuple

from pyrogram import Client, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .. import loader, utils, __version__, __system_mod__


@loader.module(author="sh1tn3t | shashachkaaa")
class HelpMod(loader.Module):
    """Помощь по командам юзербота"""

    async def _generate_modules_page(
        self, 
        page: int = 0, 
        page_size: int = 20
    ) -> Tuple[str, Optional[InlineKeyboardBuilder]]:
        """Генерирует страницу с модулями и клавиатурой пагинации."""
        hide_mods = self.db.get("help", "hide_mods", [])
        
        system_modules = []
        user_modules = []
        
        for module in self.all_modules.modules:
            if module.name.lower() in hide_mods:
                continue
            
            if module.name.lower() in __system_mod__:
                system_modules.append(module)
            else:
                user_modules.append(module)
        
        sorted_modules = system_modules + user_modules
        total_modules = len(sorted_modules)
        total_pages = (total_modules + page_size - 1) // page_size
        
        page = max(0, min(page, total_pages - 1))
        start_idx = page * page_size
        end_idx = min(start_idx + page_size, total_modules)
        modules_page = sorted_modules[start_idx:end_idx]
        modules_shown = len(modules_page)
        
        text_lines = []
        for module in modules_page:
            commands = []
            if module.command_handlers:
                commands.extend(f"<code>{cmd}</code>" for cmd in module.command_handlers)
            
            inline_commands = []
            if module.inline_handlers:
                inline_commands.extend(f"🎹 <code>{cmd}</code>" for cmd in module.inline_handlers)
            
            if commands or inline_commands:
                prefix = "▪" if module.name.lower() in __system_mod__ else "▫"
                all_commands = " | ".join(commands + inline_commands)
                text_lines.append(f"\n<b>{prefix} {module.name}</b>: ({all_commands})")
        
        header = (
            "<b>🌙 Всего <code>{}</code> модулей, "
            "<code>{}</code> скрыто, "
            "<code>{}</code> отображено</b>\n"
        ).format(
            len(self.all_modules.modules),
            len(hide_mods),
            modules_shown
        )
        
        text = header + "".join(text_lines)
        
        if total_pages > 1:
            builder = InlineKeyboardBuilder()
            if page > 0:
                builder.button(text="⬅️ Назад", callback_data=f"help_prev_{page}")
            builder.button(text=f"{page + 1}/{total_pages}", callback_data="help_page")
            if page < total_pages - 1:
                builder.button(text="Вперёд ➡️", callback_data=f"help_next_{page}")
            builder.adjust(3)
            return text, builder
        
        return text, None

    async def help_cmd(self, app: Client, message: types.Message, args: str):
        """Список всех модулей"""
        if not args:
            text, keyboard = await self._generate_modules_page(page_size=self.db.get("xioca.help", "maxmods", 20))
            
            if keyboard:
                return await utils.inline(self, message, "help page_0")
            return await utils.answer(message, text)
        
        module_name, text = utils.get_module_name_in_modules(self, args)
        module = self.all_modules.get_module(module_name.lower())
      
        if not module:
            return await utils.answer(
                message, 
                "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{}</code>» <b>не найден</b>".format(module_name))
        
        prefix = self.db.get("xioca.loader", "prefixes", ["."])[0]
        bot_username = (await self.bot.me()).username

        command_descriptions = []
        for command in module.command_handlers:
            desc = module.command_handlers[command].__doc__ or "Нет описания"
            command_descriptions.append(
                "<emoji id=5471978009449731768>👉</emoji> <code>{}</code>\n    ╰ {}".format(prefix + command, desc))
        
        inline_descriptions = []
        for command in module.inline_handlers:
            desc = module.inline_handlers[command].__doc__ or "Нет описания"
            inline_descriptions.append(
                "<emoji id=5372981976804366741>🤖</emoji> <code>@{} {}</code>\n    ╰ {}".format(bot_username, command, desc))

        header_parts = [
            "<b><emoji id=5195083327597456039>🌙</emoji> Модуль:</b> <code>{}</code>\n".format(module.name)]
        if module.author:
            header_parts.append("<b><emoji id=5237922302070367159>❤️</emoji> Автор:</b> <code>{}</code>\n".format(module.author))
        if module.version:
            header_parts.append("<b><emoji id=5226929552319594190>0️⃣</emoji> Версия:</b> <code>{}</code>\n".format(module.version))
        
        header_parts.extend([
            "\n<b><emoji id=5197269100878907942>✍️</emoji> Описание:</b>\n",
            "    ╰ {}\n\n".format(module.__doc__ or "Нет описания")])
        
        return await utils.answer(
            message, 
            "".join(header_parts) + "\n".join(command_descriptions) + "\n" + "\n".join(inline_descriptions) + "\n\n" + text)

    async def help_inline_handler(self, app: Client, inline_query: types.InlineQuery, args: str):
        """Обработчик инлайн-команды help"""
        if not args.startswith("page_"):
            return await utils.answer_inline(
                inline_query,
                "Используйте: @бот help [страница]",
                "Помощь по командам")
        
        try:
            page = int(args.split("_")[1])
        except (IndexError, ValueError):
            page = 0
            
        text, keyboard = await self._generate_modules_page(page, self.db.get("xioca.help", "maxmods", 20))
        if not text:
            return await utils.answer_inline(
                inline_query,
                "Не удалось загрузить список модулей",
                "Ошибка")
            
        await utils.answer_inline(
            inline_query,
            text,
            "Список модулей",
            reply_markup=keyboard)

    async def help_callback_handler(self, app: Client, call: types.CallbackQuery):
        """Обработчик кнопок пагинации"""
        if not call.data.startswith(("help_prev_", "help_next_")):
            return await call.answer()
            
        try:
            current_page = int(call.data.split("_")[-1])
            page = current_page - 1 if "prev" in call.data else current_page + 1
        except (IndexError, ValueError):
            page = 0
            
        text, keyboard = await self._generate_modules_page(page, self.db.get("xioca.help", "maxmods", 20))
        if not text:
            return await call.answer("Ошибка загрузки страницы", show_alert=True)
            
        await self.bot.edit_message_text(
            inline_message_id=call.inline_message_id,
            text=text,
            reply_markup=keyboard.as_markup() if keyboard else None)
        await call.answer()