# Handmade Marketplace MVP

MVP ������������ ������� ������ ������ �� `Vue 3 + FastAPI + MySQL`.

## ����
- Frontend: Vue 3, Vite, TypeScript, Vue Router, Pinia, Tailwind
- Backend: FastAPI, SQLAlchemy 2.x (sync), Alembic
- DB: MySQL 8
- Dev/Prod: Docker Compose, Nginx, certbot (Let's Encrypt)

## ���������
- `backend/` API, ������, ��������, �����
- `frontend/` SPA (buyer/seller/admin ��������)
- `infra/nginx/` ������� reverse proxy
- `scripts/` seed � ��������������� �������

## ��������� ������ (dev)
1. �������� `.env` �� `.env.example`:
   - `cp .env.example .env`
2. ��������� �������:
   - `make up`
3. ��������� ��������:
   - `make migrate`
4. ��������� ����-�������:
   - `make seed`

�������:
- Frontend: `http://localhost:5173`
- Backend docs: `http://localhost:8000/docs`
- Adminer (tools profile): `make tools-up`, ����� `http://localhost:8080`

## �������� Alembic
- ���������: `make migrate`
- ������� ������ backend:
  - `alembic upgrade head`

## �������� �������� (seed)
- `admin@example.com` / `Admin12345`
- `seller@example.com` / `Seller12345`
- `buyer@example.com` / `Buyer12345`

## �������� ��������
- Lint: `make lint`
- Tests: `make test`
- Frontend build: `docker compose exec frontend npm run build`

## ���� ������ �� VM
### 1) ���������� VM
- ���������� Docker + Docker Compose plugin
- ������� ����� `80`, `443`

### 2) DNS � reg.ru
- �������� `A` ������ `@` -> IP VM
- �������� `A` ������ `www` -> IP VM

### 3) ������ ���������
- ����������� `.env.example` -> `.env`
- ����������� ���������:
  - `DOMAIN=your-domain.tld`
  - `EMAIL=your-email@domain.tld`
  - ���������� `SECRET_KEY`
  - production `DATABASE_URL`

### 4) ������ ������ �����������
1. ��������� prod ����:
   - `docker compose -f docker-compose.prod.yml up -d --build`
2. ��������� ����������:
   - ```bash
     docker compose -f docker-compose.prod.yml run --rm certbot certonly \
       --webroot -w /var/www/certbot \
       -d your-domain.tld -d www.your-domain.tld \
       --email your-email@domain.tld --agree-tos --no-eff-email
     ```
3. ������������� nginx:
   - `docker compose -f docker-compose.prod.yml restart nginx`

## ������
- MySQL dump:
  - `docker compose exec db mysqldump -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE > backup.sql`
- Media volume backup:
  - `docker run --rm -v diplom_site_media_data:/data -v %cd%:/backup alpine tar czf /backup/media-backup.tgz -C /data .`

## �������� API
- Auth: `/api/v1/auth/*`
- Catalog: `/api/v1/catalog`
- Cart: `/api/v1/cart`
- Checkout: `/api/v1/orders/checkout`
- Notifications: `/api/v1/notifications`
- Docs: `/docs`
