# 📦 Xioca UserBot
# 👤 Copyright (C) 2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Callable, Optional

from .validators import Validator, String


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
    """Config container stored in DB.

    The config is bound to a module instance via `bind()`. Values are stored
    in the module's DB table and validated through validators.
    """

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
