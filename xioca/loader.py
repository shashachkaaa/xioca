# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import os
import sys
import re
import subprocess
import logging
import string
import random
import requests
import inspect
import asyncio

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
    """
    Обрабатывает класс модуля
    """
    def decorator(instance: "Module"):
        instance.name = instance.__name__.replace("Mod", "")
        instance.author = author
        instance.version = version
        return instance
    return decorator

def command(*aliases: str):
    """
    Декоратор для регистрации команд.
    """
    def decorator(func: FunctionType):
        func._custom_commands = aliases
        return func
    return decorator

def callback(data: str):
    """
    Декоратор для регистрации callback-хендлеров.
    """
    def decorator(func: FunctionType):
        async def wrapper(self, client, call: types.CallbackQuery):
            if not (call.data == data or call.data.startswith(f"{data}_")):
                return False

            return await func(self, client, call)

        wrapper._custom_callback = data
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        
        return wrapper
    return decorator

def inline(pattern: str):
    """
    Декоратор для регистрации inline-хендлеров.
    """
    def decorator(func: FunctionType):
        func._custom_inline = pattern
        return func
    return decorator

def loop(interval: float = 60, autostart: bool = True):
    """
    Декоратор для фоновых задач.
    
    Args:
        interval (float): Интервал повторения в секундах.
        autostart (bool): Запускать ли автоматически при загрузке.
    """
    def decorator(func: FunctionType):
        func._is_loop = True
        func._loop_interval = interval
        func._loop_autostart = autostart
        return func
    return decorator

