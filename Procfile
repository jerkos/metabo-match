web: newrelic-admin run-program gunicorn manage:flask_app --log-file=- -k gevent -w 4 --worker_connections 2000 --timeout 20
init: python manage.py createall