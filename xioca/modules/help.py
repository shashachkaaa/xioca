# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import logging
from typing import Optional, Tuple

from pyrogram import Client, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .. import loader, utils, __version__, __system_mod__


@loader.module(author="sh1tn3t | shashachkaaa")
class HelpMod(loader.Module):
    """Помощь по командам юзербота"""

    strings = {
        "ru": {
            "module_row": "\n<b>{prefix} {module}</b>: ({cmds})",
            "header_stats": "<b>🌙 Всего <code>{total}</code> модулей, <code>{hidden}</code> скрыто, <code>{shown}</code> отображено</b>\n",
            "btn_back": "⬅️ Назад",
            "btn_next": "Вперёд ➡️",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>не найден</b>",
            "no_desc": "Нет описания",
            "cmd_fmt": "<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}",
            "inline_fmt": "<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}",
            "header_mod": "<b><emoji id=5195083327597456039>🌙</emoji> Модуль:</b> <code>{mod}</code>\n",
            "header_auth": "<b><emoji id=5237922302070367159>❤️</emoji> Автор:</b> <code>{auth}</code>\n",
            "header_ver": "<b><emoji id=5226929552319594190>0️⃣</emoji> Версия:</b> <code>{ver}</code>\n",
            "header_desc": "\n<b><emoji id=5197269100878907942>✍️</emoji> Описание:</b>\n    ╰ {desc}\n\n",
            "inline_usage": "Используйте: @бот help [страница]",
            "inline_title": "Помощь по командам",
            "err_load": "Не удалось загрузить список модулей",
            "err_title": "Ошибка",
            "mod_list": "Список модулей",
            "err_page": "Ошибка загрузки страницы"
        },
        "en": {
            "module_row": "\n<b>{prefix} {module}</b>: ({cmds})",
            "header_stats": "<b>🌙 Total <code>{total}</code> modules, <code>{hidden}</code> hidden, <code>{shown}</code> shown</b>\n",
            "btn_back": "⬅️ Back",
            "btn_next": "Next ➡️",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Module</b> «<code>{mod}</code>» <b>not found</b>",
            "no_desc": "No description",
            "cmd_fmt": "<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}",
            "inline_fmt": "<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}",
            "header_mod": "<b><emoji id=5195083327597456039>🌙</emoji> Module:</b> <code>{mod}</code>\n",
            "header_auth": "<b><emoji id=5237922302070367159>❤️</emoji> Author:</b> <code>{auth}</code>\n",
            "header_ver": "<b><emoji id=5226929552319594190>0️⃣</emoji> Version:</b> <code>{ver}</code>\n",
            "header_desc": "\n<b><emoji id=5197269100878907942>✍️</emoji> Description:</b>\n    ╰ {desc}\n\n",
            "inline_usage": "Use: @bot help [page]",
            "inline_title": "Command Help",
            "err_load": "Failed to load module list",
            "err_title": "Error",
            "mod_list": "Module List",
            "err_page": "Error loading page"
        },
        "be": {
            "module_row": "\n<b>{prefix} {module}</b>: ({cmds})",
            "header_stats": "<b>🌙 Усяго <code>{total}</code> модуляў, <code>{hidden}</code> схавана, <code>{shown}</code> адлюстравана</b>\n",
            "btn_back": "⬅️ Назад",
            "btn_next": "Наперад ➡️",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>не знойдзены</b>",
            "no_desc": "Няма апісання",
            "cmd_fmt": "<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}",
            "inline_fmt": "<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}",
            "header_mod": "<b><emoji id=5195083327597456039>🌙</emoji> Модуль:</b> <code>{mod}</code>\n",
            "header_auth": "<b><emoji id=5237922302070367159>❤️</emoji> Аўтар:</b> <code>{auth}</code>\n",
            "header_ver": "<b><emoji id=5226929552319594190>0️⃣</emoji> Версія:</b> <code>{ver}</code>\n",
            "header_desc": "\n<b><emoji id=5197269100878907942>✍️</emoji> Апісанне:</b>\n    ╰ {desc}\n\n",
            "inline_usage": "Выкарыстоўвайце: @бот help [старонка]",
            "inline_title": "Дапамога па камандах",
            "err_load": "Не ўдалося загрузіць спіс модуляў",
            "err_title": "Памылка",
            "mod_list": "Спіс модуляў",
            "err_page": "Памылка загрузкі старонкі"
        },
        "de": {
            "module_row": "\n<b>{prefix} {module}</b>: ({cmds})",
            "header_stats": "<b>🌙 Insgesamt <code>{total}</code> Module, <code>{hidden}</code> versteckt, <code>{shown}</code> angezeigt</b>\n",
            "btn_back": "⬅️ Zurück",
            "btn_next": "Weiter ➡️",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Modul</b> «<code>{mod}</code>» <b>nicht gefunden</b>",
            "no_desc": "Keine Beschreibung",
            "cmd_fmt": "<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}",
            "inline_fmt": "<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}",
            "header_mod": "<b><emoji id=5195083327597456039>🌙</emoji> Modul:</b> <code>{mod}</code>\n",
            "header_auth": "<b><emoji id=5237922302070367159>❤️</emoji> Autor:</b> <code>{auth}</code>\n",
            "header_ver": "<b><emoji id=5226929552319594190>0️⃣</emoji> Version:</b> <code>{ver}</code>\n",
            "header_desc": "\n<b><emoji id=5197269100878907942>✍️</emoji> Beschreibung:</b>\n    ╰ {desc}\n\n",
            "inline_usage": "Verwendung: @bot help [Seite]",
            "inline_title": "Befehlshilfe",
            "err_load": "Modulliste konnte nicht geladen werden",
            "err_title": "Fehler",
            "mod_list": "Modulliste",
            "err_page": "Fehler beim Laden der Seite"
        },
        "es": {
            "module_row": "\n<b>{prefix} {module}</b>: ({cmds})",
            "header_stats": "<b>🌙 Total <code>{total}</code> módulos, <code>{hidden}</code> ocultos, <code>{shown}</code> mostrados</b>\n",
            "btn_back": "⬅️ Atrás",
            "btn_next": "Siguiente ➡️",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Módulo</b> «<code>{mod}</code>» <b>no encontrado</b>",
            "no_desc": "Sin descripción",
            "cmd_fmt": "<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}",
            "inline_fmt": "<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}",
            "header_mod": "<b><emoji id=5195083327597456039>🌙</emoji> Módulo:</b> <code>{mod}</code>\n",
            "header_auth": "<b><emoji id=5237922302070367159>❤️</emoji> Autor:</b> <code>{auth}</code>\n",
            "header_ver": "<b><emoji id=5226929552319594190>0️⃣</emoji> Versión:</b> <code>{ver}</code>\n",
            "header_desc": "\n<b><emoji id=5197269100878907942>✍️</emoji> Descripción:</b>\n    ╰ {desc}\n\n",
            "inline_usage": "Uso: @bot help [página]",
            "inline_title": "Ayuda de comandos",
            "err_load": "Error al cargar la lista de módulos",
            "err_title": "Error",
            "mod_list": "Lista de módulos",
            "err_page": "Error al cargar la página"
        },
        "fr": {
            "module_row": "\n<b>{prefix} {module}</b>: ({cmds})",
            "header_stats": "<b>🌙 Total <code>{total}</code> modules, <code>{hidden}</code> cachés, <code>{shown}</code> affichés</b>\n",
            "btn_back": "⬅️ Retour",
            "btn_next": "Suivant ➡️",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Module</b> «<code>{mod}</code>» <b>introuvable</b>",
            "no_desc": "Pas de description",
            "cmd_fmt": "<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}",
            "inline_fmt": "<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}",
            "header_mod": "<b><emoji id=5195083327597456039>🌙</emoji> Module :</b> <code>{mod}</code>\n",
            "header_auth": "<b><emoji id=5237922302070367159>❤️</emoji> Auteur :</b> <code>{auth}</code>\n",
            "header_ver": "<b><emoji id=5226929552319594190>0️⃣</emoji> Version :</b> <code>{ver}</code>\n",
            "header_desc": "\n<b><emoji id=5197269100878907942>✍️</emoji> Description :</b>\n    ╰ {desc}\n\n",
            "inline_usage": "Utilisation : @bot help [page]",
            "inline_title": "Aide des commandes",
            "err_load": "Échec du chargement de la liste des modules",
            "err_title": "Erreur",
            "mod_list": "Liste des modules",
            "err_page": "Erreur lors du chargement de la page"
        },
        "it": {
            "module_row": "\n<b>{prefix} {module}</b>: ({cmds})",
            "header_stats": "<b>🌙 Totale <code>{total}</code> moduli, <code>{hidden}</code> nascosti, <code>{shown}</code> visualizzati</b>\n",
            "btn_back": "⬅️ Indietro",
            "btn_next": "Avanti ➡️",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> <b>Modulo</b> «<code>{mod}</code>» <b>non trovato</b>",
            "no_desc": "Nessuna descrizione",
            "cmd_fmt": "<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}",
            "inline_fmt": "<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}",
            "header_mod": "<b><emoji id=5195083327597456039>🌙</emoji> Modulo:</b> <code>{mod}</code>\n",
            "header_auth": "<b><emoji id=5237922302070367159>❤️</emoji> Autore:</b> <code>{auth}</code>\n",
            "header_ver": "<b><emoji id=5226929552319594190>0️⃣</emoji> Versione:</b> <code>{ver}</code>\n",
            "header_desc": "\n<b><emoji id=5197269100878907942>✍️</emoji> Descrizione:</b>\n    ╰ {desc}\n\n",
            "inline_usage": "Uso: @bot help [pagina]",
            "inline_title": "Aiuto comandi",
            "err_load": "Impossibile caricare l'elenco dei moduli",
            "err_title": "Errore",
            "mod_list": "Elenco moduli",
            "err_page": "Errore nel caricamento della pagina"
        },
        "kk": {
            "module_row": "\n<b>{prefix} {module}</b>: ({cmds})",
            "header_stats": "<b>🌙 Барлығы <code>{total}</code> модуль, <code>{hidden}</code> жасырылған, <code>{shown}</code> көрсетілген</b>\n",
            "btn_back": "⬅️ Артқа",
            "btn_next": "Алға ➡️",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> «<code>{mod}</code>» <b>модулі табылмады</b>",
            "no_desc": "Сипаттама жоқ",
            "cmd_fmt": "<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}",
            "inline_fmt": "<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}",
            "header_mod": "<b><emoji id=5195083327597456039>🌙</emoji> Модуль:</b> <code>{mod}</code>\n",
            "header_auth": "<b><emoji id=5237922302070367159>❤️</emoji> Авторы:</b> <code>{auth}</code>\n",
            "header_ver": "<b><emoji id=5226929552319594190>0️⃣</emoji> Нұсқасы:</b> <code>{ver}</code>\n",
            "header_desc": "\n<b><emoji id=5197269100878907942>✍️</emoji> Сипаттамасы:</b>\n    ╰ {desc}\n\n",
            "inline_usage": "Қолдану: @bot help [бет]",
            "inline_title": "Командалар бойынша көмек",
            "err_load": "Модульдер тізімін жүктеу мүмкін болмады",
            "err_title": "Қате",
            "mod_list": "Модульдер тізімі",
            "err_page": "Бетті жүктеу қатесі"
        },
        "uz": {
            "module_row": "\n<b>{prefix} {module}</b>: ({cmds})",
            "header_stats": "<b>🌙 Jami <code>{total}</code> modul, <code>{hidden}</code> yashirin, <code>{shown}</code> ko'rsatilgan</b>\n",
            "btn_back": "⬅️ Orqaga",
            "btn_next": "Oldinga ➡️",
            "mod_not_found": "<emoji id=5210952531676504517>❌</emoji> «<code>{mod}</code>» <b>moduli topilmadi</b>",
            "no_desc": "Tavsif yo'q",
            "cmd_fmt": "<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}",
            "inline_fmt": "<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}",
            "header_mod": "<b><emoji id=5195083327597456039>🌙</emoji> Modul:</b> <code>{mod}</code>\n",
            "header_auth": "<b><emoji id=5237922302070367159>❤️</emoji> Muallif:</b> <code>{auth}</code>\n",
            "header_ver": "<b><emoji id=5226929552319594190>0️⃣</emoji> Versiya:</b> <code>{ver}</code>\n",
            "header_desc": "\n<b><emoji id=5197269100878907942>✍️</emoji> Tavsif:</b>\n    ╰ {desc}\n\n",
            "inline_usage": "Qo'llanilishi: @bot help [sahifa]",
            "inline_title": "Buyruqlar bo'yicha yordam",
            "err_load": "Modullar ro'yxatini yuklab bo'lmadi",
            "err_title": "Xato",
            "mod_list": "Modullar ro'yxati",
            "err_page": "Sahifani yuklashda xato"
        }
    }
    
    def __init__(self):
        cur_maxmods = self.db.get("xioca.help", "maxmods", 20)
    
        def _sync_maxmods(old, new):
            self.db.set("xioca.help", "maxmods", int(new))
        
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "max_help_modules",
                int(cur_maxmods),
                "Максимум модулей на странице помощи",
                validator=loader.validators.Integer(min=10, max=100),
                step=5,
                on_change=_sync_maxmods,
            ),
        )

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
                for cmd, handler in module.inline_handlers.items():
                    if getattr(handler, "_inline_hidden", False):
                        continue
                    inline_commands.append(f"🎹 <code>{cmd}</code>")
            
            if commands or inline_commands:
                prefix = "▪" if module.name.lower() in __system_mod__ else "▫"
                all_commands = " | ".join(commands + inline_commands)
                text_lines.append(self.S("module_row", prefix=prefix, module=module.name, cmds=all_commands))
        
        header = self.S(
            "header_stats",
            total=len(self.all_modules.modules),
            hidden=len(hide_mods),
            shown=modules_shown
        )
        
        text = header + "".join(text_lines)
        
        if total_pages > 1:
            builder = InlineKeyboardBuilder()
            if page > 0:
                builder.button(text=self.S("btn_back"), callback_data=f"help_prev_{page}")
            builder.button(text=f"{page + 1}/{total_pages}", callback_data="help_page")
            if page < total_pages - 1:
                builder.button(text=self.S("btn_next"), callback_data=f"help_next_{page}")
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
                self.S("mod_not_found", mod=module_name))
        
        prefix = self.db.get("xioca.loader", "prefixes", ["."])[0]
        bot_username = (await self.bot.me()).username

        command_descriptions = []
        for command in module.command_handlers:
            desc = module.command_handlers[command].__doc__ or self.S("no_desc")
            command_descriptions.append(
                self.S("cmd_fmt", cmd=prefix + command, desc=desc))
        
        inline_descriptions = []
        for command, handler in module.inline_handlers.items():
            if getattr(handler, "_inline_hidden", False):
                continue
                
            desc = handler.__doc__ or self.S("no_desc")
            inline_descriptions.append(
                self.S("inline_fmt", bot=bot_username, cmd=command, desc=desc))

        header_parts = [
            self.S("header_mod", mod=module.name)]
        if module.author:
            header_parts.append(self.S("header_auth", auth=module.author))
        if module.version:
            header_parts.append(self.S("header_ver", ver=module.version))
        
        header_parts.extend([
            self.S("header_desc", desc=module.__doc__ or self.S("no_desc"))])
        
        return await utils.answer(
            message, 
            "".join(header_parts) + "\n".join(command_descriptions) + "\n" + "\n".join(inline_descriptions) + "\n\n" + text)
    
    @loader.inline("help", True)
    async def help_inline_handler(self, app: Client, inline_query: types.InlineQuery, args: str):
        """Обработчик инлайн-команды help"""
        if not args.startswith("page_"):
            return await utils.answer_inline(
                inline_query,
                self.S("inline_usage"),
                self.S("inline_title"))
        
        try:
            page = int(args.split("_")[1])
        except (IndexError, ValueError):
            page = 0
            
        text, keyboard = await self._generate_modules_page(page, self.db.get("xioca.help", "maxmods", 20))
        if not text:
            return await utils.answer_inline(
                inline_query,
                self.S("err_load"),
                self.S("err_title"))
            
        await utils.answer_inline(
            inline_query,
            text,
            self.S("mod_list"),
            reply_markup=keyboard)
    
    @loader.callback("help")
    async def help(self, app: Client, call: types.CallbackQuery):
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
            return await call.answer(self.S("err_page"), show_alert=True)
            
        await self.bot.edit_message_text(
            inline_message_id=call.inline_message_id,
            text=text,
            reply_markup=keyboard.as_markup() if keyboard else None)
        await call.answer()
