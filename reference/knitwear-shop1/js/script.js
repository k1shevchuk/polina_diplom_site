// Основной скрипт сайта
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация мобильного меню
    initMobileMenu();
    
    // Инициализация главной страницы
    if (document.querySelector('.hero')) {
        initHomePage();
    }
    
    // Инициализация каталога
    if (document.querySelector('.catalog-grid')) {
        initCatalog();
    }
    
    // Инициализация корзины
    if (document.querySelector('.cart-items')) {
        initCart();
    }
    
    // Инициализация личного кабинета
    if (document.querySelector('.auth-form')) {
        initAccount();
    }
    
    // Инициализация избранного
    if (document.querySelector('#favorites-list')) {
        initFavorites();
    }
    
    // Обновление счетчика корзины
    updateCartCount();
});

// Мобильное меню
function initMobileMenu() {
    const toggle = document.querySelector('.mobile-menu-toggle');
    const nav = document.querySelector('.nav');
    
    if (toggle && nav) {
        toggle.addEventListener('click', function() {
            this.classList.toggle('active');
            nav.classList.toggle('active');
        });
    }
}

// Главная страница
function initHomePage() {
    // Заполнение слайдера популярных товаров
    const popularSlider = document.querySelector('#popular-slider');
    if (popularSlider) {
        const popularProducts = db.getPopularProducts().slice(0, 8);
        createSliderWithProducts(popularSlider, popularProducts, 'popular');
    }
    
    // Заполнение слайдера товаров по акции
    const saleSlider = document.querySelector('#sale-slider');
    if (saleSlider) {
        const saleProducts = db.getSaleProducts().slice(0, 8);
        createSliderWithProducts(saleSlider, saleProducts, 'sale');
    }
    
    // Заполнение отзывов
    const reviewsList = document.getElementById('reviews-list');
    if (reviewsList) {
        db.reviews.forEach(review => {
            reviewsList.appendChild(createReviewItem(review));
        });
    }
    
    // Обработка формы отзыва
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const rating = parseInt(this.querySelector('input[name="rating"]:checked')?.value);
            const text = this.querySelector('textarea[name="review-text"]').value;
            
            if (!rating) {
                alert('Пожалуйста, выберите оценку');
                return;
            }
            
            if (!text.trim()) {
                alert('Пожалуйста, напишите отзыв');
                return;
            }
            
            const result = db.addReview(rating, text);
            
            if (result.success) {
                reviewsList.appendChild(createReviewItem(result.review));
                this.reset();
                alert('Спасибо за ваш отзыв!');
            }
        });
    }
}

// Создание слайдера с товарами
function createSliderWithProducts(sliderElement, products, sliderId) {
    if (!sliderElement || products.length === 0) return;
    
    // Очищаем слайдер
    sliderElement.innerHTML = '';
    
    // Создаем карточки товаров
    products.forEach((product, index) => {
        const card = createProductCard(product);
        card.dataset.index = index;
        sliderElement.appendChild(card);
    });
    
    // Добавляем стрелочки если их еще нет
    const sliderContainer = sliderElement.closest('.slider-container');
    if (sliderContainer && !sliderContainer.querySelector('.slider-arrow')) {
        addSliderArrows(sliderContainer, sliderId);
    }
    
    // Инициализируем функциональность слайдера
    initSliderFunctionality(sliderElement, sliderId);
}

// Добавление стрелочек к слайдеру
function addSliderArrows(sliderContainer, sliderId) {
    const prevArrow = document.createElement('button');
    prevArrow.className = `slider-arrow prev ${sliderId}-prev`;
    prevArrow.innerHTML = '‹';
    prevArrow.setAttribute('aria-label', 'Предыдущий слайд');
    
    const nextArrow = document.createElement('button');
    nextArrow.className = `slider-arrow next ${sliderId}-next`;
    nextArrow.innerHTML = '›';
    nextArrow.setAttribute('aria-label', 'Следующий слайд');
    
    sliderContainer.appendChild(prevArrow);
    sliderContainer.appendChild(nextArrow);
}

