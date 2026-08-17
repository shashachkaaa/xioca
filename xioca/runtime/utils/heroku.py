# ©️ Codrago, 2024-2030
# This file is a part of Heroku Userbot
# 🌐 https://github.com/coddrago/Heroku
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import logging
import os

import herokutl

parser = herokutl.utils.sanitize_parse_mode("html")
logger = logging.getLogger(__name__)


def get_version_raw() -> str:
    """
    Get the version of the userbot
    :return: Version in format %s.%s.%s
    """
    from .. import version

    return ".".join(map(str, list(version.__version__)))


def get_base_dir() -> str:
    """
    Get directory of this file
    :return: Directory of this file
    """
    return get_dir(__file__)


def get_dir(mod: str = None) -> str:
    """
    Get directory of given module
    :param mod: Module's `__file__` to get directory of
    :return: Directory of given module

    XIOCA: было ``return os.getcwd() + "/heroku"`` - аргумент игнорировался,
    путь был жёстко зашит под layout Heroku и зависел от рабочей директории
    процесса (запуск не из корня репозитория ломал поиск модулей).

    Возвращаем каталог пакета ``xioca`` - на уровень выше рантайма, - чтобы
    ``get_base_dir() + "/modules"`` указывал на встроенные модули Xioca, а не
    на каталог внутри вендоренного рантайма. От cwd больше не зависит.
    """
    return os.path.dirname(  # xioca
        os.path.dirname(  # xioca/runtime
            os.path.dirname(os.path.abspath(__file__))  # xioca/runtime/utils
        )
    )


version = get_version_raw
