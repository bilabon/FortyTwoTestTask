#!/bin/bash
# Execute infomodels command that prints all project models and
# the count of objects in every model
# Also:
# duplicate output to STDERR, prefixing each line with "error: "
# save output of stderr into file.

MANAGE=django-admin.py
SETTINGS=fortytwo_test_task.settings
DATE=$(date +%Y-%m-%d)

if [ ! -d logs ]; then mkdir -p logs; fi;
PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$SETTINGS $MANAGE infomodels 2> "logs/$DATE.dat"
