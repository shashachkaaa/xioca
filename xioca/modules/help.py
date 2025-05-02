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

from pyrogram import Client, types
from .. import loader, utils, __version__, __system_mod__


@loader.module(author="sh1tn3t | shashachkaaa")
class HelpMod(loader.Module):
    """Помощь по командам юзербота"""

    async def help_cmd(self, app: Client, message: types.Message, args: str):
        """Список всех модулей"""
        if not args:
            hide_mods = self.db.get("help", "hide_mods", [])
            
            system_modules_list = []
            user_modules_list = []
            
            for module in self.all_modules.modules:
                if module.name.lower() in hide_mods:
                    continue
                
                if module.name.lower() in __system_mod__:
                    system_modules_list.append(module)
                else:
                    user_modules_list.append(module)
            
            sorted_modules = system_modules_list + user_modules_list
            
            text = ""
            for module in sorted_modules:
                commands = []
                inline_commands = []

                if module.command_handlers:
                    commands.extend(
                        f"<code>{command}</code>" for command in module.command_handlers
                    )

                if module.inline_handlers:
                    inline_commands.extend(
                        f"🎹 <code>{inline_command}</code>" for inline_command in module.inline_handlers
                    )

                all_commands = commands + inline_commands
                if all_commands:
                    if module.name.lower() in __system_mod__:
                        text += f"\n<b>▪ {module.name}</b>: (" + " <b>|</b> ".join(all_commands) + ")"
                    else:
                        text += f"\n<b>▫ {module.name}</b>: (" + " <b>|</b> ".join(all_commands) + ")"

            return await utils.answer(
                message, f"<b><emoji id=5195083327597456039>🌙</emoji> Всего <code>{len(self.all_modules.modules)}</code> модулей, <code>{len(hide_mods)}</code> скрыто</b>\n"
                         f"{text}"
            )
        
        module_name, text = utils.get_module_name_in_modules(self, args)
        
        module = self.all_modules.get_module(module_name.lower())
      
        if not module:
            return await utils.answer(
                message, f"<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{module_name}</code>» <b>не найден</b>"
            )
        
        prefix = self.db.get("xioca.loader", "prefixes", ["."])[0]
        bot_username = (await self.bot.me()).username

        command_descriptions = "\n".join(
            f"<emoji id=5471978009449731768>👉</emoji> <code>{prefix + command}</code>\n"
            f"    ╰ {module.command_handlers[command].__doc__ or 'Нет описания для команды'}"
            for command in module.command_handlers
        )
        
        inline_descriptions = "\n".join(
            f"<emoji id=5372981976804366741>🤖</emoji> <code>@{bot_username + ' ' + command}</code>\n"
            f"    ╰ {module.inline_handlers[command].__doc__ or 'Нет описания для команды'}"
            for command in module.inline_handlers
        )

        header = (
            f"<b><emoji id=5195083327597456039>🌙</emoji> Модуль:</b> <code>{module.name}</code>\n" + (
                f"<b><emoji id=5237922302070367159>❤️</emoji> Автор:</b> <code>{module.author}</code>\n" if module.author else ""
            ) + (
                f"<b><emoji id=5226929552319594190>0️⃣</emoji> Версия:</b> <code>{module.version}</code>\n" if module.version else ""
            ) + (
                f"\n<b><emoji id=5197269100878907942>✍️</emoji> Описание:</b>\n"
                f"    ╰ {module.__doc__ or 'Нет описания для модуля'}\n\n"
            )
        )

        return await utils.answer(
            message, header + command_descriptions + "\n" + inline_descriptions + f"\n\n{text}"
        )