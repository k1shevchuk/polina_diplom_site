# Handmade Marketplace MVP

MVP маркетплейса изделий ручной работы на стеке `Vue 3 + FastAPI + MySQL`.

## Stack
- Frontend: Vue 3, Vite, TypeScript, Vue Router, Pinia, Tailwind
- Backend: FastAPI, SQLAlchemy 2.x (sync), Alembic
- DB: MySQL 8
- Dev/Prod: Docker Compose, Nginx, certbot (Let's Encrypt)

## Repository layout
- `backend/` API, модели, сервисы, миграции, тесты
- `frontend/` SPA (public/buyer/seller/admin)
- `infra/nginx/` конфиги reverse proxy
- `scripts/` seed и вспомогательные скрипты

## Local run (Windows + Docker Desktop)
1. Создать `.env` из шаблона:
   - PowerShell: `Copy-Item .env.example .env`
2. Поднять сервисы:
   - `make up`
3. Применить миграции (отдельно от старта backend):
   - `make migrate`
4. Заполнить демо-данными:
   - `make seed`

### URLs
- Frontend: `http://localhost:5173`
- Backend docs (OpenAPI): `http://localhost:8000/docs`
- Adminer: `make tools-up`, затем `http://localhost:8080`

## Why backend no longer restarts
`backend` теперь запускает только `uvicorn`.  
Миграции выполняются отдельной командой `make migrate`, поэтому падение миграций не уводит сервис в restart loop.

## Migrations
- `make migrate`
- вручную:
  - `docker compose run --rm migrate`
  - или внутри backend: `alembic upgrade head`

## Test accounts (seed)
- `admin@example.com` / `Admin12345`
- `seller@example.com` / `Seller12345`
- `buyer@example.com` / `Buyer12345`

## Quality checks
- Backend lint: `docker compose exec backend ruff check app tests`
- Backend tests: `docker compose exec backend pytest`
- Frontend lint/test/build:
  - `docker compose run --rm --no-deps frontend sh -c "npm install && npm run lint && npm run test && npm run build"`

## Production deploy (VM)
1. Install Docker + Docker Compose plugin.
2. Open ports `80` and `443`.
3. DNS in reg.ru:
   - `A @ -> <VM_IP>`
   - `A www -> <VM_IP>`
4. Fill `.env` (`DOMAIN`, `EMAIL`, secure `SECRET_KEY`, production `DATABASE_URL`).
5. Start stack:
   - `docker compose -f docker-compose.prod.yml up -d --build`
6. Issue certificate:
   - `docker compose -f docker-compose.prod.yml run --rm certbot certonly --webroot -w /var/www/certbot -d your-domain.tld -d www.your-domain.tld --email your-email@domain.tld --agree-tos --no-eff-email`
7. Restart Nginx:
   - `docker compose -f docker-compose.prod.yml restart nginx`

## Backups
- MySQL dump:
  - `docker compose exec db mysqldump -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE > backup.sql`
- Media volume:
  - `docker run --rm -v diplom_site_media_data:/data -v ${PWD}:/backup alpine tar czf /backup/media-backup.tgz -C /data .`

