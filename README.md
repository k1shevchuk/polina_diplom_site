# Craft With Love MVP

MVP маркетплейса вязаных изделий ручной работы (`Vue 3 + FastAPI + MySQL`).
Бренд: **Craft With Love**. Тон: «Связано с любовью».

## Стек
- Frontend: Vue 3, Vite, TypeScript, Vue Router, Pinia, Tailwind
- Backend: FastAPI, SQLAlchemy 2.x (sync), Alembic
- DB: MySQL 8
- Dev/Prod: Docker Compose, Nginx, certbot (Let's Encrypt)

## Структура репозитория
- `backend/` — API, модели, сервисы, миграции, pytest
- `frontend/` — SPA (public/buyer/seller/admin)
- `infra/nginx/` — конфиги reverse proxy
- `scripts/` — сидинг и утилиты
- `docs/reference-audit.md` — аудит референса knitwear

## Локальный запуск (Windows + Docker Desktop)
1. Создать `.env` из шаблона:
   - PowerShell: `Copy-Item .env.example .env`
2. Поднять сервисы:
   - `make up`
3. Применить миграции:
   - `make migrate`
4. Выполнить сидинг демо-данных:
   - `make seed`

### URL
- Frontend: `http://localhost:5173`
- Backend docs (OpenAPI): `http://localhost:8000/docs`
- Adminer: `make tools-up` -> `http://localhost:8080`

## Демо-аккаунты
- `admin@example.com` / `Admin12345`
- `seller@example.com` / `Seller12345`
- `buyer@example.com` / `Buyer12345`

Если не получается авторизоваться (401/invalid credentials), обычно причина в том, что сидинг не запускался для текущего volume БД.
Проверьте по шагам:
1. `make migrate`
2. `make seed`
3. Повторите вход

Если выполнялся `make clean`, данные БД удаляются, сидинг нужно выполнить заново.

## Миграции
- Основной путь: `make migrate`
- Вручную:
  - `docker compose run --rm migrate`
  - или внутри backend: `alembic upgrade head`

## Почему backend не уходит в restart loop
`backend` запускает только `uvicorn`.
Миграции вынесены отдельно (`make migrate` / service `migrate`), поэтому падение миграции не перезапускает API по кругу.

## Проверки качества
- Backend lint: `docker compose exec backend ruff check app tests`
- Backend tests: `docker compose run --rm backend pytest -q`
- Frontend lint: `docker compose run --rm --no-deps frontend npm run lint`
- Frontend tests: `docker compose run --rm --no-deps frontend npm run test`
- Frontend build: `docker compose run --rm --no-deps frontend npm run build`

## Production deploy (VM)
1. Установить Docker Engine + Docker Compose plugin.
2. Открыть порты `80` и `443`.
3. DNS в reg.ru:
   - `A @ -> <VM_IP>`
   - `A www -> <VM_IP>`
4. Заполнить `.env` (минимум: `DOMAIN`, `EMAIL`, `SECRET_KEY`, `DATABASE_URL`).
5. Запустить прод-стек:
   - `docker compose -f docker-compose.prod.yml up -d --build`
6. Выпустить сертификат:
   - `docker compose -f docker-compose.prod.yml run --rm certbot certonly --webroot -w /var/www/certbot -d your-domain.tld -d www.your-domain.tld --email your-email@domain.tld --agree-tos --no-eff-email`
7. Перезапустить Nginx:
   - `docker compose -f docker-compose.prod.yml restart nginx`

## Резервные копии
- MySQL dump:
  - `docker compose exec db mysqldump -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE > backup.sql`
- Media volume:
  - `docker run --rm -v diplom_site_media_data:/data -v ${PWD}:/backup alpine tar czf /backup/media-backup.tgz -C /data .`
