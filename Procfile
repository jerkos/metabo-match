web: newrelic-admin run-program gunicorn manage:flask_app --log-file=- --workers 2 --worker-class gevent --timeout 20
init: python manage.py createall