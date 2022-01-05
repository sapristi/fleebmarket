#! /bin/bash

set -x

yarn build


ssh truth "rm -r /fleebmarket/fleebmarket_django/fleebmarket_django/static/search_app"
rsync -rav -e ssh --exclude *.map build/static/* truth.local:/fleebmarket/fleebmarket_django/fleebmarket_django/static/search_app
ssh truth "vf activate fleebmarket_django; cd /fleebmarket/fleebmarket_django/fleebmarket_django; python manage.py collectstatic"
