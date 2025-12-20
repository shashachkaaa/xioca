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

from datetime import datetime

__authors__ = "Sh1tN3t - https://github.com/sh1tn3t https://t.me/sh1tn3t | shashachkaaa - https://github.com/shashachkaa, https://t.me/shashachkaaa"
__license__ = "GNU Affero General Public License v3.0"
__copyright__ = "Copyright (C) 2020-2021 Sh1tN3t"

__version__ = "2.7.1"
__start_time__ = datetime.now()
__system_mod__ = ["loader", "help", "tester", "updater", "information", "executor", "settings", "terminal", "info", "botmanager", "eval", "evaluator"]
__get_version_url__ = "https://raw.githubusercontent.com/shashachkaaa/xioca/refs/heads/main/xioca/__init__.py"
__get_commits_url__ = f"https://api.github.com/repos/shashachkaaa/xioca/commits"

__update_desc__ = """Улучшена система логирования: Теперь при первом запуске чат для логов создается корректно. Логи отправляются в специальный канал, не забивая личные сообщения.
Оптимизация установки модулей: Исправлена ошибка «зависания» поврежденных модулей. Если установка не удалась, временные файлы теперь полностью удаляются, не оставляя мусора в директории modules.
Редизайн логгера: Полностью переработано оформление системных сообщений. Убрана лишняя информация, логи стали более читаемыми и понятными.
Обновление инфраструктуры: Актуализированы все ссылки на репозитории внутри исходного кода.
"""
