#!/bin/bash

set -e
set -x

if [ "$DEVELOPMENT" = "YES" ]; then
    python manage.py runserver --verbosity 0 0.0.0.0:8000
else
    pip install uwsgi
    pip install -r /unlimitree/requirements.txt
    python manage.py migrate
    python manage.py collectstatic --noinput --clear > /dev/null
    uwsgi --http :8000 --module unlimitemplate.wsgi
fi