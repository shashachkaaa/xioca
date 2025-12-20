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

import os
import sys
import re
import subprocess
import logging
import string
import random
import requests
import inspect

from importlib.abc import SourceLoader
from importlib.machinery import ModuleSpec
from importlib.util import spec_from_file_location, module_from_spec

from typing import Union, List, Dict, Any
from types import FunctionType, LambdaType

from pyrogram import Client, types, filters
from .db import db
from . import dispatcher, utils, bot

VALID_URL = r"[-[\]_.~:/?#@!$&'()*+,;%<=>a-zA-Z0-9]+"
VALID_PIP_PACKAGES = re.compile(
    r"^\s*#\s*required:(?: ?)((?:{url} )*(?:{url}))\s*$".format(url=VALID_URL),
    re.MULTILINE,
)

def module(
    author: str = None,
    version: Union[int, float] = None
) -> FunctionType:
    """Обрабатывает класс модуля"""
    def decorator(instance: "Module"):
        instance.name = instance.__name__.replace("Mod", "")
        instance.author = author
        instance.version = version
        return instance
    return decorator


@module()
class Module:
    author: str
    version: Union[int, float]

    async def on_load(self, app: Client) -> Any:
        """Вызывается при загрузке модуля"""

class StringLoader(SourceLoader):
    def __init__(self, data: str, origin: str) -> None:
        self.data = data.encode("utf-8")
        self.origin = origin

    def get_code(self, full_name: str) -> Union[Any, None]:
        source = self.get_source(full_name)
        if not source:
            return None
        return compile(source, self.origin, "exec", dont_inherit=True)

    def get_filename(self, _: str) -> str:
        return self.origin

    def get_data(self, _: str) -> str:
        return self.data


def get_command_handlers(instance: Module) -> Dict[str, FunctionType]:
    return {
        method_name[:-4].lower(): getattr(instance, method_name) 
        for method_name in dir(instance)
        if (callable(getattr(instance, method_name)) and len(method_name) > 4 and method_name.endswith("_cmd"))
    }

def get_watcher_handlers(instance: Module) -> List[FunctionType]:
    return [getattr(instance, method_name) for method_name in dir(instance) if (callable(getattr(instance, method_name)) and method_name.startswith("watcher"))]

def get_message_handlers(instance: Module) -> Dict[str, FunctionType]:
    return {method_name[:-16].lower(): getattr(instance, method_name) for method_name in dir(instance) if (callable(getattr(instance, method_name)) and len(method_name) > 16 and method_name.endswith("_message_handler"))}

def get_callback_handlers(instance: Module) -> Dict[str, FunctionType]:
    return {method_name[:-17].lower(): getattr(instance, method_name) for method_name in dir(instance) if (callable(getattr(instance, method_name)) and len(method_name) > 17 and method_name.endswith("_callback_handler"))}

def get_inline_handlers(instance: Module) -> Dict[str, FunctionType]:
    return {method_name[:-15].lower(): getattr(instance, method_name) for method_name in dir(instance) if (callable(getattr(instance, method_name)) and len(method_name) > 15 and method_name.endswith("_inline_handler"))}


def on(custom_filters: Union[filters.Filter, LambdaType]) -> FunctionType:
    def decorator(func: FunctionType):
        func._filters = (filters.create(custom_filters) if custom_filters.__module__ != "pyrogram.filters" else custom_filters)
        return func
    return decorator


def on_bot(custom_filters: LambdaType) -> FunctionType:
    def decorator(func: FunctionType):
        func._filters = custom_filters
        return func
    return decorator

