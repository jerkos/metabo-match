web: newrelic-admin run-program gunicorn manage:flask_app --log-file=- --worker-class gevent --workers 4 --worker-connections 2000 --timeout 20 --preload -D
init: python manage.py createall