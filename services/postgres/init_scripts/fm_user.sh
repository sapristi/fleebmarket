#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER fleebmarket with PASSWORD '$FLEEBMARKET_POSTGRES_PASSWORD';
    CREATE DATABASE fleebmarket;
    GRANT ALL PRIVILEGES ON DATABASE fleebmarket TO fleebmarket;
EOSQL
