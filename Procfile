web: gunicorn manage:flask_app --log-file=- --worker-class gevent -w 3 --preload
init: python manage.py createall
migrate: python manage.py db migrate
update_softwares: python manage.py update_softwares_rates