# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import os
import sys
import re
import ast
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

from typing import Union, List, Dict, Any, Optional, Callable
from types import FunctionType, LambdaType

import pyrogram
from pyrogram import Client, types, filters
from pyrogram.handlers import MessageHandler
from .db import db
from . import dispatcher, utils, bot, dragon

VALID_URL = r"[-[\]_.~:/?#@!$&'()*+,;%<=>a-zA-Z0-9]+"
VALID_PIP_PACKAGES = re.compile(
    r"^\s*#\s*required:(?: ?)((?:{url} )*(?:{url}))\s*$".format(url=VALID_URL),
    re.MULTILINE,
)

from dataclasses import dataclass
from typing import Optional, Callable

class ValidationError(ValueError):
    """Raised when a config value is invalid."""
    pass

class Validator:
    """Base validator: parse(text)->value and validate(value)->value."""
    def parse(self, text: str):
        return text

    def validate(self, value):
        return value

class Boolean(Validator):
    TRUE = {"1","true","yes","y","on","да","д","+"}
    FALSE = {"0","false","no","n","off","нет","н","-"}

    def parse(self, text: str) -> bool:
        t = (text or "").strip().lower()
        if t in self.TRUE:
            return True
        if t in self.FALSE:
            return False
        raise ValidationError("Expected boolean (true/false)")

    def validate(self, value) -> bool:
        if isinstance(value, bool):
            return value
        raise ValidationError("Expected bool")

class Integer(Validator):
    def __init__(self, min: int = None, max: int = None):
        self.min = min
        self.max = max

    def parse(self, text: str) -> int:
        try:
            v = int((text or "").strip())
        except Exception:
            raise ValidationError("Expected integer")
        return self.validate(v)

    def validate(self, value) -> int:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValidationError("Expected int")
        if self.min is not None and value < self.min:
            raise ValidationError(f"Min is {self.min}")
        if self.max is not None and value > self.max:
            raise ValidationError(f"Max is {self.max}")
        return value

class Float(Validator):
    def __init__(self, min: float = None, max: float = None):
        self.min = min
        self.max = max

    def parse(self, text: str) -> float:
        try:
            v = float((text or "").strip())
        except Exception:
            raise ValidationError("Expected float")
        return self.validate(v)

    def validate(self, value) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValidationError("Expected float")
        v = float(value)
        if self.min is not None and v < self.min:
            raise ValidationError(f"Min is {self.min}")
        if self.max is not None and v > self.max:
            raise ValidationError(f"Max is {self.max}")
        return v

class String(Validator):
    def __init__(self, min_len: int = None, max_len: int = None):
        self.min_len = min_len
        self.max_len = max_len

    def parse(self, text: str) -> str:
        return self.validate(str(text or ""))

    def validate(self, value) -> str:
        if not isinstance(value, str):
            raise ValidationError("Expected string")
        if self.min_len is not None and len(value) < self.min_len:
            raise ValidationError(f"Min length is {self.min_len}")
        if self.max_len is not None and len(value) > self.max_len:
            raise ValidationError(f"Max length is {self.max_len}")
        return value

class Choice(Validator):
    def __init__(self, *choices: str):
        self.choices = list(choices)

    def parse(self, text: str) -> str:
        return self.validate((text or "").strip())

    def validate(self, value) -> str:
        if value not in self.choices:
            raise ValidationError(f"Allowed: {', '.join(self.choices)}")
        return value

@dataclass
class ConfigValue:
    name: str
    default: Any
    description: str = ""
    validator: Validator = String()
    hidden: bool = False
    step: Optional[float] = None
    on_change: Optional[Callable[[Any, Any], Any]] = None

class ModuleConfig:
    """Config container stored in DB."""
    def __init__(self, *values: ConfigValue):
        self._values = list(values)
        self._by_name = {v.name: v for v in self._values}
        self._module = None

    def bind(self, module: "Module"):
        self._module = module
        tbl = self._table()
        for v in self._values:
            if not module.db.exists(tbl, v.name):
                module.db.set(tbl, v.name, v.default)

    def _table(self) -> str:
        return f"xioca.config.{self._module.name}"

    def keys(self, include_hidden: bool = False):
        if include_hidden:
            return list(self._by_name.keys())
        return [k for k, v in self._by_name.items() if not v.hidden]

    def meta(self, name: str) -> ConfigValue:
        return self._by_name[name]

    def get(self, name: str):
        v = self._by_name[name]
        return self._module.db.get(self._table(), name, v.default)

    def set(self, name: str, value):
        v = self._by_name[name]
        new_val = v.validator.validate(value)
        old_val = self.get(name)
        self._module.db.set(self._table(), name, new_val)
        if v.on_change:
            try:
                v.on_change(old_val, new_val)
            except Exception:
                logging.exception("config on_change error")
        return new_val

    def reset(self, name: str):
        v = self._by_name[name]
        self._module.db.set(self._table(), name, v.default)
        return v.default

    def parse_and_set(self, name: str, text: str):
        v = self._by_name[name]
        parsed = v.validator.parse(text)
        return self.set(name, parsed)

    def __getitem__(self, name: str):
        return self.get(name)

    def __setitem__(self, name: str, value):
        return self.set(name, value)

