import os
import logging
from pyrogram import Client, types
from .. import loader, utils, __system_mod__

@loader.module(name="Loader", author="sh1tn3t | shashachkaaa")
class LoaderMod(loader.Module):
    """Загрузчик модулей"""
    
    async def loadmod_cmd(self, app: Client, message: types.Message):
        """Загрузить модуль по файлу. Использование: <реплай на файл>"""
        reply = message.reply_to_message
        file = (
            message
            if message.document
            else reply
            if reply and reply.document
            else None
        )

        if not file:
            return await utils.answer(
                message, "<emoji id=5210952531676504517>❌</emoji> <b>Необходим ответ на файл</b>"
            )

        modules_dir = "modules"
        
        file_path = os.path.join(modules_dir, file.document.file_name)
        await file.download(file_path)

        try:
            with open(f"xioca/{file_path}", "r", encoding="utf-8") as f:
                module_source = f.read()
        except UnicodeDecodeError:
            return await utils.answer(
                message, "<emoji id=5210952531676504517>❌</emoji> <b>Неверная кодировка файла</b>"
            )
        except Exception as e:
            logging.error(f"Ошибка при чтении файла: {e}")
            return await utils.answer(
                message, "<emoji id=5210952531676504517>❌</emoji> <b>Не удалось прочитать файл</b>"
            )

        module_name = await self.all_modules.load_module(module_source)
        if module_name is True:
            return await utils.answer(
                message, "<emoji id=5206607081334906820>✔️</emoji> <b>Зависимости установлены. Требуется перезагрузка</b>"
            )

        if not module_name:
            return await utils.answer(
                message, "<emoji id=5210952531676504517>❌</emoji> <b>Не удалось загрузить модуль. Подробности смотри в логах</b>"
            )
            
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
            f"<emoji id=5471978009449731768>👉</emoji> <code>@{bot_username + ' ' + command}</code>\n"
            f"    ╰ {module.inline_handlers[command].__doc__ or 'Нет описания для команды'}"
            for command in module.inline_handlers
        )

        header = (
            (
                f"<b><emoji id=5237922302070367159>❤️</emoji> Автор:</b> <code>{module.author}</code>\n" if module.author else ""
            ) + (
                f"<b><emoji id=5226929552319594190>0️⃣</emoji> Версия:</b> <code>{module.version}</code>\n" if module.version else ""
            ) + (
                f"\n<b><emoji id=5197269100878907942>✍️</emoji> Описание:</b>\n"
                f"    ╰ {module.__doc__ or 'Нет описания для модуля'}\n\n"
            )
        )

        return await utils.answer(
            message, f"<emoji id=5206607081334906820>✔️</emoji> <b>Модуль \"<code>{module_name}</code>\" загружен</b>\n\n" + header + command_descriptions + "\n" + inline_descriptions
        )
    
    async def unloadmod_cmd(self, app: Client, message: types.Message, args: str):
        """Выгрузить модуль. Использование: unloadmod <название модуля>"""
        module_name, text = utils.get_module_name(message)
        
        if module_name.lower() in __system_mod__:
            return await utils.answer(
                message, f"<emoji id=5210952531676504517>❌</emoji> <code>{module_name}</code> <b>является системным модулем, его выгрузить невозможно!</b>"
            )
        
        self.all_modules.unload_module(module_name)
        os.remove(f"xioca/modules/{module_name}.py")

        return await utils.answer(
            message, f"<emoji id=5206607081334906820>✔️</emoji> <b>Модуль \"<code>{module_name}</code>\" выгружен</b>\n\n{text}"
        )

    async def ml_cmd(self, app: Client, message: types.Message, args: str):
        """Поделиться модулем"""
        if not args:
            return await utils.answer(
                message, "<emoji id=5210952531676504517>❌</emoji> <b>Нет аргументов</b>"
            )
        
        module_name, text = utils.get_module_name(message)
        
        try:
            file_path = f"xioca/modules/{module_name}.py"
            await utils.answer(
                message,
                chat_id=message.chat.id,
                document=True,
                response=file_path,
                caption=(
                    f"<emoji id=5433653135799228968>📁</emoji> <b>Файл</b> <code>{module_name}</code>\n\n"
                    f"<emoji id=5195083327597456039>🌙</emoji> <code>.loadmod</code> <b>в ответ на это сообщение, чтобы установить модуль</b>\n\n"
                    f"{text}"
                )
            )
        except Exception as e:
            logging.error(e)
            await utils.answer(
                message, "<emoji id=5210952531676504517>❌</emoji> <b>Модуль не найден</b>"
            )