# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2025 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

import sys

if sys.version_info < (3, 8, 0):
    print("Требуется Python 3.8 или выше")
    sys.exit(1)


import asyncio
import argparse

from . import main, logger


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="xioca", description="Телеграм юзербот разработанный shashachkaaa",
        epilog="Канал: @XiocaINFO", add_help=False
    )
    parser.add_argument("--help", "-h", action="help",
                        help="Показать это сообщение")
    parser.add_argument("--log-level", "-lvl", dest="logLevel", default="INFO",
                        help="Установить уровень логирования. Доступно: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL или число от 0 до 50")

    return parser.parse_args()

if __name__ == "__main__":
    logger.setup_logger(parse_arguments().logLevel)
    asyncio.run(main.main())
