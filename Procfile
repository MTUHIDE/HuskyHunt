release: python3 mainsite/manage.py makemigrations && python3 mainsite/manage.py migrate
web: gunicorn --chdir mainsite mainsite.wsgi
