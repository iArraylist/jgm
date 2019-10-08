#!/bin/bash

echo 'Rom.Job'
python manage.py loaddata jgm/json/rom-job.json

echo 'Sites.Site'
python manage.py loaddata jgm/json/sites-site.json