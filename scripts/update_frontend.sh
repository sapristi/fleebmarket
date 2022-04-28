#! /usr/bin/sh


cd frontend
pnpm build
cd ../backend
. .venv/bin/activate
cd fleebmarket_django
python manage.py collectstatic

