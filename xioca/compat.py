# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

"""Алиасы пакетов для сторонних модулей Hikka и Heroku.

Модули, написанные для этих юзерботов, импортируют ядро абсолютно::

    from heroku import loader, utils
    from hikka.inline.types import InlineCall

У нас ядро называется ``xioca.runtime``, поэтому такие импорты падают с
ImportError. Загрузчик на это реагирует попыткой доустановить пакет с этим
именем - и в логах появляется ``No matching distribution found for heroku``,
после чего модуль не грузится вовсе.

Регистрируем ``heroku`` и ``hikka`` как псевдонимы ``xioca.runtime`` через
meta path finder: он покрывает и вложенные пути (``heroku.inline.types``),
которые перечислить заранее нельзя.
"""

import importlib
import sys
from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec

__all__ = ["install"]

# Имена, под которыми сторонние модули знают ядро
ALIASES = ("heroku", "hikka")

TARGET = "xioca.runtime"


class _AliasLoader(Loader):
    def __init__(self, real_name: str) -> None:
        self.real_name = real_name

    def create_module(self, spec: ModuleSpec):
        # Возвращаем уже существующий модуль ядра: копии нам не нужны,
        # иначе состояние (например, реестр загруженных модулей) разъедется
        return importlib.import_module(self.real_name)

    def exec_module(self, module) -> None:
        """Модуль уже выполнен при импорте оригинала"""


class _AliasFinder(MetaPathFinder):
    def find_spec(self, fullname: str, path=None, target=None):
        for alias in ALIASES:
            if fullname != alias and not fullname.startswith(f"{alias}."):
                continue

            real_name = TARGET + fullname[len(alias):]

            try:
                importlib.import_module(real_name)
            except ImportError:
                # Такого модуля нет и в нашем ядре - пусть ошибка будет
                # честной, про реальное имя
                return None

            return ModuleSpec(fullname, _AliasLoader(real_name))

        return None


def install() -> None:
    """Включает алиасы. Повторный вызов безопасен."""
    if any(isinstance(finder, _AliasFinder) for finder in sys.meta_path):
        return

    sys.meta_path.insert(0, _AliasFinder())
