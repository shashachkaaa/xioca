#!/bin/sh

tmux new-session -d -s xioca

tmux send-keys -t xioca 'git clone https://github.com/shashachkaaa/xioca.git && cd xioca && pip install -r req* && python3 -m xioca' C-m

tmux attach-session -t xioca