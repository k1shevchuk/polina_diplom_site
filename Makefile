SHELL := /bin/sh

.PHONY: up down logs ps tools-up migrate seed test lint e2e verify smoke clean

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

tools-up:
	docker compose up -d adminer

migrate:
	docker compose run --rm migrate

seed:
	docker compose exec backend sh -lc "PYTHONPATH=/app python /scripts/seed.py"

test:
	docker compose run --rm backend pytest -q
	docker compose run --rm --no-deps frontend npm run test

lint:
	docker compose run --rm backend ruff check app tests
	docker compose run --rm --no-deps frontend npm run lint

e2e:
	docker compose up -d db backend frontend
	@i=0; until curl -fsS http://localhost:5173/ >/dev/null 2>&1; do i=$$((i+1)); if [ $$i -ge 30 ]; then echo "frontend is unavailable"; exit 1; fi; sleep 2; done
	@i=0; until curl -fsS http://localhost:8000/docs >/dev/null 2>&1; do i=$$((i+1)); if [ $$i -ge 30 ]; then echo "backend docs are unavailable"; exit 1; fi; sleep 2; done
	docker compose --profile tools run --rm e2e

verify:
	docker compose config > /dev/null
	docker compose -f docker-compose.prod.yml config > /dev/null
	docker compose run --rm backend ruff check app tests
	docker compose run --rm backend pytest -q
	docker compose run --rm --no-deps frontend npm run lint
	docker compose run --rm --no-deps frontend npm run test
	docker compose run --rm --no-deps frontend npm run build
	$(MAKE) e2e

smoke:
	docker compose up -d --build
	@i=0; until curl -fsS http://localhost:5173/ >/dev/null 2>&1; do i=$$((i+1)); if [ $$i -ge 30 ]; then echo "frontend is unavailable"; exit 1; fi; sleep 2; done
	@i=0; until curl -fsS http://localhost:8000/docs >/dev/null 2>&1; do i=$$((i+1)); if [ $$i -ge 30 ]; then echo "backend docs are unavailable"; exit 1; fi; sleep 2; done
	@echo "smoke checks passed"

clean:
	docker compose down -v --remove-orphans
