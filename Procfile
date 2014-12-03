web: gunicorn manage:flask_app --log-file=- --workers 1 --timeout 20
init: python manage.py createall