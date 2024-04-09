ENV ?= dev

build:
	docker compose -f docker-compose.$(ENV).yml up --build -d --remove-orphans

up:
	docker compose -f docker-compose.$(ENV).yml up

down:
	docker compose -f docker-compose.$(ENV).yml down

down-v:
	docker compose -f docker-compose.$(ENV).yml down -v

logs:
	docker compose -f docker-compose.$(ENV).yml logs

logs-api:
	docker compose -f docker-compose.$(ENV).yml logs api

superuser:
	docker compose -f docker-compose.$(ENV).yml run --rm api python manage.py createsuperuser

