# Craft With Love MVP

MVP маркетплейса вязаных изделий ручной работы на стеке `Vue 3 + FastAPI + MySQL`.
Бренд: **Craft With Love**. Тон: «Связано с любовью».

## Стек
- Frontend: Vue 3, Vite, TypeScript, Vue Router, Pinia, Tailwind
- Backend: FastAPI, SQLAlchemy 2.x (sync), Alembic
- DB: MySQL 8
- Dev/Prod: Docker Compose, Nginx, certbot (Let's Encrypt)

## Структура
- `backend/` — API, модели, сервисы, миграции, тесты
- `frontend/` — SPA (public/buyer/seller/admin)
- `infra/nginx/` — конфиги reverse proxy
- `scripts/` — сидинг и утилиты
- `reference/knitwear-shop1/` — дизайн-референс

## Локальный запуск (Windows + Docker Desktop)
1. Создать `.env` из шаблона:
   - `Copy-Item .env.example .env`
2. Поднять сервисы:
   - `docker compose up -d --build`
3. Применить миграции:
   - `docker compose run --rm migrate`
4. Выполнить сидинг демо-данных:
   - `docker compose exec backend sh -lc "PYTHONPATH=/app python /scripts/seed.py"`

## URL
- Frontend: `http://localhost:5173`
- Backend docs: `http://localhost:8000/docs`
- Adminer: `http://localhost:8080`

## Демо-аккаунты
Фиксированные:
- `admin@example.com` / `Admin12345`
- `seller@example.com` / `Seller12345`
- `buyer@example.com` / `Buyer12345`

Дополнительно после `seed` создаются:
- всего `100` пользователей
- около `12` продавцов (включая `seller@example.com`)
- дополнительные продавцы: `seller01@craftwithlove.ru ... seller11@craftwithlove.ru` (пароль `Seller12345`)
- дополнительные покупатели: `buyer001@craftwithlove.ru ...` (пароль `Buyer12345`)

Важно: текущий `seed` пересоздаёт доменные demo-данные (товары/заказы/сообщения/избранное) для консистентной среды.

## Что уже в demo-данных
- Категории knitwear: scarves, mittens, socks, cardigans, dresses, skirts, bags, sweaters
- Карточки товаров из референса (`/brand/products/*.jpg`), без старых placeholder `vase`
- Заказы, отзывы, переписки, уведомления, избранное, корзины

## Навигация по ролям
- После логина в верхнем меню появляются ролевые ссылки:
  - `Кабинет продавца` для `SELLER`
  - `Админка` для `ADMIN`
- Админ-панель: `http://localhost:5173/admin`

## Проверки качества
Команды `make` на Windows могут быть недоступны в PowerShell. Эквивалент `verify`:
- `docker compose config`
- `docker compose -f docker-compose.prod.yml config`
- `docker compose run --rm backend ruff check app tests`
- `docker compose run --rm backend pytest -q`
- `docker compose run --rm --no-deps frontend npm run lint`
- `docker compose run --rm --no-deps frontend npm run test`
- `docker compose run --rm --no-deps frontend npm run build`
- `docker compose up -d db backend frontend`
- `docker compose --profile tools run --rm e2e`

### E2E (Playwright в Docker)
- В `docker-compose.yml` добавлен сервис `e2e` на `mcr.microsoft.com/playwright`.
- Запуск:
  - `docker compose up -d db backend frontend`
  - `docker compose --profile tools run --rm e2e`
- `make verify` теперь включает e2e (после lint/test/build).

## CI/CD (GitHub Actions)
- `CI`: `.github/workflows/ci.yml`
  - запускается на `pull_request` и `push` в `dev`, `master`
  - проверки: compose config, backend (`ruff`, `pytest`), frontend (`lint`, `vitest`, `build`), e2e (Playwright в Docker)
- `Deploy Production`: `.github/workflows/deploy-production.yml`
  - запускается после успешного `CI` на push в `master`
  - также доступен ручной запуск `workflow_dispatch`
  - использует environment `production` (рекомендуется включить ручное подтверждение в GitHub)

Что нужно настроить в GitHub (один раз):
1. Создать environment: `production`.
2. Для `production` включить `Required reviewers` (ручной approve перед деплоем).
3. Добавить environment secrets:
   - `SSH_HOST` — IP/домен сервера
   - `SSH_PORT` — SSH порт (обычно `22`)
   - `SSH_USER` — пользователь (`ubuntu`)
   - `SSH_PRIVATE_KEY` — приватный ключ для SSH
   - `DEPLOY_PATH` — путь к проекту на сервере (`/home/ubuntu/diplom_site`)
4. Включить branch protection для `master`: merge только через PR и только при зелёном `CI`.

Базовый поток релизов:
1. Разработка в feature-ветке от `dev`.
2. Merge feature -> `dev` запускает `CI`.
3. После проверки merge `dev` -> `master`.
4. `CI` на `master` + approve environment `production` -> автодеплой в prod.

## Production deploy (VM)
1. Установить Docker + Compose plugin.
2. Открыть порты `80` и `443`.
3. Настроить DNS в reg.ru:
   - `A @ -> <VM_IP>`
   - `A www -> <VM_IP>`
4. Заполнить `.env` (`DOMAIN`, `EMAIL`, `SECRET_KEY`, `DATABASE_URL`).
5. Запустить стек:
   - `docker compose -f docker-compose.prod.yml up -d --build`
6. Выпустить сертификат:
   - `docker compose -f docker-compose.prod.yml run --rm certbot certonly --webroot -w /var/www/certbot -d your-domain.tld -d www.your-domain.tld --email your-email@domain.tld --agree-tos --no-eff-email`
7. Перезапустить Nginx:
   - `docker compose -f docker-compose.prod.yml restart nginx`

## Бэкапы
- MySQL dump:
  - `docker compose exec db mysqldump -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE > backup.sql`
- Media volume:
  - `docker run --rm -v diplom_site_media_data:/data -v ${PWD}:/backup alpine tar czf /backup/media-backup.tgz -C /data .`
