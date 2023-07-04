#!/bin/sh


sudo docker-compose -f docker-compose.yml up -d --build
sudo docker-compose -f docker-compose.yml exec web python manage.py makemigrations
sudo docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
sudo docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
# sudo docker-compose -f docker-compose.yml exec web python manage.py createsuperuser
