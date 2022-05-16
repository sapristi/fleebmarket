#! /bin/bash

set -a
source $INSTANCE_PATH/backend/.env
set +a

source $VENV_PATH/bin/activate
cd $INSTANCE_PATH/backend/fleebmarket_django
uvicorn fleebmarket.asgi:app --forwarded-allow-ips "*" --port ${UVICORN_PORT:-8000}
