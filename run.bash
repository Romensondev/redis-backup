#!/bin/bash
set -ex
DATA=$(date +%d%m%y%H%M%S)
TIPO=".rdb"
ARQUIVO="${REDIS_NAME}-$DATA.rdb"
redis-cli -h $REDIS_HOST --rdb $ARQUIVO
python3 send-s3.py "$ARQUIVO"