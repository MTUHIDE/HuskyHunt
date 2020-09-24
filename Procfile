release: python3 mainsite/manage.py migrate && python3 mainsite/manage.py loaddata default
web: gunicorn --chdir mainsite mainsite.wsgi
