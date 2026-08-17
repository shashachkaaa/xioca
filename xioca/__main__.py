# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

"""Точка входа Xioca.

Запуск: ``python3 -m xioca``

Загрузкой, диспетчеризацией и инлайн-ботом занимается рантайм в
``xioca/runtime`` (адаптирован из Heroku UserBot, см. runtime/NOTICE.md).
Здесь только то, что специфично для Xioca: проверка версии Python,
регистрация парс-мода под разметку языковых паков Xioca и запуск.
"""

import sys

MIN_PYTHON = (3, 10)

if sys.version_info < MIN_PYTHON:
    # Рантайм требует 3.10+; сообщаем внятно, а не падаем на синтаксисе
    print(
        f"Требуется Python {'.'.join(map(str, MIN_PYTHON))} или выше, "
        f"установлен {'.'.join(map(str, sys.version_info[:3]))}"
    )
    sys.exit(1)


def main() -> None:
    from . import __version__
    from .parse_mode import install as install_parse_mode

    # Строго до импорта рантайма: он и модули разбирают HTML своими
    # ссылками на парсер herokutl, а языковые паки Xioca размечены как
    # <emoji id=…> - на этом синтаксисе штатный парсер падает
    install_parse_mode()

    from .runtime import main as runtime

    print(f"🌙 Xioca UserBot {__version__}")

    runtime.heroku.main()


if __name__ == "__main__":
    main()
