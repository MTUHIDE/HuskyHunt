#!/usr/bin/env bash

# Migrate database
python3 mainsite/manage.py migrate
python3 mainsite/manage.py migrate django_cron

# Add cron jobs
python3 mainsite/manage.py crontab add

if [ "$DEBUG" = 'true' ]
then
  # Also install fixtures
  python3 mainsite/manage.py loaddata default
fi
