<p align="center">
    <br>
    <b>Xioca</b> — крутой юзербот написанный на <a href="https://github.com/pyrogram/pyrogram">Pyrogram</a>
    <br>
    <a href="https://t.me/XiocaUB">Канал с обновлениями</a>
    •
    <a href="https://t.me/XiocaUB">Чат поддержки</a>
    •
    <a href="https://t.me/XiocaUB">Канал с модулями</a>
</p>

<a href="https://github.com/shashachkaaa/xioca/stargazers">
    <img src="https://badgen.net/github/stars/shashachkaaa/xioca" alt="stars">
</a>
<a href="https://github.com/shashachkaaa/xioca/watchers">
    <img src="https://badgen.net/github/watchers/shashachkaaa/xioca" alt="watchers">
</a>
<a href="https://github.com/shashachkaaa/xioca/commits/main">
    <img src="https://badgen.net/github/commits/shashachkaaa/xioca/main" alt="commits">
</a>
<br>
<a href="https://www.codefactor.io/repository/github/shashahchkaaa/xioca">
    <img src="https://www.codefactor.io/repository/github/shashachkaaa/xioca/badge" alt="CodeFactor"/>
</a>

Этот проект основан на [Sh1tN3t UserBot](https://github.com/sh1tn3t/sh1t-ub), распространяемом под лицензией [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.html).

## Изменения
- Обновлен под актуальный Pyrogram (Kurigram)
- Обновлен под актуальный Aiogram 3
- Большие изменения почти в каждом файле
- Исправлено большое количество багов
- Исправлена проблема с крашем всех сессий

<h1>Описание</h1>

Xioca — это ваш интерактивный многофункциональный помощник в Телеграме  
Многофункциональный и расширяемый юзербот позволит создавать любые модули, нужна лишь фантазия

Подключение к аккаунту происходит посредством создании новой (!) сессии

Наши преимущества:
<ul>
    <li>Удобство и простота в использовании</li>
    <li>Низкая ресурсозатраность</li>
    <li>Большой ассортимент готовых модулей</li>
    <li>Грамотное построение структуры каждого модуля</li>
    <li>Асинхронное выполнение каждой задачи</li>
    <li>Удобная загрузка и выгрузка модулей</li>
    <li>Инлайн бот</li>
</ul>


<h1>Установка</h1>

<h2>На свой сервер</h2>

Для начала нужно установить компоненты:

<pre lang="bash">
apt update && apt upgrade -y && apt install -y openssl git python3 python3-pip
</pre>

После этого клонировать репозиторий и установить зависимости:

<pre lang="bash">
git clone https://github.com/shashachkaaa/xioca.git && cd xioca
pip3 install -r requirements.txt
</pre>


<h1>Запуск</h1>

> При первом запуске потребуется ввести api_id и api_hash. Их можно получить на <a href="https://my.telegram.org">my.telegram.org</a>

<pre lang="bash">
python3 -m xioca
</pre>

вы также можете:

<pre lang="bash">
$ python3 -m xioca --help
usage: xioca [--help] [--log-level LOGLEVEL]

Телеграм юзербот разработанный sh1tn3t‘ом & shashachkaaa

optional arguments:
  --help, -h            Показать это сообщение
  --log-level LOGLEVEL, -lvl LOGLEVEL
                        Установить уровень логирования. Доступно: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL или число от 0 до 50

Канал xioca: @XiocaUB
</pre>

<h1>Пример модуля</h1>

> Больше примеров функций и полное описание смотри в файле <a href="./xioca/modules/_example.py">_example.py</a>

<pre lang="python">
from pyrogram import Client, types
from .. import loader, utils


@loader.module(name="Example")
class ExampleMod(loader.Module):
    """Описание модуля"""

    async def example_cmd(self, app: Client, message: types.Message):
        """Описание команды"""
        return await utils.answer(
            message, "Пример команды")

    @loader.on(lambda _, __, m: m and m.text == "Привет, это проверка вотчера xioca")
    async def watcher(self, app: Client, message: types.Message):
        return await message.reply(
            "Привет, все работает отлично")
</pre>


<h1>Ссылки</h1>

<ul>
    <li><a href="https://t.me/XiocaUB">Модули</a></li>
</ul>
