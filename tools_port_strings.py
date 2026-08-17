"""Извлекает strings из модуля Xioca (pyrogram) в формат Heroku.

Xioca:   strings = {"ru": {...}, "en": {...}, ...}
Heroku:  strings = {"name": ..., **en}; strings_ru = {...}; strings_be = {...}

Переносим значения дословно через ast, без ручного перенабора: 9 языков
на 12 модулей - это тысячи строк, любая опечатка молча ломает перевод.
"""

import ast
import sys


def extract(path: str) -> dict:
    tree = ast.parse(open(path, encoding="utf-8").read())

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(t, ast.Name) and t.id == "strings" for t in node.targets
        ):
            continue
        return ast.literal_eval(node.value)

    return {}


def render(langs: dict, module_name: str) -> str:
    out = []

    en = langs.get("en", {})
    body = ",\n".join(f"        {k!r}: {v!r}" for k, v in en.items())
    out.append(f'    strings = {{\n        "name": {module_name!r},\n{body},\n    }}\n')

    for code, values in langs.items():
        if code == "en":
            continue
        body = ",\n".join(f"        {k!r}: {v!r}" for k, v in values.items())
        out.append(f"    strings_{code} = {{\n{body},\n    }}\n")

    return "\n".join(out)


if __name__ == "__main__":
    src, name = sys.argv[1], sys.argv[2]
    langs = extract(src)
    print(f"# языков: {len(langs)} -> {', '.join(langs)}", file=sys.stderr)
    print(f"# ключей в en: {len(langs.get('en', {}))}", file=sys.stderr)
    print(render(langs, name))