class ModulesManager:
    def __init__(self, app: Client, db: db, me: types.User) -> None:
        self.modules: List[Module] = []
        self.watcher_handlers: List[FunctionType] = []
        self.command_handlers: Dict[str, FunctionType] = {}
        self.message_handlers: Dict[str, FunctionType] = {}
        self.inline_handlers: Dict[str, FunctionType] = {}
        self.callback_handlers: Dict[str, FunctionType] = {}

        self._local_modules_path: str = "xioca/modules/"
        self._app = app
        self._db = db
        self.me = me
        self.aliases = self._db.get(__name__, "aliases", {})
        self.dp: dispatcher.DispatcherManager = None
        self.bot_manager: bot.BotManager = None

    def _convert_github_url(self, url: str) -> str:
        if "github.com" in url and "/blob/" in url:
            return url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        return url

    async def load(self, app: Client) -> bool:
        self.dp = dispatcher.DispatcherManager(app, self)
        await self.dp.load()
        self.bot_manager = bot.BotManager(app, self._db, self)
        await self.bot_manager.load()

        logging.info("Загрузка модулей...")

        # 1. Загрузка локальных файлов
        for local_module in filter(lambda f: f.endswith(".py") and not f.startswith("_"), os.listdir(self._local_modules_path)):
            module_name = f"xioca.modules.{local_module[:-3]}"
            file_path = os.path.join(os.path.abspath("."), self._local_modules_path, local_module)
            try:
                self.register_instance(module_name, file_path)
            except Exception as error:
                logging.exception(f"Ошибка в локальном модуле {module_name}: {error}")
                # Если файл пустой или с ошибкой синтаксиса (как ваш случай), он тут упадет

        await self.send_on_loads()

        # 2. Загрузка из базы данных
        for custom_module in self._db.get(__name__, "modules", []):
            try:
                fixed_url = self._convert_github_url(custom_module)
                r = await utils.run_sync(requests.get, fixed_url)
                # Здесь используется load_module, который теперь умеет удалять мусор
                await self.load_module(r.text, fixed_url)
            except Exception as error:
                logging.exception(f"Ошибка в стороннем модуле {custom_module}: {error}")

        logging.info("Менеджер модулей загружен")
        return True

    def register_instance(self, module_name: str, file_path: str = "", spec: ModuleSpec = None) -> Module:
        spec = spec or spec_from_file_location(module_name, file_path)
        module = module_from_spec(spec)
        sys.modules[module.__name__] = module
        spec.loader.exec_module(module)

        instance = None
        for key, value in vars(module).items():
            if key.endswith("Mod") and issubclass(value, Module):
                value.db = self._db
                value.all_modules = self
                value.bot = self.bot_manager.bot
                instance = value()
                
                # Очистка старых версий при перезаписи
                for m in self.modules[:]:
                    if m.__class__.__name__ == value.__name__:
                        self.unload_module(m, True)

                instance.command_handlers = get_command_handlers(instance)
                instance.watcher_handlers = get_watcher_handlers(instance)
                instance.message_handlers = get_message_handlers(instance)
                instance.callback_handlers = get_callback_handlers(instance)
                instance.inline_handlers = get_inline_handlers(instance)

                self.modules.append(instance)
                self.command_handlers.update(instance.command_handlers)
                self.watcher_handlers.extend(instance.watcher_handlers)
                self.message_handlers.update(instance.message_handlers)
                self.callback_handlers.update(instance.callback_handlers)
                self.inline_handlers.update(instance.inline_handlers)

        return instance

    async def load_module(self, module_source: str, origin: str = "<string>", did_requirements: bool = False, update_callback: callable = None) -> str:
        """Загружает сторонний модуль и удаляет файл при ошибке"""
        module_name = "xioca.modules." + ("".join(random.choice(string.ascii_letters + string.digits) for _ in range(10)))
        
        # Определяем путь к файлу, если это локальное сохранение
        potential_file = None
        if origin.startswith("http"):
            filename = origin.split("/")[-1]
            if not filename.endswith(".py"): filename += ".py"
            potential_file = os.path.join(self._local_modules_path, filename)

        try:
            # Защита от HTML
            if module_source.strip().startswith("<!DOCTYPE") or "<html" in module_source[:100].lower():
                raise ValueError("Попытка загрузить HTML вместо Python кода (неверная ссылка).")

            spec = ModuleSpec(module_name, StringLoader(module_source, origin), origin=origin)
            instance = self.register_instance(module_name, spec=spec)
            
            if not instance:
                raise ValueError("Класс модуля (Mod) не найден.")
            
            await self.send_on_load(instance)
            return instance.name

        except ModuleNotFoundError as e:
            if did_requirements: return False
            missing = e.name
            if update_callback: await update_callback(f"⏳ Установка <code>{missing}</code>...")
            try:
                if sys.version_info >= (3, 11):
                	subprocess.run([sys.executable, "-m", "pip", "install", missing, "--break-system-packages"], check=True)
                else:
                    subprocess.run([sys.executable, "-m", "pip", "install", missing], check=True)
                return await self.load_module(module_source, origin, True, update_callback)
            except: return False

        except Exception as e:
            logging.exception(f"Критическая ошибка при загрузке {origin}: {e}")
            
            # --- АВТОМАТИЧЕСКОЕ УДАЛЕНИЕ ---
            if potential_file and os.path.exists(potential_file):
                try:
                    os.remove(potential_file)
                    logging.warning(f"Файл {potential_file} удален из-за ошибки в коде.")
                except: pass
            return False

    async def send_on_loads(self) -> bool:
        for module in self.modules:
            await self.send_on_load(module)
        return True

    async def send_on_load(self, module: Module) -> bool:
        try:
            await module.on_load(self._app)
        except Exception as error:
            logging.exception(error)
            return False
        return True

    def unload_module(self, module_name: str = None, is_replace: bool = False) -> str:
        if is_replace:
            module = module_name
        else:
            module_name = utils.find_mod_class_in_file(module_name)
            if not (module := self.get_module(module_name.replace("Mod", ""))):
                return False

            orig = inspect.getmodule(module).__spec__.origin
            if orig != "<string>":
                set_modules = set(self._db.get(__name__, "modules", []))
                self._db.set("xioca.loader", "modules", list(set_modules - {orig}))

        if module in self.modules:
            self.modules.remove(module)
            # Тут должна быть логика очистки хендлеров, если нужно
        return module.name
        
    def get_module(self, name: str, by_commands_too: bool = False) -> Union[Module, None]:
        if (module := list(filter(lambda m: m.name.lower() == name.lower(), self.modules))):
            return module[0]
        if by_commands_too and name in self.command_handlers:
            return self.command_handlers[name].__self__
        return None
