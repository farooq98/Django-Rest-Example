release: python manage.py migrate
web: daphne myproject.asgi:application --port $PORT --bind 0.0.0.0 -v2
myprojectworker: python manage.py runserver --settings=myproject.settings -v2