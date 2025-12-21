#!/bin/bash

pkg update -y && pkg upgrade -y
pkg install proot-distro git -y

proot-distro install ubuntu

proot-distro login ubuntu -- bash -c '
    apt update -y && apt upgrade -y
    apt install python3 python3-pip python3-venv -y

    python3 -m venv /root/myenv
    source /root/myenv/bin/activate

    git clone https://github.com/shashachkaaa/xioca.git /root/xioca
    cd /root/xioca
    pip install -r requirements.txt

    python3 -m xioca
'