// Инициализация функциональности слайдера
function initSliderFunctionality(slider, sliderId) {
    const sliderContainer = slider.closest('.slider-container');
    if (!sliderContainer) return;
    
    const prevArrow = sliderContainer.querySelector(`.${sliderId}-prev`);
    const nextArrow = sliderContainer.querySelector(`.${sliderId}-next`);
    const cards = slider.querySelectorAll('.product-card');
    
    if (cards.length === 0) return;
    
    let currentPosition = 0;
    let isAnimating = false;
    let autoSlideInterval;
    const cardWidth = cards[0].offsetWidth + 25; // Ширина карточки + gap
    
    // Функция для плавной прокрутки
    function smoothScroll(position) {
        if (isAnimating) return;
        
        isAnimating = true;
        slider.style.scrollBehavior = 'smooth';
        slider.scrollLeft = position;
        
        setTimeout(() => {
            isAnimating = false;
            checkInfiniteScroll();
        }, 300);
    }
    
    // Функция для мгновенной прокрутки (без анимации)
    function instantScroll(position) {
        slider.style.scrollBehavior = 'auto';
        slider.scrollLeft = position;
        setTimeout(() => {
            slider.style.scrollBehavior = 'smooth';
        }, 50);
    }
    
    // Функция проверки бесконечной прокрутки
    function checkInfiniteScroll() {
        const scrollLeft = slider.scrollLeft;
        const scrollWidth = slider.scrollWidth;
        const clientWidth = slider.clientWidth;
        const maxScroll = scrollWidth - clientWidth;
        
        // Если прокрутили к концу, переходим к началу
        if (scrollLeft >= maxScroll - 10) {
            setTimeout(() => {
                instantScroll(0);
                currentPosition = 0;
            }, 100);
        }
        // Если прокрутили к началу (для обратной прокрутки)
        else if (scrollLeft <= 10) {
            setTimeout(() => {
                instantScroll(maxScroll - cardWidth);
                currentPosition = cards.length - 1;
            }, 100);
        }
    }
    
    // Функция перехода к следующему слайду
    function nextSlide() {
        if (isAnimating) return;
        
        const scrollLeft = slider.scrollLeft;
        const newPosition = scrollLeft + cardWidth;
        
        // Если достигли конца, плавно переходим к началу
        if (newPosition >= slider.scrollWidth - slider.clientWidth - cardWidth) {
            // Сначала прокручиваем до конца
            smoothScroll(slider.scrollWidth - slider.clientWidth);
            // Затем мгновенно возвращаемся к началу
            setTimeout(() => {
                instantScroll(0);
                currentPosition = 0;
            }, 350);
        } else {
            currentPosition++;
            smoothScroll(newPosition);
        }
    }
    
    // Функция перехода к предыдущему слайду
    function prevSlide() {
        if (isAnimating) return;
        
        const scrollLeft = slider.scrollLeft;
        const newPosition = scrollLeft - cardWidth;
        
        // Если достигли начала, плавно переходим к концу
        if (newPosition <= 0) {
            // Сначала прокручиваем к началу
            smoothScroll(0);
            // Затем мгновенно переходим к концу
            setTimeout(() => {
                instantScroll(slider.scrollWidth - slider.clientWidth - cardWidth);
                currentPosition = cards.length - 1;
            }, 350);
        } else {
            currentPosition--;
            smoothScroll(newPosition);
        }
    }
    
    // Обработчики для стрелочек
    if (prevArrow) {
        prevArrow.addEventListener('click', prevSlide);
    }
    
    if (nextArrow) {
        nextArrow.addEventListener('click', nextSlide);
    }
    
    // Обработчик события прокрутки
    slider.addEventListener('scroll', checkInfiniteScroll);
    
    // Автопрокрутка
    function startAutoSlide() {
        stopAutoSlide();
        autoSlideInterval = setInterval(nextSlide, 4000);
    }
    
    function stopAutoSlide() {
        if (autoSlideInterval) {
            clearInterval(autoSlideInterval);
        }
    }
    
    // Запускаем автопрокрутку
    startAutoSlide();
    
    // Останавливаем автопрокрутку при наведении
    slider.addEventListener('mouseenter', stopAutoSlide);
    slider.addEventListener('mouseleave', startAutoSlide);
    
    // Останавливаем автопрокрутку при касании на мобильных
    slider.addEventListener('touchstart', stopAutoSlide);
    slider.addEventListener('touchend', startAutoSlide);
    
    // Пересчет позиции при изменении размера окна
    window.addEventListener('resize', function() {
        setTimeout(() => {
            const newCardWidth = cards[0].offsetWidth + 25;
            instantScroll(currentPosition * newCardWidth);
        }, 100);
    });
}

// Каталог
function initCatalog() {
    const catalogGrid = document.querySelector('.catalog-grid');
    const filterOptions = document.querySelectorAll('.filter-option');
    
    // Заполнение каталога товарами
    function displayProducts(products) {
        catalogGrid.innerHTML = '';
        products.forEach(product => {
            catalogGrid.appendChild(createProductCard(product, true));
        });
    }
    
    // Изначально показываем все товары
    displayProducts(db.products);
    
    // Обработка фильтров
    filterOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Убираем активный класс у всех опций
            filterOptions.forEach(opt => opt.classList.remove('active'));
            // Добавляем активный класс к выбранной опции
            this.classList.add('active');
            
            const category = this.dataset.category;
            const products = db.getProductsByCategory(category);
            displayProducts(products);
        });
    });
    
    // Обработка бегунка цены
    const priceRange = document.querySelector('.price-range');
    if (priceRange) {
        priceRange.addEventListener('input', function() {
            const maxPrice = parseInt(this.value);
            document.querySelector('.max-price').textContent = maxPrice;
            
            const filteredProducts = db.products.filter(product => product.price <= maxPrice);
            displayProducts(filteredProducts);
        });
    }
}

