#!/bin/sh

python manage.py flush --noinput
python manage.py migrate

# Create the superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('root', 'admin@example.com', 'root')" | python manage.py shell


exec "$@"
