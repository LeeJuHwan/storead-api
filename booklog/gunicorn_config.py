# gunicorn_config.py

bind = "0.0.0.0:8000"
module = "config.wsgi:application"

workers = 4
worker_connections = 1000
threads = 4

certfile = "/etc/letsencrypt/live/api.storead.site/fullchain.pem"
keyfile = "/etc/letsencrypt/live/api.storead.site/privkey.pem"