// Корзина
function initCart() {
    const cartItems = document.querySelector('.cart-items');
    const cartSummary = document.querySelector('.cart-summary');
    const checkoutForm = document.querySelector('.checkout-form');
    
    // Обновление корзины
    function updateCart() {
        const cart = db.getCart();
        const total = db.getCartTotal();
        
        // Обновляем список товаров
        cartItems.innerHTML = '';
        cart.forEach(item => {
            cartItems.appendChild(createCartItem(item));
        });
        
        // Обновляем итоговую сумму
        document.querySelector('.summary-total').textContent = `${total} руб.`;
        
        // Обновляем счетчик корзины
        updateCartCount();
        
        // Показываем/скрываем форму оформления заказа
        if (cart.length === 0) {
            checkoutForm.style.display = 'none';
            cartItems.innerHTML = '<p class="empty-cart">Ваша корзина пуста</p>';
        } else {
            checkoutForm.style.display = 'block';
        }
    }
    
    // Обработка оформления заказа
    const orderForm = document.getElementById('order-form');
    if (orderForm) {
        orderForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (!db.currentUser) {
                alert('Для оформления заказа необходимо авторизоваться');
                return;
            }
            
            const address = this.querySelector('#address').value;
            const paymentMethod = this.querySelector('input[name="payment"]:checked')?.value;
            
            if (!address) {
                alert('Пожалуйста, укажите адрес доставки');
                return;
            }
            
            if (!paymentMethod) {
                alert('Пожалуйста, выберите способ оплаты');
                return;
            }
            
            alert('Заказ успешно оформлен! Спасибо за покупку!');
            db.clearCart();
            updateCart();
            this.reset();
        });
    }
    
    // Инициализация корзины
    updateCart();
}

// Личный кабинет
function initAccount() {
    const authTabs = document.querySelectorAll('.auth-tab');
    const authContents = document.querySelectorAll('.auth-content');
    const userProfile = document.querySelector('.user-profile');
    
    // Переключение между вкладками авторизации/регистрации
    authTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const target = this.dataset.target;
            
            authTabs.forEach(t => t.classList.remove('active'));
            authContents.forEach(c => c.classList.remove('active'));
            
            this.classList.add('active');
            document.getElementById(target).classList.add('active');
        });
    });
    
    // Обработка формы регистрации
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = this.querySelector('#reg-name').value;
            const email = this.querySelector('#reg-email').value;
            const password = this.querySelector('#reg-password').value;
            const confirmPassword = this.querySelector('#reg-confirm-password').value;
            
            if (password !== confirmPassword) {
                alert('Пароли не совпадают');
                return;
            }
            
            const result = authManager.register(name, email, password);
            
            if (result.success) {
                alert('Регистрация прошла успешно!');
                window.location.href = 'account.html';
            } else {
                alert(result.message);
            }
        });
    }
    
    // Обработка формы авторизации
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = this.querySelector('#login-email').value;
            const password = this.querySelector('#login-password').value;
            
            const result = authManager.login(email, password);
            
            if (result.success) {
                alert('Авторизация прошла успешно!');
                window.location.href = 'account.html';
            } else {
                alert(result.message);
            }
        });
    }
    
    // Показ профиля пользователя, если он авторизован
    if (db.currentUser) {
        document.querySelector('.auth-form').style.display = 'none';
        userProfile.style.display = 'block';
        
        document.querySelector('.user-avatar').textContent = db.currentUser.name.charAt(0).toUpperCase();
        document.querySelector('.user-details h2').textContent = db.currentUser.name;
        document.querySelector('.user-details p').textContent = db.currentUser.email;
        
        // Обработка выхода
        const logoutBtn = document.querySelector('.logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', function() {
                authManager.logout();
                window.location.reload();
            });
        }
    } else {
        if (userProfile) userProfile.style.display = 'none';
    }
}

// Избранное
function initFavorites() {
    const favoritesList = document.getElementById('favorites-list');
    
    function updateFavorites() {
        const favorites = db.getFavorites();
        
        if (favorites.length === 0) {
            favoritesList.innerHTML = '<p class="empty-favorites">У вас пока нет избранных товаров</p>';
        } else {
            favoritesList.innerHTML = '';
            favorites.forEach(product => {
                favoritesList.appendChild(createProductCard(product, true));
            });
        }
    }
    
    // Проверяем, авторизован ли пользователь
    if (!db.currentUser) {
        favoritesList.innerHTML = '<p class="auth-required">Для просмотра избранных товаров необходимо <a href="account.html">авторизоваться</a></p>';
        return;
    }
    
    updateFavorites();
}

