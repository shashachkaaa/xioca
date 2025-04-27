import os
import requests
import logging
from pyrogram import Client, types
from .. import loader, utils, __system_mod__

@loader.module(name="Loader", author="sh1tn3t | shashachkaaa")
class LoaderMod(loader.Module):
    """Загрузчик модулей"""
    
    async def dlmod_cmd(self, app: Client, message: types.Message, args):
    	"""Загрузить модуль по ссылке или из репозитория. Использование: dlmod <ссылка или название модуля>"""
    	
    	if not args:
    		return await utils.answer(message, "<emoji id=5210952531676504517>❌</emoji> <b>Необходимо указать ссылку или название модуля</b>")
    	
    	repo_url = self.db.get("xioca.loader", "repo", "https://xioca.live/modules/")
    	
    	if not args.startswith(("http://", "https://")):
    		module_name = args if args.endswith(".py") else f"{args}.py"
    		args = f"{repo_url}{module_name}"
    	else:
    		module_name = args.split("/")[-1]
    		if not module_name.endswith(".py"):
    			module_name = f"{module_name}.py"
    	
    	msg = await utils.answer(message, f"<emoji id=5328274090262275771>⏳</emoji> <b>Загрузка модуля из {args}...</b>")
    	
    	async def update_message(text):
    		try:
    			await msg.edit(text)
    		except:
    			pass
    	
    	try:
    		r = await utils.run_sync(requests.get, args)
    		if r.status_code != 200:
    			return await utils.answer(message, f"<emoji id=5210952531676504517>❌</emoji> <b>Ошибка загрузки модуля (код {r.status_code})</b>\nURL: {args}")
    	
    		module_source = r.text
    		module_content = module_source
    		
    		modules_dir = "modules"
    		os.makedirs(modules_dir, exist_ok=True)
    		file_path = os.path.join(modules_dir, module_name)
    		
    		with open(f"xioca/{file_path}", "w", encoding="utf-8") as f:
    			f.write(module_content)
    		
    		module_name = await self.all_modules.load_module(module_source=module_source, origin=args, update_callback=update_message)
    	
    		if module_name is True:
    			return await utils.answer(message, "<emoji id=5206607081334906820>✔️</emoji> <b>Зависимости установлены. Требуется перезагрузка</b>")
    	
    		if not module_name:
    			return await utils.answer(message, "<emoji id=5210952531676504517>❌</emoji> <b>Не удалось загрузить модуль. Подробности смотри в логах</b>")
    	
    		module = self.all_modules.get_module(module_name.lower())
    		if not module:
    			return await utils.answer(message, f"<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{module_name}</code>» <b>не найден</b>")
    	
    		if args.startswith(("http://", "https://")):
    			modules = self.db.get("xioca.loader", "modules", [])
    			if args not in modules:
    				modules.append(args)
    				self.db.set("xioca.loader", "modules", modules)
    	
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
    			(f"<b><emoji id=5237922302070367159>❤️</emoji> Автор:</b> <code>{module.author}</code>\n" if module.author else "") +
    			(f"<b><emoji id=5226929552319594190>0️⃣</emoji> Версия:</b> <code>{module.version}</code>\n" if module.version else "") +
    			f"\n<b><emoji id=5197269100878907942>✍️</emoji> Описание:</b>\n" +
    			f"    ╰ {module.__doc__ or 'Нет описания для модуля'}\n\n"
    		)
    	
    		return await utils.answer(message, f"<emoji id=5206607081334906820>✔️</emoji> <b>Модуль \"<code>{module_name}</code>\" загружен</b>\n\n" + header + command_descriptions + "\n" + inline_descriptions)
    	except requests.exceptions.RequestException as e:
    		return await utils.answer(message, f"<emoji id=5210952531676504517>❌</emoji> <b>Ошибка при загрузке модуля:</b> {str(e)}\nURL: {args}")
    	except Exception as e:
    		logging.exception(f"Ошибка в dlmod_cmd: {e}")
    		return await utils.answer(message, "<emoji id=5210952531676504517>❌</emoji> <b>Произошла непредвиденная ошибка. Подробности в логах</b>")
   
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
        original_file_name = file.document.file_name
        
        file_path = os.path.join(modules_dir, file.document.file_name)
        await file.download(file_path)

        try:
            with open(f"xioca/{file_path}", "r", encoding="utf-8") as f:
                module_source = f.read()
            
            class_name = None
            for line in module_source.splitlines():
            	if "class" in line and "Mod(loader.Module):" in line:
            		class_name = line.split("class")[1].split("(")[0].strip()
            		break
            
            if not class_name:
            	os.remove(f"xioca/{temp_file_path}")
            	return await utils.answer(message, "<emoji id=5210952531676504517>❌</emoji> <b>Не удалось определить класс модуля (должен заканчиваться на Mod)</b>")
            
            new_file_name = f"{class_name.lower().replace('mod', '')}.py"
            new_file_path = os.path.join(modules_dir, new_file_name)
            os.rename(f"xioca/{file_path}", f"xioca/{new_file_path}")
            
        except UnicodeDecodeError:
            return await utils.answer(
                message, "<emoji id=5210952531676504517>❌</emoji> <b>Неверная кодировка файла</b>"
            )
        except Exception as e:
            logging.error(f"Ошибка при чтении файла: {e}")
            return await utils.answer(
                message, "<emoji id=5210952531676504517>❌</emoji> <b>Не удалось прочитать файл</b>"
            )
        
        msg = await utils.answer(message, "<emoji id=5328274090262275771>⏳</emoji> <b>Загрузка модуля...</b>")
        
        async def update_message(text):
        	try:
        		await msg.edit(text)
        	except:
        		pass
        
        module_name = await self.all_modules.load_module(module_source=module_source, update_callback=update_message)
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
        module_name, text = utils.get_module_name(args)
        
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