.PHONY: up down build logs

COMPOSE=docker compose -f docker-compose.migration.yml

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

logs:
	$(COMPOSE) logs -f