#!/usr/bin/env bash
set -o errexit
cd my_brixproject
pip install -r requirements.txt
python manage.py collectstatic --no-input  
python manage.py create_deploy_superuser || true
python manage.py migrate
exec gunicorn my_brixproject.wsgi --bind 0.0.0.0: