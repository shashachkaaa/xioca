#!/bin/bash

set -e

install_termux() {
    echo "✅ Обнаружена среда Termux. Запускаем установку..."
    pkg update -y && pkg upgrade -y
    pkg install proot-distro git -y

    proot-distro install ubuntu

    echo "Установка Ubuntu в proot-distro завершена."
    echo "Запускаем настройку внутри Ubuntu..."

    proot-distro login ubuntu -- bash -c '
        set -e
        apt update -y && apt upgrade -y
        apt install -y python3 python3-pip python3-venv git

        python3 -m venv /root/myenv
        source /root/myenv/bin/activate

        git clone https://github.com/shashachkaaa/xioca.git /root/xioca
        cd /root/xioca
        pip install -r requirements.txt

        echo "✅ Установка Xioca в Termux завершена."
        echo "Запускаем приложение..."
        python3 -m xioca
    '
}

install_linux() {
    echo "✅ Обнаружена стандартная среда Linux (Debian/Ubuntu). Запускаем установку..."

    echo "[1/3] Устанавливаем зависимости..."
    sudo apt-get update
    sudo apt-get install -y git python3 python3-pip tmux

    echo "[2/3] Клонируем репозиторий..."
    INSTALL_DIR="$HOME/xioca"
    if [ -d "$INSTALL_DIR" ]; then
        echo "Обнаружена существующая директория. Удаляем для чистой установки..."
        rm -rf "$INSTALL_DIR"
    fi
    git clone https://github.com/shashachkaaa/xioca.git "$INSTALL_DIR"

    echo "[3/3] Устанавливаем зависимости Python и запускаем Xioca..."
    cd "$INSTALL_DIR"
    pip install --upgrade pip
    pip install -r requirements.txt

    if tmux has-session -t xioca 2>/dev/null; then
        echo "Найден существующий сеанс tmux 'xioca'. Завершаем его..."
        tmux kill-session -t xioca
    fi

    echo "✅ Установка завершена. Сейчас вы будете подключены к сеансу tmux."
    echo "Чтобы отсоединиться (оставить работать в фоне), нажмите Ctrl+b, затем d."
    echo "Чтобы вернуться, используйте: tmux attach -t xioca"
    sleep 3

    tmux new-session -s xioca "python3 -m xioca 2>&1 | tee xioca.log"
}

install_serv00() {
    echo "✅ Обнаружена среда Serv00. Запускаем установку..."

    if tmux has-session -t xioca 2>/dev/null; then
        echo "Найден существующий сеанс tmux 'xioca'. Завершаем его..."
        tmux kill-session -t xioca
    fi
    
    if [ ! -d "xioca" ]; then
        echo "Клонируем репозиторий xioca..."
        git clone https://github.com/shashachkaaa/xioca.git
    else
        echo "Директория xioca уже существует."
    fi

    echo "Создаем сессию tmux и запускаем установку зависимостей и запуск..."
    tmux new-session -d -s xioca "cd xioca && pip install -r req* && python3 -m xioca"

    echo "✅ Установка завершена. Подключаемся к сеансу tmux..."
    sleep 2
    tmux attach-session -t xioca
}

echo "Запуск установщика Xioca..."

if [[ "$PREFIX" == *com.termux* ]]; then
    install_termux
elif hostname | grep -q 'serv00'; then
    install_serv00
elif command -v apt-get &> /dev/null; then
    install_linux
else
    echo "❌ Ошибка: Не удалось определить тип вашей системы (Termux, Serv00, Debian/Ubuntu)."
    echo "Установка прервана."
    exit 1
fi