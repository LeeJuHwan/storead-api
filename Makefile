ENV ?= prd

restart:
	docker compose -f docker-compose.$(ENV).yml restart

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

createadmin:
	docker compose -f docker-compose.$(ENV).yml run --rm api python booklog/manage.py createadmin

makemigrations:
	docker compose -f docker-compose.$(ENV).yml run --rm api python booklog/manage.py makemigrations

migrate:
	docker compose -f docker-compose.$(ENV).yml run --rm api python booklog/manage.py migrate

dbshell:
	docker compose -f docker-compose.$(ENV).yml run --rm api python booklog/manage.py dbshell

es-rebuild:
	docker compose -f docker-compose.$(ENV).yml run --rm api python booklog/manage.py search_index --rebuild
