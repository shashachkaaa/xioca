# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

from datetime import datetime

__authors__ = "shashachkaaa - https://github.com/shashachkaa, https://t.me/shashachkaaa"
__license__ = "GNU Affero General Public License v3.0"
__copyright__ = "Copyright (C) 2025-2026 shashachkaaa"

__version__ = "2.8.0"
__start_time__ = datetime.now()
__system_mod__ = ["loader", "help", "tester", "updater", "information", "executor", "settings", "terminal", "info", "botmanager", "eval", "evaluator", "configurator"]
__get_version_url__ = "https://raw.githubusercontent.com/shashachkaaa/xioca/refs/heads/main/xioca/__init__.py"
__get_commits_url__ = f"https://api.github.com/repos/shashachkaaa/xioca/commits"

__update_desc__ = """
🆕 Added (Новое)

Новый модуль конфигуратора
xioca/modules/configurator.py

Полноценный inline-конфигуратор (.config)

Поддержка ModuleConfig

Inline-ввод значений с кнопкой Set

Поддержка chosen_inline_result (Apply по выбору результата)

Пагинация, скрытые параметры, авто-рендер типов


Новый модуль spam.py
xioca/modules/spam.py
(утилитарный модуль для работы со спам/массовыми действиями)

Новый системный модуль dragon.py
xioca/dragon.py
(служебная логика / системные расширения ядра) Xioca теперь поддерживает Dragon Userbot модули


Поддержка ChosenInlineResult в ядре

Теперь бот получает событие выбора inline-результата

Используется, например, для конфигуратора (Apply)

---

🔄 Changed (Изменения)

Ядро бота

xioca/bot/core.py

Зарегистрирован обработчик chosen_inline_result

Улучшена регистрация событий polling


xioca/bot/events.py

Добавлен _chosen_inline_result_handler

ContinuePropagation и StopPropagation больше не логируются как ошибки

Исправлена логика вызова message-handlers


Dispatcher

xioca/dispatcher.py

Исправлен спам логов из-за pyrogram.ContinuePropagation

Корректная обработка цепочки хендлеров


Подготовка под динамическую локализацию и автоперевод


requirements.txt

Актуализированы зависимости под новые возможности


token_manager

xioca/bot/token_manager.py

Улучшена стабильность и логика работы с токенами

---

🐞 Fixed (Исправления)

Исправлены ложные ERROR-логи при:

ContinuePropagation

no running event loop

Исправлены отступы и логика в логгере

Устранён спам ошибок при inline / callback обработке

---

⚠️ Important notes

Для работы inline-Apply должен быть включён Inline Feedback
(@BotFather → /setinlinefeedback → Enabled)

Новый конфигуратор использует ModuleConfig; старые модули без self.config продолжают работать
"""

import json as _json
from pathlib import Path as _Path

__version__ = globals().get("__version__", "0.0.0")
__changelog__ = globals().get("__changelog__", "")

try:
    _rp = _Path(__file__).resolve().parent.parent / "release.json"
    if _rp.exists():
        _meta = _json.loads(_rp.read_text(encoding="utf-8"))
        __version__ = str(_meta.get("version") or __version__)
        __changelog__ = str(_meta.get("changelog") or __changelog__)
except Exception:
    pass

