# Аудит референса `reference/knitwear-shop1`

## 1) Страницы референса
- `index.html` — главная (hero, популярное, превью бренда, sale, отзывы)
- `catalog.html` — каталог (фильтры + сетка карточек)
- `product.html` — карточка товара (галерея, бейджи, CTA, табы, похожие)
- `cart.html` — корзина + форма оформления
- `favorites.html` — избранное
- `account.html` — вход/регистрация + личный кабинет
- `about.html` — о бренде
- `customers.html` — информация покупателям (доставка/возврат/оплата/уход)

## 2) Дизайн-токены (из `css/style.css`)

### Цвета
- `--primary-color: #C67797`
- `--primary-dark: #350D36`
- `--primary-light: #F5E6F0`
- `--accent-color: #946FAC`
- `--text-dark: #2D2D2D`
- `--text-light: #5D5D5D`
- `--background: #FAF5F8`
- `--white: #FFFFFF`

### Эффекты
- `--shadow: 0 8px 30px rgba(53, 13, 54, 0.08)`
- `--transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)`

### Шрифты
- `Cormorant Garamond` (основной)
- `Playfair Display` (резерв serif)
- `Dancing Script` (декоративный акцент)

### Размеры/геометрия (ключевые)
- контейнер: `max-width: 1200px`, `width: 90%`
- radius кнопок: `50px`
- radius карточек: `12px/15px/20px` (в зависимости от блока)
- sticky/fixed header: `position: fixed`, `backdrop-filter: blur(10px)`

### Breakpoints (`responsive.css`)
- `@media (max-width: 992px)`
- `@media (max-width: 768px)`
- `@media (max-width: 576px)`

## 3) Ключевые UI-паттерны референса
- Fixed header с полупрозрачным фоном и blur.
- Навигация с underline-анимацией у active/hover ссылок.
- Иконка корзины с бейджем количества.
- Мобильное меню (burger -> раскрывающаяся вертикальная навигация).
- Hero с фото-фоном + градиентным оверлеем + паттерном (`data:image/svg+xml`).
- CTA-кнопки с градиентом и shine-эффектом через псевдоэлемент `:before`.
- Карточки товара: тень, hover-lift, бейджи, favorite/cart actions.
- Формы: скруглённые поля, мягкий border/focus glow.
- Табы на странице товара.
- Визуальная тема: knitwear/уют/пастельная палитра.

## 4) Карта маппинга в наш Vue SPA
- `/` <- `index.html`
- `/catalog` <- `catalog.html`
- `/product/:id` <- `product.html`
- `/cart` <- `cart.html`
- `/favorites` <- `favorites.html`
- `/me` (+ alias `/account`) <- `account.html`
- `/about` <- `about.html`
- `/customers` (+ alias `/reviews`) <- `customers.html`

## 5) Замечания по интеграции
- Legacy JS (`js/*`) не переносится; поведение реализуется через Vue/Pinia/Router.
- Визуальные значения берутся из референса, но будут вынесены в поддерживаемые токены (`brand.css` + Tailwind theme).
- Тематика фиксируется как knitwear: контент, тексты и CTA в стиле бренда `Craft With Love`.
