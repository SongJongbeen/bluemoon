#!/bin/bash

# conda 초기화 및 가상환경 활성화
source ~/miniconda3/etc/profile.d/conda.sh
conda activate bluemoon

# tmux 세션 생성
tmux new-session -d -s bluemoon

# PM2로 main.py 실행
cd /home/ec2-user/bluemoon
pm2 start main.py --name bluemoon-main --interpreter /home/ec2-user/miniconda3/envs/bluemoon/bin/python3

# PM2 설정 저장 및 startup 설정
pm2 save
pm2 startup

# 서비스 스케줄링 설정
# 매일 새벽 1시에 중지
pm2 stop bluemoon-main --cron "0 1 * * *"
# 매일 아침 8시에 시작
pm2 restart bluemoon-main --cron "0 8 * * *"

# tmux 세션에 접속
tmux attach -t bluemoon
