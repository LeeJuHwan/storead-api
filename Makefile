RUNFILE ?= docker-compose.dev.yml

restart:
	docker compose -f $(RUNFILE) restart

build:
	docker compose -f $(RUNFILE) up --build -d --remove-orphans

up:
	docker compose -f $(RUNFILE) up

down:
	docker compose -f $(RUNFILE) down

down-v:
	docker compose -f $(RUNFILE) down -v

logs:
	docker compose -f $(RUNFILE) logs

logs-api:
	docker compose -f $(RUNFILE) logs api

createadmin:
	docker compose -f $(RUNFILE) run --rm api python booklog/manage.py createadmin

makemigrations:
	docker compose -f $(RUNFILE) run --rm api python booklog/manage.py makemigrations

migrate:
	docker compose -f $(RUNFILE) run --rm api python booklog/manage.py migrate

dbshell:
	docker compose -f $(RUNFILE) run --rm api python booklog/manage.py dbshell

es-rebuild:
	docker compose -f $(RUNFILE) run --rm api python booklog/manage.py search_index --rebuild
