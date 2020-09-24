#!/usr/bin/env bash

# Migrate database
python3 mainsite/manage.py migrate
python3 mainsite/manage.py migrate django_cron

if [ "$DEBUG" = 'true' ]
then
  # Also install fixtures
  python3 mainsite/manage.py loaddata default
fi