// Создание карточки товара
function createProductCard(product, showCategory = false) {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.dataset.id = product.id;
    
    const priceHtml = product.oldPrice ? 
        `<div class="product-price">
            <span class="old-price">${product.oldPrice} руб.</span>
            <span class="price">${product.price} руб.</span>
        </div>` : 
        `<div class="product-price">
            <span class="price">${product.price} руб.</span>
        </div>`;
    
    const categoryHtml = showCategory ? 
        `<div class="product-category">${getCategoryName(product.category)}</div>` : '';
    
    card.innerHTML = `
        <div class="product-image">
            <img src="${product.image}" alt="${product.name}" onerror="this.src='images/placeholder.jpg'">
        </div>
        <div class="product-info">
            ${categoryHtml}
            <h3 class="product-title">${product.name}</h3>
            <p class="product-description">${product.description}</p>
            ${priceHtml}
            <div class="product-actions">
                <button class="favorite-btn ${db.currentUser && db.currentUser.favorites && db.currentUser.favorites.includes(product.id) ? 'active' : ''}" 
                        onclick="toggleFavorite('${product.id}')">❤</button>
                <button class="cart-btn" onclick="addToCart('${product.id}')">🛒</button>
            </div>
        </div>
    `;
    
    // Добавляем обработчик клика для перехода на страницу товара
    card.addEventListener('click', function(e) {
        if (!e.target.closest('.product-actions')) {
            alert(`Переход на страницу товара: ${product.name}`);
        }
    });
    
    return card;
}

// Создание элемента корзины
function createCartItem(item) {
    const element = document.createElement('div');
    element.className = 'cart-item';
    
    element.innerHTML = `
        <div class="cart-item-image">
            <img src="${item.product.image}" alt="${item.product.name}" onerror="this.src='images/placeholder.jpg'">
        </div>
        <div class="cart-item-details">
            <h3 class="cart-item-title">${item.product.name}</h3>
            <div class="cart-item-price">${item.product.price} руб.</div>
            <div class="cart-item-quantity">
                <button class="quantity-btn" onclick="updateCartItem('${item.productId}', ${item.quantity - 1})">-</button>
                <input type="number" class="quantity-input" value="${item.quantity}" min="1" 
                       onchange="updateCartItem('${item.productId}', parseInt(this.value))">
                <button class="quantity-btn" onclick="updateCartItem('${item.productId}', ${item.quantity + 1})">+</button>
            </div>
        </div>
        <button class="remove-item" onclick="removeFromCart('${item.productId}')">×</button>
    `;
    
    return element;
}

// Создание элемента отзыва
function createReviewItem(review) {
    const element = document.createElement('div');
    element.className = 'review-item';
    
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        stars += i <= review.rating ? '★' : '☆';
    }
    
    element.innerHTML = `
        <div class="review-rating">${stars}</div>
        <p class="review-text">${review.text}</p>
        <div class="review-author">${review.author}, ${review.date}</div>
    `;
    
    return element;
}

// Получение названия категории
function getCategoryName(category) {
    const categories = {
        'sweaters': 'Свитеры',
        'cardigans': 'Кардиганы',
        'accessories': 'Аксессуары',
        'bags': 'Сумки',
        'skirts': 'Юбки',
        'dresses': 'Платья'
    };
    
    return categories[category] || category;
}

// Обновление счетчика корзины
function updateCartCount() {
    const cartCount = document.getElementById('cart-count');
    if (cartCount) {
        const count = db.cart.reduce((total, item) => total + item.quantity, 0);
        cartCount.textContent = count;
    }
}

// Функции для работы с избранным
function toggleFavorite(productId) {
    if (!db.currentUser) {
        alert('Для добавления в избранное необходимо авторизоваться');
        return;
    }
    
    const button = document.querySelector(`.favorite-btn[onclick="toggleFavorite('${productId}')"]`);
    
    if (db.currentUser.favorites && db.currentUser.favorites.includes(productId)) {
        db.removeFromFavorites(productId);
        if (button) button.classList.remove('active');
    } else {
        db.addToFavorites(productId);
        if (button) button.classList.add('active');
    }
}

// Функции для работы с корзиной
function addToCart(productId) {
    db.addToCart(productId);
    updateCartCount();
    alert('Товар добавлен в корзину!');
}

function updateCartItem(productId, quantity) {
    db.updateCartItem(productId, quantity);
    
    if (document.querySelector('.cart-items')) {
        initCart();
    } else {
        updateCartCount();
    }
}

function removeFromCart(productId) {
    db.removeFromCart(productId);
    
    if (document.querySelector('.cart-items')) {
        initCart();
    } else {
        updateCartCount();
    }
}