#! /bin/bash


source $INSTANCE_PATH/backend/.venv/bin/activate
cd $INSTANCE_PATH/backend
uvicorn fleebmarket.asgi:app --forwarded-allow-ips "*" --port ${UVICORN_PORT:-8000}