@module()
class Module:
    author: str
    version: Union[int, float]

    _tasks: Dict[str, asyncio.Task] = {} 
    
    strings: Dict[str, Dict[str, str]] = {}

    async def on_load(self, app: Client) -> Any:
        """Вызывается при загрузке модуля"""
    
    async def on_unload(self) -> Any:
        """Вызывается ПЕРЕД выгрузкой модуля. Используйте для очистки ресурсов."""
    
    def S(self, key: str, *args, **kwargs) -> str:
        """Получает строку перевода по ключу."""
        lang = self.db.get("xioca.loader", "language", "en")
        template = self.strings.get(lang, {}).get(key)
        if not template:
            template = self.strings.get("en", {}).get(key)
        if not template:
            return f"<{key}>"
        try:
            return template.format(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error formatting string '{key}' in module '{self.name}': {e}")
            return template

    async def _loop_worker(self, func: FunctionType, interval: float):
        """Внутренняя логика выполнения цикла"""
        await asyncio.sleep(1)
        
        while True:
            try:
                await func()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Error in loop '{func.__name__}' of module '{self.name}': {e}")
            
            await asyncio.sleep(interval)

    def start_loop(self, name: str) -> bool:
        """
        Запускает задачу loop по имени метода.
        Пример: self.start_loop("check_updates")
        """
        if name in self._tasks:
            return False
            
        method = getattr(self, name, None)
        if not method:
            logging.error(f"Method '{name}' not found in module '{self.name}'")
            return False
            
        if not getattr(method, "_is_loop", False):
            logging.error(f"Method '{name}' is not decorated with @loader.loop")
            return False

        interval = getattr(method, "_loop_interval", 60)
        
        task = asyncio.create_task(self._loop_worker(method, interval))
        self._tasks[name] = task
        
        logging.debug(f"Started loop '{name}' in module '{self.name}'")
        return True

    def stop_loop(self, name: str) -> bool:
        """
        Останавливает задачу loop по имени метода.
        Пример: self.stop_loop("check_updates")
        """
        if name in self._tasks:
            self._tasks[name].cancel()
            del self._tasks[name]
            logging.debug(f"Stopped loop '{name}' in module '{self.name}'")
            return True
        return False

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
    handlers = {}
    for name in dir(instance):
        method = getattr(instance, name)
        if not callable(method): continue
            
        if hasattr(method, "_custom_commands"):
            for alias in method._custom_commands:
                handlers[alias.lower()] = method
        
        if name.endswith("_cmd") and len(name) > 4:
            cmd_name = name[:-4].lower()
            if getattr(method, "_custom_commands", None) is None or cmd_name not in method._custom_commands:
                handlers[cmd_name] = method
    return handlers

def get_watcher_handlers(instance: Module) -> List[FunctionType]:
    return [getattr(instance, method_name) for method_name in dir(instance) if (callable(getattr(instance, method_name)) and method_name.startswith("watcher"))]

def get_message_handlers(instance: Module) -> Dict[str, FunctionType]:
    return {method_name[:-16].lower(): getattr(instance, method_name) for method_name in dir(instance) if (callable(getattr(instance, method_name)) and len(method_name) > 16 and method_name.endswith("_message_handler"))}

def get_callback_handlers(instance: Module) -> Dict[str, FunctionType]:
    handlers = {}
    for name in dir(instance):
        method = getattr(instance, name)
        if not callable(method): continue
        
        if hasattr(method, "_custom_callback"):
            handlers[method._custom_callback] = method
            continue

        if len(name) > 17 and name.endswith("_callback_handler"):
            handlers[name[:-17].lower()] = method
            
    return handlers

def get_inline_handlers(instance: Module) -> Dict[str, FunctionType]:
    handlers = {}
    for name in dir(instance):
        method = getattr(instance, name)
        if not callable(method): continue
        
        if hasattr(method, "_custom_inline"):
            handlers[method._custom_inline] = method
            continue

        if len(name) > 15 and name.endswith("_inline_handler"):
            handlers[name[:-15].lower()] = method
            
    return handlers

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

        logging.info("Loading modules...")

        for local_module in filter(lambda f: f.endswith(".py") and not f.startswith("_"), os.listdir(self._local_modules_path)):
            module_name = f"xioca.modules.{local_module[:-3]}"
            file_path = os.path.join(os.path.abspath("."), self._local_modules_path, local_module)
            try:
                self.register_instance(module_name, file_path)
            except Exception as error:
                logging.exception(f"Error in local module {module_name}: {error}")

        await self.send_on_loads()

        for custom_module in self._db.get(__name__, "modules", []):
            try:
                fixed_url = self._convert_github_url(custom_module)
                r = await utils.run_sync(requests.get, fixed_url)
                await self.load_module(r.text, fixed_url)
            except Exception as error:
                logging.exception(f"Error in third-party module {custom_module}: {error}")

        logging.info("Module manager loaded")
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
                value._client = self._app
                value.client = self._app
                value.app = self._app
                instance = value()

                instance._tasks = {} 

                for m in self.modules[:]:
                    if m.__class__.__name__ == value.__name__:
                        self.unload_module(m, True)

                instance.command_handlers = get_command_handlers(instance)
                instance.watcher_handlers = get_watcher_handlers(instance)
                instance.message_handlers = get_message_handlers(instance)
                instance.callback_handlers = get_callback_handlers(instance)
                instance.inline_handlers = get_inline_handlers(instance)

                for name in dir(instance):
                    method = getattr(instance, name)
                    if not callable(method): continue
                    
                    if getattr(method, "_is_loop", False) and getattr(method, "_loop_autostart", True):
                        instance.start_loop(name)

                self.modules.append(instance)
                self.command_handlers.update(instance.command_handlers)
                self.watcher_handlers.extend(instance.watcher_handlers)
                self.message_handlers.update(instance.message_handlers)
                self.callback_handlers.update(instance.callback_handlers)
                self.inline_handlers.update(instance.inline_handlers)

        return instance

    async def load_module(
        self, 
        module_source: str, 
        origin: str = "<string>", 
        installed_attempts: List[str] = None,
        update_callback: callable = None
    ) -> str:
        if installed_attempts is None:
            installed_attempts = []

        module_name = "xioca.modules." + ("".join(random.choice(string.ascii_letters + string.digits) for _ in range(10)))
        
        potential_file = None
        if origin.startswith("http"):
            filename = origin.split("/")[-1]
            if not filename.endswith(".py"): filename += ".py"
            potential_file = os.path.join(self._local_modules_path, filename)

        if not installed_attempts:
            requirements = VALID_PIP_PACKAGES.search(module_source)
            if requirements:
                req_list = requirements.group(1).split()
                for req in req_list:
                    if req in installed_attempts: continue
                    
                    if update_callback:
                        await update_callback(utils.sys_S("install_req", r=req))
                    try:
                        pip_args = [sys.executable, "-m", "pip", "install", req]
                        if sys.version_info >= (3, 11):
                            pip_args.append("--break-system-packages")

                        process = await asyncio.create_subprocess_exec(
                            *pip_args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                        )
                        await process.communicate()
                        installed_attempts.append(req)
                    except Exception as e:
                        logging.error(f"Failed to install req {req}: {e}")

        try:
            if module_source.strip().startswith("<!DOCTYPE") or "<html" in module_source[:100].lower():
                raise ValueError("Attempted to load HTML instead of Python code (invalid link).")

            spec = ModuleSpec(module_name, StringLoader(module_source, origin), origin=origin)
            instance = self.register_instance(module_name, spec=spec)
            
            if not instance:
                raise ValueError("Module class (Mod) not found.")
            
            await self.send_on_load(instance)
            return instance.name

        except ModuleNotFoundError as e:
            missing_pkg = e.name
            
            if missing_pkg in installed_attempts:
                logging.error(f"Failed to load module even after installing {missing_pkg}")
                return False

            if update_callback: 
                await update_callback(utils.sys_S("auto_install_req", mpkg=missing_pkg))
            
            logging.info(f"Missing module '{missing_pkg}', trying to install...")

            try:
                pip_args = [sys.executable, "-m", "pip", "install", missing_pkg]
                if sys.version_info >= (3, 11):
                    pip_args.append("--break-system-packages")

                process = await asyncio.create_subprocess_exec(
                    *pip_args,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                await process.communicate()
                
                if process.returncode != 0:
                    logging.error(f"Pip install failed for {missing_pkg}")
                    return False

                installed_attempts.append(missing_pkg)

                return await self.load_module(module_source, origin, installed_attempts, update_callback)

            except Exception as pip_error: 
                logging.error(f"Pip error: {pip_error}")
                return False

        except Exception as e:
            logging.exception(f"Critical error loading {origin}: {e}")
            
            if potential_file and os.path.exists(potential_file):
                try:
                    os.remove(potential_file)
                    logging.warning(f"File {potential_file} deleted due to a code error.")
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

        if hasattr(module, "on_unload") and callable(module.on_unload):
            try:
                if asyncio.iscoroutinefunction(module.on_unload):
                    asyncio.create_task(module.on_unload())
            except Exception as e:
                logging.error(f"Error in on_unload for {module.name}: {e}")

        if hasattr(module, "_tasks"):
            for name, task in module._tasks.items():
                task.cancel()
            logging.debug(f"Cancelled {len(module._tasks)} tasks for module {module.name}")

        if module in self.modules:
            self.modules.remove(module)
        return module.name
        
    def get_module(self, name: str, by_commands_too: bool = False) -> Union[Module, None]:
        if (module := list(filter(lambda m: m.name.lower() == name.lower(), self.modules))):
            return module[0]
        if by_commands_too and name in self.command_handlers:
            return self.command_handlers[name].__self__
        return None
