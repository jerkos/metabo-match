web: gunicorn manage:flask_app --log-file=- --workers 2 --timeout 20
init: python manage.py createall