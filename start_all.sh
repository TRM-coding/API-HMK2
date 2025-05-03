#!/bin/bash
# filepath: /root/api_hmk2/start_all.sh
# 启动 Redis (确保 redis-server 在系统 PATH 中)
redis-server &
# 启动 Celery worker
celery -A celery_worker worker --loglevel=info &
# 启动 Flask 应用
python run.py