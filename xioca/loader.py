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
    version: Union[int, float] = None,
    name: str = None,
) -> FunctionType:
    """Обрабатывает класс модуля

    Параметры:
        name (``str``):
            Название модуля (не используется, требуется для совместимости старых модулей)

        author (``str``, optional):
            Автор модуля

        version (``int`` | ``float``, optional):
            Версия модуля
    """
    def decorator(instance: "Module"):
        """Декоратор для обработки класса модуля"""
        instance.name = instance.__name__.replace("Mod", "")
        instance.author = author
        instance.version = version
        return instance
    return decorator


@module(name="Unknown")
class Module:
    """Описание модуля"""
    name: str
    author: str
    version: Union[int, float]

    async def on_load(self, app: Client) -> Any:
        """Вызывается при загрузке модуля"""

class StringLoader(SourceLoader):
    """Загружает модуль со строки"""

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
    """Возвращает словарь из названий с функциями команд"""
    return {
        method_name[:-4].lower(): getattr(
            instance, method_name
        ) for method_name in dir(instance)
        if (
            callable(getattr(instance, method_name))
            and len(method_name) > 4
            and method_name.endswith("_cmd")
        )
    }


def get_watcher_handlers(instance: Module) -> List[FunctionType]:
    """Возвращает список из вотчеров"""
    return [
        getattr(instance, method_name)
        for method_name in dir(instance)
        if (
            callable(getattr(instance, method_name))
            and method_name.startswith("watcher")
        )
    ]


def get_message_handlers(instance: Module) -> Dict[str, FunctionType]:
    """Возвращает словарь из названий с функциями хендлеров сообщений"""
    return {
        method_name[:-16].lower(): getattr(
            instance, method_name
        ) for method_name in dir(instance)
        if (
            callable(getattr(instance, method_name))
            and len(method_name) > 16
            and method_name.endswith("_message_handler")
        )
    }


def get_callback_handlers(instance: Module) -> Dict[str, FunctionType]:
    """Возвращает словарь из названий с функциями каллбек-хендлеров"""
    return {
        method_name[:-17].lower(): getattr(
            instance, method_name
        ) for method_name in dir(instance)
        if (
            callable(getattr(instance, method_name))
            and len(method_name) > 17
            and method_name.endswith("_callback_handler")
        )
    }


def get_inline_handlers(instance: Module) -> Dict[str, FunctionType]:
    """Возвращает словарь из названий с функциями инлайн-хендлеров"""
    return {
        method_name[:-15].lower(): getattr(
            instance, method_name
        ) for method_name in dir(instance)
        if (
            callable(getattr(instance, method_name))
            and len(method_name) > 15
            and method_name.endswith("_inline_handler")
        )
    }


def on(custom_filters: Union[filters.Filter, LambdaType]) -> FunctionType:
    """Создает фильтр для команды

    Параметры:
        custom_filters (``pyrogram.filters.Filter`` | ``types.LambdaType``):
            Фильтры

    Пример:
        >>> @on(lambda _, app, message: message.chat.type == "supergroup")
        >>> async def func_cmd(
                self,
                app: pyrogram.Client,
                message: pyrogram.types.Message
            ):
        >>>     ...
    """
    def decorator(func: FunctionType):
        """Декоратор для обработки команды"""
        func._filters = (
            filters.create(custom_filters)
            if custom_filters.__module__ != "pyrogram.filters"
            else custom_filters
        )
        return func
    return decorator


def on_bot(custom_filters: LambdaType) -> FunctionType:
    """Создает фильтр для команды бота

    Параметры:
        custom_filters (``types.FunctionType`` | ``types.LambdaType``):
            Фильтры.
            Функция должна принимать параметры self, app, message/call/inline_query

    Пример:
        >>> @on_bot(lambda self, app, call: call.from_user.id == self.all_modules.me.id)
        >>> async def func_callback_handler(
                self,
                app: pyrogram.Client,
                call: aiogram.types.CallbackQuery
            ):
        >>>     ...
    """
    def decorator(func: FunctionType):
        """Декоратор для обработки команды бота"""
        func._filters = custom_filters
        return func
    return decorator

