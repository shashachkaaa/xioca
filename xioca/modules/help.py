# 📦 Xioca UserBot
# 👤 Copyright (C) 2025-2026 shashachkaaa
#
# ⚖️ Licensed under GNU AGPL v3.0
# 🌐 Source: https://github.com/shashachkaaa/xioca
# 📝 Docs:   https://www.gnu.org/licenses/agpl-3.0.html

from herokutl.tl.custom import Message

from xioca import __system_mod__

from .. import loader, utils
from ..inline.types import InlineCall


@loader.tds
class XiocaHelpMod(loader.Module):
    """Помощь по командам юзербота"""

    strings = {
        "name": 'XiocaHelp',
        'cfg_max': 'Maximum modules shown on one help page',
        'cfg_sys_emoji': 'Emoji marking system modules',
        'cfg_loaded_emoji': 'Emoji marking loaded modules',
        'module_row': '\n<b>{prefix} {module}</b>: ({cmds})',
        'header_stats': '<b>🌙 Total <code>{total}</code> modules, <code>{hidden}</code> hidden, <code>{shown}</code> shown</b>\n',
        'btn_back': '⬅️ Back',
        'btn_next': 'Next ➡️',
        'mod_not_found': '<emoji id=5210952531676504517>❌</emoji> <b>Module</b> «<code>{mod}</code>» <b>not found</b>',
        'no_desc': 'No description',
        'cmd_fmt': '<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}',
        'inline_fmt': '<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}',
        'header_mod': '<b><emoji id=5195083327597456039>🌙</emoji> Module:</b> <code>{mod}</code>\n',
        'header_auth': '<b><emoji id=5237922302070367159>❤️</emoji> Author:</b> <code>{auth}</code>\n',
        'header_ver': '<b><emoji id=5226929552319594190>0️⃣</emoji> Version:</b> <code>{ver}</code>\n',
        'header_desc': '\n<b><emoji id=5197269100878907942>✍️</emoji> Description:</b>\n    ╰ {desc}\n\n',
        'inline_usage': 'Use: @bot help [page]',
        'inline_title': 'Command Help',
        'err_load': 'Failed to load module list',
        'err_title': 'Error',
        'mod_list': 'Module List',
        'err_page': 'Error loading page',
    }

    strings_ru = {
        'cfg_max': 'Максимум модулей на одной странице помощи',
        'cfg_sys_emoji': 'Эмодзи для отметки системных модулей',
        'cfg_loaded_emoji': 'Эмодзи для отметки загруженных модулей',
        'module_row': '\n<b>{prefix} {module}</b>: ({cmds})',
        'header_stats': '<b>🌙 Всего <code>{total}</code> модулей, <code>{hidden}</code> скрыто, <code>{shown}</code> отображено</b>\n',
        'btn_back': '⬅️ Назад',
        'btn_next': 'Вперёд ➡️',
        'mod_not_found': '<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>не найден</b>',
        'no_desc': 'Нет описания',
        'cmd_fmt': '<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}',
        'inline_fmt': '<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}',
        'header_mod': '<b><emoji id=5195083327597456039>🌙</emoji> Модуль:</b> <code>{mod}</code>\n',
        'header_auth': '<b><emoji id=5237922302070367159>❤️</emoji> Автор:</b> <code>{auth}</code>\n',
        'header_ver': '<b><emoji id=5226929552319594190>0️⃣</emoji> Версия:</b> <code>{ver}</code>\n',
        'header_desc': '\n<b><emoji id=5197269100878907942>✍️</emoji> Описание:</b>\n    ╰ {desc}\n\n',
        'inline_usage': 'Используйте: @бот help [страница]',
        'inline_title': 'Помощь по командам',
        'err_load': 'Не удалось загрузить список модулей',
        'err_title': 'Ошибка',
        'mod_list': 'Список модулей',
        'err_page': 'Ошибка загрузки страницы',
    }

    strings_be = {
        'module_row': '\n<b>{prefix} {module}</b>: ({cmds})',
        'header_stats': '<b>🌙 Усяго <code>{total}</code> модуляў, <code>{hidden}</code> схавана, <code>{shown}</code> адлюстравана</b>\n',
        'btn_back': '⬅️ Назад',
        'btn_next': 'Наперад ➡️',
        'mod_not_found': '<emoji id=5210952531676504517>❌</emoji> <b>Модуль</b> «<code>{mod}</code>» <b>не знойдзены</b>',
        'no_desc': 'Няма апісання',
        'cmd_fmt': '<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}',
        'inline_fmt': '<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}',
        'header_mod': '<b><emoji id=5195083327597456039>🌙</emoji> Модуль:</b> <code>{mod}</code>\n',
        'header_auth': '<b><emoji id=5237922302070367159>❤️</emoji> Аўтар:</b> <code>{auth}</code>\n',
        'header_ver': '<b><emoji id=5226929552319594190>0️⃣</emoji> Версія:</b> <code>{ver}</code>\n',
        'header_desc': '\n<b><emoji id=5197269100878907942>✍️</emoji> Апісанне:</b>\n    ╰ {desc}\n\n',
        'inline_usage': 'Выкарыстоўвайце: @бот help [старонка]',
        'inline_title': 'Дапамога па камандах',
        'err_load': 'Не ўдалося загрузіць спіс модуляў',
        'err_title': 'Памылка',
        'mod_list': 'Спіс модуляў',
        'err_page': 'Памылка загрузкі старонкі',
    }

    strings_de = {
        'module_row': '\n<b>{prefix} {module}</b>: ({cmds})',
        'header_stats': '<b>🌙 Insgesamt <code>{total}</code> Module, <code>{hidden}</code> versteckt, <code>{shown}</code> angezeigt</b>\n',
        'btn_back': '⬅️ Zurück',
        'btn_next': 'Weiter ➡️',
        'mod_not_found': '<emoji id=5210952531676504517>❌</emoji> <b>Modul</b> «<code>{mod}</code>» <b>nicht gefunden</b>',
        'no_desc': 'Keine Beschreibung',
        'cmd_fmt': '<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}',
        'inline_fmt': '<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}',
        'header_mod': '<b><emoji id=5195083327597456039>🌙</emoji> Modul:</b> <code>{mod}</code>\n',
        'header_auth': '<b><emoji id=5237922302070367159>❤️</emoji> Autor:</b> <code>{auth}</code>\n',
        'header_ver': '<b><emoji id=5226929552319594190>0️⃣</emoji> Version:</b> <code>{ver}</code>\n',
        'header_desc': '\n<b><emoji id=5197269100878907942>✍️</emoji> Beschreibung:</b>\n    ╰ {desc}\n\n',
        'inline_usage': 'Verwendung: @bot help [Seite]',
        'inline_title': 'Befehlshilfe',
        'err_load': 'Modulliste konnte nicht geladen werden',
        'err_title': 'Fehler',
        'mod_list': 'Modulliste',
        'err_page': 'Fehler beim Laden der Seite',
    }

    strings_es = {
        'module_row': '\n<b>{prefix} {module}</b>: ({cmds})',
        'header_stats': '<b>🌙 Total <code>{total}</code> módulos, <code>{hidden}</code> ocultos, <code>{shown}</code> mostrados</b>\n',
        'btn_back': '⬅️ Atrás',
        'btn_next': 'Siguiente ➡️',
        'mod_not_found': '<emoji id=5210952531676504517>❌</emoji> <b>Módulo</b> «<code>{mod}</code>» <b>no encontrado</b>',
        'no_desc': 'Sin descripción',
        'cmd_fmt': '<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}',
        'inline_fmt': '<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}',
        'header_mod': '<b><emoji id=5195083327597456039>🌙</emoji> Módulo:</b> <code>{mod}</code>\n',
        'header_auth': '<b><emoji id=5237922302070367159>❤️</emoji> Autor:</b> <code>{auth}</code>\n',
        'header_ver': '<b><emoji id=5226929552319594190>0️⃣</emoji> Versión:</b> <code>{ver}</code>\n',
        'header_desc': '\n<b><emoji id=5197269100878907942>✍️</emoji> Descripción:</b>\n    ╰ {desc}\n\n',
        'inline_usage': 'Uso: @bot help [página]',
        'inline_title': 'Ayuda de comandos',
        'err_load': 'Error al cargar la lista de módulos',
        'err_title': 'Error',
        'mod_list': 'Lista de módulos',
        'err_page': 'Error al cargar la página',
    }

    strings_fr = {
        'module_row': '\n<b>{prefix} {module}</b>: ({cmds})',
        'header_stats': '<b>🌙 Total <code>{total}</code> modules, <code>{hidden}</code> cachés, <code>{shown}</code> affichés</b>\n',
        'btn_back': '⬅️ Retour',
        'btn_next': 'Suivant ➡️',
        'mod_not_found': '<emoji id=5210952531676504517>❌</emoji> <b>Module</b> «<code>{mod}</code>» <b>introuvable</b>',
        'no_desc': 'Pas de description',
        'cmd_fmt': '<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}',
        'inline_fmt': '<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}',
        'header_mod': '<b><emoji id=5195083327597456039>🌙</emoji> Module :</b> <code>{mod}</code>\n',
        'header_auth': '<b><emoji id=5237922302070367159>❤️</emoji> Auteur :</b> <code>{auth}</code>\n',
        'header_ver': '<b><emoji id=5226929552319594190>0️⃣</emoji> Version :</b> <code>{ver}</code>\n',
        'header_desc': '\n<b><emoji id=5197269100878907942>✍️</emoji> Description :</b>\n    ╰ {desc}\n\n',
        'inline_usage': 'Utilisation : @bot help [page]',
        'inline_title': 'Aide des commandes',
        'err_load': 'Échec du chargement de la liste des modules',
        'err_title': 'Erreur',
        'mod_list': 'Liste des modules',
        'err_page': 'Erreur lors du chargement de la page',
    }

    strings_it = {
        'module_row': '\n<b>{prefix} {module}</b>: ({cmds})',
        'header_stats': '<b>🌙 Totale <code>{total}</code> moduli, <code>{hidden}</code> nascosti, <code>{shown}</code> visualizzati</b>\n',
        'btn_back': '⬅️ Indietro',
        'btn_next': 'Avanti ➡️',
        'mod_not_found': '<emoji id=5210952531676504517>❌</emoji> <b>Modulo</b> «<code>{mod}</code>» <b>non trovato</b>',
        'no_desc': 'Nessuna descrizione',
        'cmd_fmt': '<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}',
        'inline_fmt': '<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}',
        'header_mod': '<b><emoji id=5195083327597456039>🌙</emoji> Modulo:</b> <code>{mod}</code>\n',
        'header_auth': '<b><emoji id=5237922302070367159>❤️</emoji> Autore:</b> <code>{auth}</code>\n',
        'header_ver': '<b><emoji id=5226929552319594190>0️⃣</emoji> Versione:</b> <code>{ver}</code>\n',
        'header_desc': '\n<b><emoji id=5197269100878907942>✍️</emoji> Descrizione:</b>\n    ╰ {desc}\n\n',
        'inline_usage': 'Uso: @bot help [pagina]',
        'inline_title': 'Aiuto comandi',
        'err_load': "Impossibile caricare l'elenco dei moduli",
        'err_title': 'Errore',
        'mod_list': 'Elenco moduli',
        'err_page': 'Errore nel caricamento della pagina',
    }

    strings_kk = {
        'module_row': '\n<b>{prefix} {module}</b>: ({cmds})',
        'header_stats': '<b>🌙 Барлығы <code>{total}</code> модуль, <code>{hidden}</code> жасырылған, <code>{shown}</code> көрсетілген</b>\n',
        'btn_back': '⬅️ Артқа',
        'btn_next': 'Алға ➡️',
        'mod_not_found': '<emoji id=5210952531676504517>❌</emoji> «<code>{mod}</code>» <b>модулі табылмады</b>',
        'no_desc': 'Сипаттама жоқ',
        'cmd_fmt': '<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}',
        'inline_fmt': '<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}',
        'header_mod': '<b><emoji id=5195083327597456039>🌙</emoji> Модуль:</b> <code>{mod}</code>\n',
        'header_auth': '<b><emoji id=5237922302070367159>❤️</emoji> Авторы:</b> <code>{auth}</code>\n',
        'header_ver': '<b><emoji id=5226929552319594190>0️⃣</emoji> Нұсқасы:</b> <code>{ver}</code>\n',
        'header_desc': '\n<b><emoji id=5197269100878907942>✍️</emoji> Сипаттамасы:</b>\n    ╰ {desc}\n\n',
        'inline_usage': 'Қолдану: @bot help [бет]',
        'inline_title': 'Командалар бойынша көмек',
        'err_load': 'Модульдер тізімін жүктеу мүмкін болмады',
        'err_title': 'Қате',
        'mod_list': 'Модульдер тізімі',
        'err_page': 'Бетті жүктеу қатесі',
    }

    strings_uz = {
        'module_row': '\n<b>{prefix} {module}</b>: ({cmds})',
        'header_stats': "<b>🌙 Jami <code>{total}</code> modul, <code>{hidden}</code> yashirin, <code>{shown}</code> ko'rsatilgan</b>\n",
        'btn_back': '⬅️ Orqaga',
        'btn_next': 'Oldinga ➡️',
        'mod_not_found': '<emoji id=5210952531676504517>❌</emoji> «<code>{mod}</code>» <b>moduli topilmadi</b>',
        'no_desc': "Tavsif yo'q",
        'cmd_fmt': '<emoji id=5471978009449731768>👉</emoji> <code>{cmd}</code>\n    ╰ {desc}',
        'inline_fmt': '<emoji id=5372981976804366741>🤖</emoji> <code>@{bot} {cmd}</code>\n    ╰ {desc}',
        'header_mod': '<b><emoji id=5195083327597456039>🌙</emoji> Modul:</b> <code>{mod}</code>\n',
        'header_auth': '<b><emoji id=5237922302070367159>❤️</emoji> Muallif:</b> <code>{auth}</code>\n',
        'header_ver': '<b><emoji id=5226929552319594190>0️⃣</emoji> Versiya:</b> <code>{ver}</code>\n',
        'header_desc': '\n<b><emoji id=5197269100878907942>✍️</emoji> Tavsif:</b>\n    ╰ {desc}\n\n',
        'inline_usage': "Qo'llanilishi: @bot help [sahifa]",
        'inline_title': "Buyruqlar bo'yicha yordam",
        'err_load': "Modullar ro'yxatini yuklab bo'lmadi",
        'err_title': 'Xato',
        'mod_list': "Modullar ro'yxati",
        'err_page': 'Sahifani yuklashda xato',
    }


    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "max_help_modules",
                20,
                lambda: self.strings("cfg_max"),
                validator=loader.validators.Integer(minimum=5, maximum=100),
            ),
            loader.ConfigValue(
                "system_mods_emoji",
                "▪",
                lambda: self.strings("cfg_sys_emoji"),
                validator=loader.validators.String(max_len=8),
            ),
            loader.ConfigValue(
                "loaded_mods_emoji",
                "▫",
                lambda: self.strings("cfg_loaded_emoji"),
                validator=loader.validators.String(max_len=8),
            ),
        )

    def _is_system(self, module) -> bool:
        # Сверяем и имя класса, и отображаемое имя: они могут расходиться
        # (XiocaConfigMod / "XiocaConfig"), и раньше модуль из-за этого молча
        # показывался как сторонний
        names = {
            type(module).__name__.removesuffix("Mod"),
            getattr(module, "name", ""),
        }
        return bool(names & set(__system_mod__))

    def _sorted_modules(self) -> list:
        """Системные модули идут первыми - так же, как было в Xioca"""
        mods = list(self.allmodules.modules)
        return sorted(mods, key=lambda m: (not self._is_system(m), m.name.lower()))

    def _page(self, page: int) -> tuple:
        """Возвращает текст страницы и её номер, приведённый к границам"""
        per_page = self.config["max_help_modules"]
        modules = self._sorted_modules()
        total_pages = max(1, -(-len(modules) // per_page))
        page = max(0, min(page, total_pages - 1))

        chunk = modules[page * per_page:(page + 1) * per_page]

        rows = []
        for module in chunk:
            names = [f"<code>{utils.escape_html(c)}</code>" for c in module.commands]
            names += [
                f"🎹 <code>{utils.escape_html(c)}</code>"
                for c in getattr(module, "inline_handlers", {})
            ]

            if not names:
                continue

            rows.append(
                self.strings("module_row").format(
                    prefix=(
                        self.config["system_mods_emoji"]
                        if self._is_system(module)
                        else self.config["loaded_mods_emoji"]
                    ),
                    module=utils.escape_html(module.name),
                    cmds=" | ".join(names),
                )
            )

        header = self.strings("header_stats").format(
            total=len(modules), hidden=0, shown=len(chunk)
        )

        return header + "".join(rows), page, total_pages

    def _markup(self, page: int, total_pages: int) -> list:
        if total_pages <= 1:
            return []

        row = []
        if page > 0:
            row.append(
                {
                    "text": self.strings("btn_back"),
                    "callback": self._turn,
                    "args": (page - 1,),
                }
            )

        row.append({"text": f"{page + 1}/{total_pages}", "data": "noop"})

        if page < total_pages - 1:
            row.append(
                {
                    "text": self.strings("btn_next"),
                    "callback": self._turn,
                    "args": (page + 1,),
                }
            )

        return [row]

    async def _turn(self, call: InlineCall, page: int):
        text, page, total_pages = self._page(page)
        await call.edit(text=text, reply_markup=self._markup(page, total_pages))

    def _module_help(self, module) -> str:
        prefix = utils.escape_html(self.get_prefix())

        lines = [self.strings("header_mod").format(mod=utils.escape_html(module.name))]

        author = getattr(module, "author", None)
        if author:
            lines.append(
                self.strings("header_auth").format(auth=utils.escape_html(str(author)))
            )

        version = getattr(module, "version", None)
        if version:
            lines.append(
                self.strings("header_ver").format(ver=utils.escape_html(str(version)))
            )

        lines.append(
            self.strings("header_desc").format(
                desc=utils.escape_html(module.__doc__ or self.strings("no_desc"))
            )
        )

        for name, func in module.commands.items():
            lines.append(
                self.strings("cmd_fmt").format(
                    cmd=prefix + utils.escape_html(name),
                    desc=utils.escape_html(
                        (func.__doc__ or self.strings("no_desc")).strip()
                    ),
                )
                + "\n"
            )

        return "".join(lines)

    @loader.command()
    async def helpcmd(self, message: Message):
        """[модуль] - список модулей или помощь по конкретному"""
        args = utils.get_args_raw(message)

        if args:
            module = self.lookup(args)
            if not module:
                await utils.answer(
                    message,
                    self.strings("mod_not_found").format(mod=utils.escape_html(args)),
                )
                return

            await utils.answer(message, self._module_help(module))
            return

        text, page, total_pages = self._page(0)

        if total_pages > 1:
            await self.inline.form(
                message=message,
                text=text,
                reply_markup=self._markup(page, total_pages),
            )
            return

        await utils.answer(message, text)
