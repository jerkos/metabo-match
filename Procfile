web: gunicorn manage:flask_app --log-file=- --worker-class gevent --timeout 20
init: python manage.py createall