class ModulesManager:
    """Менеджер модулей"""

    def __init__(
        self,
        app: Client,
        db: db,
        me: types.User
    ) -> None:
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

    async def load(self, app: Client) -> bool:
        """Загружает менеджер модулей"""
        self.dp = dispatcher.DispatcherManager(app, self)
        await self.dp.load()

        self.bot_manager = bot.BotManager(app, self._db, self)
        await self.bot_manager.load()

        logging.info("Загрузка модулей...")

        for local_module in filter(
            lambda file_name: file_name.endswith(".py")
                and not file_name.startswith("_"), os.listdir(self._local_modules_path)
        ):
            module_name = f"xioca.modules.{local_module[:-3]}"
            file_path = os.path.join(
                os.path.abspath("."), self._local_modules_path, local_module
            )

            try:
                self.register_instance(module_name, file_path)
            except Exception as error:
                logging.exception(
                    f"Ошибка при загрузке локального модуля {module_name}: {error}")

        await self.send_on_loads()

        for custom_module in self._db.get(__name__, "modules", []):
            try:
                r = await utils.run_sync(requests.get, custom_module)
                await self.load_module(r.text, r.url)
            except requests.exceptions.RequestException as error:
                logging.exception(
                    f"Ошибка при загрузке стороннего модуля {custom_module}: {error}")

        logging.info("Менеджер модулей загружен")
        return True

    def register_instance(
        self,
        module_name: str,
        file_path: str = "",
        spec: ModuleSpec = None
    ) -> Module:
        """Регистрирует модуль"""
        spec = spec or spec_from_file_location(module_name, file_path)
        module = module_from_spec(spec)
        sys.modules[module.__name__] = module
        spec.loader.exec_module(module)

        instance = None
        for key, value in vars(module).items():
            if key.endswith("Mod") and issubclass(value, Module):
                value: Module

                for module in self.modules:
                    if module.__class__.__name__ == value.__name__:
                        self.unload_module(module, True)

                value.db = self._db
                value.all_modules = self
                value.bot = self.bot_manager.bot

                instance = value()
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

        if not instance:
            logging.error("Не удалось найти класс модуля заканчивающийся на `Mod`")

        return instance

    async def load_module(self, module_source: str, origin: str = "<string>", did_requirements: bool = False, update_callback: callable = None
) -> str:
        """Загружает сторонний модуль"""
        module_name = "xioca.modules." + (
            "".join(random.choice(string.ascii_letters + string.digits)
                    for _ in range(10))
        )

        try:
            spec = ModuleSpec(module_name, StringLoader(
                module_source, origin), origin=origin)
            instance = self.register_instance(module_name, spec=spec)
        except ModuleNotFoundError as e:
            if did_requirements:
                logging.error(f"Не удалось установить зависимости: {e}")
                return False
            
            missing_module = e.name
            logging.info(f"Обнаружен отсутствующий модуль: {missing_module}")
            
            if update_callback:
            	await update_callback("<emoji id=5328274090262275771>⏳</emoji> <b>Установка недостающего модуля:</b> <code>{missing_module}</code>...")
            
            try:
            	subprocess.run([sys.executable, "-m", "pip", "install", "--user", missing_module], check=True, capture_output=True, text=True)
            	logging.info(f"Модуль {missing_module} успешно установлен")
            except subprocess.CalledProcessError as e:
            	logging.error(f"Ошибка установки {missing_module}: {e.stderr}")
            	return False
            
            return await self.load_module(module_source, origin, True, update_callback)
            
        except Exception as e:
        	logging.exception(f"Ошибка загрузки модуля {origin}: {e}")
        	return False
        
        if not instance:
        	return False
        
        try:
        	await self.send_on_load(instance)
        except Exception as e:
        	logging.exception(f"Ошибка в on_load: {e}")
        	return False
        
        return instance.name

    async def send_on_loads(self) -> bool:
        """Отсылает команды выполнения функции"""
        for module in self.modules:
            await self.send_on_load(module)

        return True

    async def send_on_load(self, module: Module) -> bool:
        """Используется для выполнении функции после загрузки модуля"""
        try:
            await module.on_load(self._app)
        except Exception as error:
            return logging.exception(error)

        return True

    def unload_module(self, module_name: str = None, is_replace: bool = False) -> str:
        """Выгружает загруженный (если он загружен) модуль"""
        if is_replace:
            module = module_name
        else:
            module_name = utils.find_mod_class_in_file(module_name)
            if not (module := self.get_module(module_name.replace("Mod", ""))):
                logging.error(f"Модуль {module_name} не найден для выгрузки.")
                return False

            if (get_module := inspect.getmodule(module)).__spec__.origin != "<string>":
                set_modules = set(self._db.get(__name__, "modules", []))
                self._db.set("xioca.loader", "modules",
                             list(set_modules - {get_module.__spec__.origin}))

            for alias, command in self.aliases.copy().items():
                if command in module.command_handlers:
                    del self.aliases[alias]
                    del self.command_handlers[command]

        self.modules.remove(module)
        self.command_handlers = dict(
            set(self.command_handlers.items()) ^ set(module.command_handlers.items())
        )
        self.watcher_handlers = list(
            set(self.watcher_handlers) ^ set(module.watcher_handlers)
        )

        self.inline_handlers = dict(
            set(self.inline_handlers.items()) ^ set(module.inline_handlers.items())
        )
        self.callback_handlers = dict(
            set(self.callback_handlers.items()) ^ set(module.callback_handlers.items())
        )

        logging.info(f"Модуль {module.name} успешно выгружен.")
        return module.name
        
    def get_module(self, name: str, by_commands_too: bool = False) -> Union[Module, None]:
        """Ищет модуль по названию или по команде"""

        if (
            module := list(
                filter(
                    lambda module: module.name.lower() == name.lower(), self.modules
                )
            )
        ):
            return module[0]

        if by_commands_too and name in self.command_handlers:
            return self.command_handlers[name].__self__

        return None