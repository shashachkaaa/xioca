# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

"""Парс-мод HTML для herokutl, совместимый с синтаксисом Xioca.

Xioca (на pyrogram) размечает премиум-эмодзи как ``<emoji id=123>🌙</emoji>``.
herokutl ожидает ``<emoji document_id=123>`` либо ``<tg-emoji emoji-id=123>``
и **падает** с ``KeyError: 'document_id'`` на варианте pyrogram, а не игнорирует
его. Все языковые паки Xioca написаны в старом синтаксисе, поэтому вместо
массовой правки строк мы нормализуем разметку перед парсингом.

Использование::

    from .parse_mode import XiocaParseMode

    client.parse_mode = XiocaParseMode()
"""

import re
from typing import List, Tuple

from herokutl.extensions import html as tl_html
from herokutl.tl.types import MessageEntityCustomEmoji, TypeMessageEntity

__all__ = ["XiocaParseMode", "normalize_custom_emoji"]

# <emoji id=123>, <emoji id="123">, <emoji id='123'>
_EMOJI_ID_RE = re.compile(
    r"<emoji\s+id\s*=\s*[\"']?(\d+)[\"']?\s*>",
    re.IGNORECASE,
)


def normalize_custom_emoji(text: str) -> str:
    """Приводит ``<emoji id=…>`` к понятному herokutl ``<emoji document_id=…>``.

    Уже корректная разметка (``document_id``/``tg-emoji``) не трогается.
    """
    if not text or "<emoji" not in text:
        return text

    return _EMOJI_ID_RE.sub(r'<emoji document_id="\1">', text)


class XiocaParseMode:
    """HTML-парсер herokutl, понимающий синтаксис премиум-эмодзи pyrogram."""

    @staticmethod
    def parse(text: str) -> Tuple[str, List[TypeMessageEntity]]:
        return tl_html.parse(normalize_custom_emoji(text))

    @staticmethod
    def unparse(text: str, entities: List[TypeMessageEntity]) -> str:
        return tl_html.unparse(text, entities)