class validators:
    Boolean = Boolean
    Integer = Integer
    Float = Float
    String = String
    Choice = Choice

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

def inline(pattern: str, hide: bool = False):
    """
    Декоратор для регистрации inline-хендлеров.
    
    Args:
        pattern (str): Regex паттерн триггера.
        hide (bool): Если True, хендлер не будет отображаться в помощи.
    """
    def decorator(func: FunctionType):
        func._custom_inline = pattern
        func._inline_hidden = hide
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
    
    strings: Dict[str, Dict[str, str]] = {}

    async def on_load(self, app: Client) -> bool:
        pass

    async def on_unload(self) -> bool:
        pass

    def S(self, key: str, *args, **kwargs):
        """Получает строку перевода по ключу"""
        lang = self.db.get("xioca.loader", "language", "en")
        text = self.strings.get(lang, {}).get(key, self.strings.get("en", {}).get(key, key))
        try:
            return text.format(*args, **kwargs)
        except Exception:
            return text

    def __getattr__(self, name: str) -> Any:
        if name.endswith("_cmd"):
            raise AttributeError(f"Command {name} not found")
        return super().__getattribute__(name)
    
    async def _loop_worker(self, func: FunctionType, interval: float):
        """Внутренняя логика выполнения loop-задачи"""
        await asyncio.sleep(1)

        while True:
            try:
                await func()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(
                    f"Error in loop '{func.__name__}' of module '{self.name}': {e}"
                )

            await asyncio.sleep(interval)

    def start_loop(self, name: str) -> bool:
        """
        Запускает loop-задачу по имени метода.
        Пример: self.start_loop("check_updates")
        """
        if not hasattr(self, "_tasks"):
            self._tasks = {}

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
        Останавливает loop-задачу по имени метода.
        """
        if hasattr(self, "_tasks") and name in self._tasks:
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
            file_path = os.path.join(os.path.abspath("."), self._local_modules_path, local_module)
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                logging.error(f"Failed to read module {local_module}: {e}")
                continue

            if "utils.misc" in content or "utils.scripts" in content or "@Client.on_message" in content:
                try:
                    await self.load_module(content, origin=file_path)
                except Exception as error:
                    logging.exception(f"Error in local Dragon module {local_module}: {error}")
                continue

            module_name = f"xioca.modules.{local_module[:-3]}"
            try:
                self.register_instance(module_name, file_path)
            except Exception as error:
                logging.exception(f"Error in local module {module_name}: {error}")

        await self.send_on_loads()

        for custom_module in self._db.get(__name__, "modules", []):
            try:
                fixed_url = self._convert_github_url(custom_module)

                raw_name = fixed_url.split("/")[-1]
                raw_name = re.split(r"[?#]", raw_name)[0]
                filename = raw_name if raw_name.endswith(".py") else f"{raw_name}.py"

                candidate_paths = [
                    os.path.join(self._local_modules_path, filename),
                    os.path.join("modules", filename),
                    os.path.join(os.getcwd(), "modules", filename),
                    os.path.join(os.getcwd(), filename),
                ]
                if any(os.path.exists(path) for path in candidate_paths):
                    continue

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
                value.me = self
                value.bot = self.bot_manager.bot
                value._client = self._app
                value.client = self._app
                value.app = self._app
                
                instance = value()

                instance._tasks = {} 

                if hasattr(instance, "config") and isinstance(getattr(instance, "config"), ModuleConfig):
                    instance.config.bind(instance)

                for module_instance in self.modules[:]:
                    if module_instance.__class__.__name__ == value.__name__:
                        self.unload_module(module_instance, True)

                instance.command_handlers = get_command_handlers(instance)
                instance.watcher_handlers = get_watcher_handlers(instance)
                instance.message_handlers = get_message_handlers(instance)
                instance.callback_handlers = get_callback_handlers(instance)
                instance.inline_handlers = get_inline_handlers(instance)

                for name in dir(instance):
                    method = getattr(instance, name)
                    if not callable(method): continue
                    
                    if getattr(method, "_is_loop", False) and getattr(method, "_loop_autostart", True):
                        interval = getattr(method, "_loop_interval", 60)
                        instance.start_loop(name)

                self.modules.append(instance)
                self.command_handlers.update(instance.command_handlers)
                self.watcher_handlers.extend(instance.watcher_handlers)
                self.message_handlers.update(instance.message_handlers)
                self.callback_handlers.update(instance.callback_handlers)
                self.inline_handlers.update(instance.inline_handlers)

        return instance

    async def _loop_worker(self, instance: Module, func: FunctionType, interval: float):
        await asyncio.sleep(1)
        while True:
            try:
                await func()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Error in loop '{func.__name__}' of module '{instance.name}': {e}")
            await asyncio.sleep(interval)

    async def load_module(
        self, module_source: str, origin: str = "<string>", installed_attempts: List[str] = None, update_callback: callable = None
    ) -> str:
        if installed_attempts is None:
            installed_attempts = []

        def _build_status_text(current_pkg: str, icon: str) -> str:
            header = utils.sys_S("installing_deps_header")
            text = f"{header}\n"
            for lib in installed_attempts:
                text += f"<emoji id=5350626672028697529>✅</emoji> {lib}\n"
            text += f"{icon} {current_pkg}..."
            return text

        module_name = "xioca.modules." + ("".join(random.choice(string.ascii_letters + string.digits) for _ in range(10)))

        if not installed_attempts:
            requirements = VALID_PIP_PACKAGES.search(module_source)
            if requirements:
                req_list = requirements.group(1).split()
                for req in req_list:
                    if req in installed_attempts: continue

                    if update_callback:
                        await update_callback(_build_status_text(req, "<emoji id=5382159870944364701>⚪️</emoji>"))

                    try:
                        pip_args = [sys.executable, "-m", "pip", "install", req]
                        if sys.version_info >= (3, 11):
                            pip_args.append("--break-system-packages")

                        process = await asyncio.create_subprocess_exec(
                            *pip_args,
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE
                        )
                        await process.communicate()
                        installed_attempts.append(req)
                    except Exception as e:
                        logging.error(f"Failed to install req {req}: {e}")

        dragon.register_compat()
        is_dragon_style = "utils.misc" in module_source or "utils.scripts" in module_source or "@Client.on_message" in module_source

        try:
            if module_source.strip().startswith("<!DOCTYPE") or "<html" in module_source[:100].lower():
                raise ValueError("Attempted to load HTML instead of Python code (invalid link).")

            if is_dragon_style and "class " not in module_source:
                return await self._load_dragon_module(module_source, origin)

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
                await update_callback(_build_status_text(missing_pkg, "<emoji id=5963087934696459905>⬇</emoji>️"))

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
            logging.exception(f"Failed to load module {origin}: {e}")
            return False

    async def _load_dragon_module(self, code: str, origin: str) -> str:
        """
        Финальная версия загрузчика: использует AST-анализ для извлечения команд из исходного кода.
        """
        dragon.modules_help.clear()

        if self._app.me is None and self.me:
            self._app.me = self.me

        module_name = "xioca.modules.dragon_" + ("".join(random.choice(string.ascii_letters + string.digits) for _ in range(8)))

        class DragonMod(Module):
            pass

        clean_name = origin.split("/")[-1].replace(".py", "")
        if not clean_name or clean_name == "<string>":
            clean_name = f"DragonMod_{random.randint(100,999)}"

        DragonMod.__name__ = clean_name + "Mod"
        instance = DragonMod()
        instance.name = clean_name
        instance.author = "Dragon Port"

        instance.command_handlers = {}
        instance.watcher_handlers = []
        instance._dragon_handlers = []
        instance.inline_handlers = {}

        instance.db = self._db
        instance.all_modules = self
        instance.client = self._app
        instance.app = self._app

        func_to_command = {}

        def _extract_command_from_node(node):
            """Рекурсивно ищет вызов .command("name") внутри узла AST"""
            if isinstance(node, ast.BinOp):
                return _extract_command_from_node(node.left) or _extract_command_from_node(node.right)

            if isinstance(node, ast.Call):
                if hasattr(node.func, "attr") and node.func.attr == "command":
                    if node.args:
                        arg0 = node.args[0]
                        if isinstance(arg0, ast.Constant):
                            return str(arg0.value)
                        elif isinstance(arg0, ast.Str):
                            return arg0.s
                        elif isinstance(arg0, ast.List) and arg0.elts:
                            elt = arg0.elts[0]
                            if isinstance(elt, ast.Constant):
                                return str(elt.value)
                            elif isinstance(elt, ast.Str):
                                return elt.s

                if hasattr(node.func, "attr") and node.func.attr == "regex":
                    if node.args:
                        arg0 = node.args[0]
                        if isinstance(arg0, ast.Constant):
                            clean = str(arg0.value).replace("^", "").replace("$", "").split()[0]
                            if clean.isalnum(): return clean
            return None

        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.AsyncFunctionDef):
                    for decorator in node.decorator_list:
                        is_message_handler = False
                        if isinstance(decorator, ast.Call):
                            if hasattr(decorator.func, "attr") and decorator.func.attr == "on_message":
                                is_message_handler = True

                            if is_message_handler:
                                for arg in decorator.args:
                                    cmd = _extract_command_from_node(arg)
                                    if cmd:
                                        func_to_command[node.name] = cmd.lower()
                                        break
        except Exception as e:
            logging.error(f"AST Parsing failed for {clean_name}: {e}")

        captured_handlers = []

        def on_message_interceptor(*args, **kwargs):
            def decorator(func):
                flt = args[0] if args else filters.all
                group = kwargs.get("group", 0)
                captured_handlers.append((func, flt, group))
                return func
            return decorator

        class MockClient:
            on_message = staticmethod(on_message_interceptor)
            on_edited_message = staticmethod(on_message_interceptor)
            on_callback_query = staticmethod(on_message_interceptor)
            on_deleted_messages = staticmethod(on_message_interceptor)

            def __init__(self, *args, **kwargs): pass
            def __getattr__(self, item): return lambda *a, **k: None

        mock_app_instance = MockClient()

        exec_globals = {
            "Client": MockClient, "client": mock_app_instance, "app": mock_app_instance, "bot": mock_app_instance,
            "filters": filters, "Message": types.Message, "__name__": module_name,
            "sys": sys, "os": os, "asyncio": asyncio, "random": random, "utils": dragon
        }

        original_client = pyrogram.Client
        pyrogram.Client = MockClient

        try:
            exec(code, exec_globals)
        except Exception as e:
            logging.exception(f"Error executing Dragon module body {origin}: {e}")
            return False
        finally:
            pyrogram.Client = original_client

        def _wrap_dragon_command(func):
            async def wrapper(app: Client, message: types.Message):
                message.command = ["."]
                return await func(app, message)
            return wrapper

        for func, flt, group in captured_handlers:
            cmd = func_to_command.get(func.__name__)
            if cmd:
                instance.command_handlers[cmd] = _wrap_dragon_command(func)
            else:
                instance._dragon_handlers.append((group, MessageHandler(func, flt)))

        self.modules.append(instance)
        self.command_handlers.update(instance.command_handlers)

        for group, handler in instance._dragon_handlers:
            self._app.add_handler(handler, group=group)

        await self.send_on_load(instance)
        return instance.name

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
            module = self.get_module(module_name)

            if not module:
                try:
                    found_class = utils.find_mod_class_in_file(module_name)
                    if found_class:
                        module = self.get_module(found_class.replace("Mod", ""))
                except Exception as e:
                    logging.error(f"Error resolving module class from file: {e}")

            if not module:
                return False

            orig = inspect.getmodule(module).__spec__.origin
            if orig != "<string>":
                set_modules = set(self._db.get(__name__, "modules", []))
                if orig in set_modules:
                    set_modules.remove(orig)
                    self._db.set("xioca.loader", "modules", list(set_modules))

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
        
        if hasattr(module, "_dragon_handlers"):
            for group, handler in module._dragon_handlers:
                try:
                    self._app.remove_handler(handler, group)
                except Exception as e:
                    logging.error(f"Error removing Dragon handler for {module.name}: {e}")
            module._dragon_handlers.clear()

        if module in self.modules:
            self.modules.remove(module)
            
        if hasattr(module, "command_handlers"):
            for cmd in list(module.command_handlers.keys()):
                if cmd in self.command_handlers:
                    del self.command_handlers[cmd]

        return module.name

    def get_module(self, name: str, by_commands_too: bool = False) -> Union[Module, None]:
        if (module := list(filter(lambda m: m.name.lower() == name.lower(), self.modules))):
            return module[0]
        if by_commands_too and name in self.command_handlers:
            return self.command_handlers[name].__self__
        return None