#! /usr/bin/env fish

workon fleebmarket_django

set workdir (dirname (status --current-filename))
cd $workdir/../fleebmarket_django
python manage.py runserver 0.0.0.0:8080
