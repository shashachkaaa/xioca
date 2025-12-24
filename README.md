<p align="center">
    <br>
    <h1 align="center">🌙 <b>Xioca</b></h1>
    <p align="center">Модульный юзербот для Telegram на <a href="https://github.com/pyrogram/pyrogram">Pyrogram</a></p>
    <br>
    <div align="center">
        <a href="https://t.me/XiocaINFO">Канал</a> •
        <a href="https://t.me/XiocaSUPPORT">Поддержка</a> •
        <a href="https://xioca.ferz.live/docs">Документация</a>
    </div>
</p>

<div align="center">
    <a href="https://github.com/shashachkaaa/xioca/stargazers">
        <img src="https://img.shields.io/github/stars/shashachkaaa/xioca?style=for-the-badge&color=4af" alt="stars">
    </a>
    <a href="https://github.com/shashachkaaa/xioca/watchers">
        <img src="https://img.shields.io/github/watchers/shashachkaaa/xioca?style=for-the-badge&color=4af" alt="watchers">
    </a>
    <a href="https://github.com/shashachkaaa/xioca/commits/main">
        <img src="https://img.shields.io/github/commit-activity/m/shashachkaaa/xioca?style=for-the-badge&color=4af" alt="commits">
    </a>
    <a href="https://www.codefactor.io/repository/github/shashahchkaaa/xioca">
        <img src="https://img.shields.io/codefactor/grade/github/shashachkaaa/xioca?style=for-the-badge&color=4af" alt="CodeFactor">
    </a>
</div>

---

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Pyrogram-2.0+-green?style=flat-square&logo=telegram" alt="Pyrogram">
  <img src="https://img.shields.io/badge/Aiogram-3.0+-orange?style=flat-square&logo=telegram" alt="Aiogram">
</div>

## 🚀 **О проекте**

Xioca — ваш интерактивный многофункциональный помощник в Telegram с:
- 🔥 Низкой ресурсозатратностью
- 📦 Модульной системой
- ⚡ Асинхронной работой
- 🤖 Встроенным инлайн-ботом

> Основано на [Sh1tN3t UserBot](https://github.com/sh1tn3t/sh1t-ub) (AGPL-3.0)

## ✨ **Особенности**
```python
@loader.module(author="shashachkaaa", version=1)
class ExampleMod(loader.Module):
    """Пример модуля Xioca"""
    
    async def example_cmd(self, app, message):
        """Интерактивная команда"""
        await message.edit("🚀 Работает!")
```

> Полная документация на [Xioca docs](https://xioca.ferz.live/docs)

## 🛠 **Установка**
```bash
# Установка зависимостей
apt update && apt upgrade -y
apt install -y openssl git python3 python3-pip

wget -qO - https://raw.githubusercontent.com/shashachkaaa/xioca/main/install.sh | bash
```

## 🚀 **Запуск**
```bash
python3 -m xioca
```
> При первом запуске потребуется ввести API данные с [my.telegram.org](https://my.telegram.org)

<details>
<summary><b>📌 Дополнительные параметры</b></summary>

```bash
$ python3 -m xioca --help
usage: xioca [--help] [--log-level LOGLEVEL]

Телеграм юзербот разработанный sh1tn3t‘ом & shashachkaaa

optional arguments:
  --help, -h            Показать это сообщение
  --log-level LOGLEVEL, -lvl LOGLEVEL
                        Уровень логирования (DEBUG, INFO, WARNING, ERROR)
```
</details>

## 📚 **Документация**
Полная документация по модулям и API доступна на:  
👉 [xioca.ferz.live/docs](https://xioca.ferz.live/docs)

## 🌐 **Ссылки**
<div align="center">
  <a href="https://t.me/XiocaSUPPORT">
    <img src="https://img.icons8.com/color/48/000000/telegram-app--v1.png" width="40" alt="Telegram">
  </a>
  <a href="https://github.com/shashachkaaa/xioca">
    <img src="https://img.icons8.com/ios-glyphs/48/000000/github.png" width="40" alt="GitHub">
  </a>

</div>

