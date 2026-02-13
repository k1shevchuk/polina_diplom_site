SHELL := /bin/sh

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

tools-up:
	docker compose --profile tools up -d adminer

migrate:
	docker compose run --rm migrate

seed:
	docker compose exec backend python /scripts/seed.py

test:
	docker compose exec backend pytest
	docker compose exec frontend npm run test

lint:
	docker compose exec backend ruff check app tests
	docker compose exec frontend npm run lint

clean:
	docker compose down -v --remove-orphans
