#!/bin/bash

# tmux 세션 생성
tmux new-session -d -s streaming

# npm 글로벌 설정
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo "export PATH=~/.npm-global/bin:\$PATH" >> ~/.bashrc
source ~/.bashrc

# PM2 프로세스 시작
pm2 start test-streaming-bgi.js --name streaming-bgi
pm2 start test-streaming-hms.js --name streaming-hms
pm2 start test-streaming-yuki.js --name streaming-yuki
pm2 start test-streaming-capital.js --name streaming-capital

# PM2 설정 저장 및 startup 설정
pm2 save
pm2 startup

# 크론잡 설정
pm2 restart streaming-bgi --cron "0 * * * *"
pm2 restart streaming-hms --cron "0 * * * *"
pm2 restart streaming-yuki --cron "0 * * * *"
pm2 restart streaming-capital --cron "0 * * * *"
# tmux 세션에 접속
tmux attach -t streaming