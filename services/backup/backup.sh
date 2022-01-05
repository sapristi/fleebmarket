#! /bin/bash
# This script is supposed to be run after loading fleebmarket env vars

timestamp=$(date "+%F_%H-%M")
target_file=$DATA_PATH/backups/fleebmarket_$timestamp.bak

mkdir -p $DATA_PATH/backups
pg_dump --user fleebmarket fleebmarket > $target_file

scp $target_file pi@charm.local:/home/data/backups/
