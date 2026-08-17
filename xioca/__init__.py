# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import json as _json
from datetime import datetime
from pathlib import Path as _Path

__authors__ = "shashachkaaa - https://github.com/shashachkaa, https://t.me/shashachkaaa"
__license__ = "GNU Affero General Public License v3.0"
__copyright__ = "Copyright (C) 2025-2026 shashachkaaa"

__version__ = "3.0.0"
__changelog__ = ""
__start_time__ = datetime.now()

__get_version_url__ = (
    "https://raw.githubusercontent.com/shashachkaaa/xioca/refs/heads/main/xioca/__init__.py"
)
__get_commits_url__ = "https://api.github.com/repos/shashachkaaa/xioca/commits"

# Модули, которые нельзя выгрузить командой пользователя.
#
# Имена соответствуют классам модулей в формате рантайма (<Name>Mod без
# суффикса), а не именам файлов, как было в ядре на pyrogram: рантайм
# резолвит модули по имени класса, и старый список из имён файлов
# ("loader", "help", "information", ...) там просто ни с чем не совпадал бы.
__system_mod__ = [
    "XiocaInfo",
    "XiocaTerminal",
]

try:
    _rp = _Path(__file__).resolve().parent.parent / "release.json"
    if _rp.exists():
        _meta = _json.loads(_rp.read_text(encoding="utf-8"))
        __version__ = str(_meta.get("version") or __version__)
        __changelog__ = str(_meta.get("changelog") or __changelog__)
except Exception:
    pass
