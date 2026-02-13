# Handmade Marketplace MVP

MVP маркетплейса изделий ручной работы на `Vue 3 + FastAPI + MySQL`.

## Стек
- Frontend: Vue 3, Vite, TypeScript, Vue Router, Pinia, Tailwind
- Backend: FastAPI, SQLAlchemy 2.x (sync), Alembic
- DB: MySQL 8
- Dev/Prod: Docker Compose, Nginx, certbot (Let's Encrypt)

## Структура
- `backend/` API, модели, миграции, тесты
- `frontend/` SPA (buyer/seller/admin кабинеты)
- `infra/nginx/` конфиги reverse proxy
- `scripts/` seed и вспомогательные скрипты

## Локальный запуск (dev)
1. Создайте `.env` из `.env.example`:
   - `cp .env.example .env`
2. Запустите сервисы:
   - `make up`
3. Примените миграции:
   - `make migrate`
4. Заполните демо-данными:
   - `make seed`

Доступы:
- Frontend: `http://localhost:5173`
- Backend docs: `http://localhost:8000/docs`
- Adminer (tools profile): `make tools-up`, затем `http://localhost:8080`

## Миграции Alembic
- Применить: `make migrate`
- Вручную внутри backend:
  - `alembic upgrade head`

## Тестовые аккаунты (seed)
- `admin@example.com` / `Admin12345`
- `seller@example.com` / `Seller12345`
- `buyer@example.com` / `Buyer12345`

## Проверки качества
- Lint: `make lint`
- Tests: `make test`
- Frontend build: `docker compose exec frontend npm run build`

## Прод деплой на VM
### 1) Подготовка VM
- Установить Docker + Docker Compose plugin
- Открыть порты `80`, `443`

### 2) DNS в reg.ru
- Добавить `A` запись `@` -> IP VM
- Добавить `A` запись `www` -> IP VM

### 3) Конфиг окружения
- Скопировать `.env.example` -> `.env`
- Обязательно выставить:
  - `DOMAIN=your-domain.tld`
  - `EMAIL=your-email@domain.tld`
  - безопасный `SECRET_KEY`
  - production `DATABASE_URL`

### 4) Первый выпуск сертификата
1. Запустить prod стек:
   - `docker compose -f docker-compose.prod.yml up -d --build`
2. Выпустить сертификат:
   - ```bash
     docker compose -f docker-compose.prod.yml run --rm certbot certonly \
       --webroot -w /var/www/certbot \
       -d your-domain.tld -d www.your-domain.tld \
       --email your-email@domain.tld --agree-tos --no-eff-email
     ```
3. Перезапустить nginx:
   - `docker compose -f docker-compose.prod.yml restart nginx`

## Бэкапы
- MySQL dump:
  - `docker compose exec db mysqldump -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE > backup.sql`
- Media volume backup:
  - `docker run --rm -v diplom_site_media_data:/data -v %cd%:/backup alpine tar czf /backup/media-backup.tgz -C /data .`

## Основные API
- Auth: `/api/v1/auth/*`
- Catalog: `/api/v1/catalog`
- Cart: `/api/v1/cart`
- Checkout: `/api/v1/orders/checkout`
- Notifications: `/api/v1/notifications`
- Docs: `/docs`
