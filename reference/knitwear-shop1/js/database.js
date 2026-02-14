// Имитация базы данных
class Database {
    constructor() {
        this.products = this.loadFromStorage('products') || this.initializeProducts();
        this.users = this.loadFromStorage('users') || [];
        this.reviews = this.loadFromStorage('reviews') || this.initializeReviews();
        this.cart = this.loadFromStorage('cart') || [];
        this.currentUser = this.loadFromStorage('currentUser') || null;
        
        this.saveToStorage();
    }
    
    // Инициализация товаров с правильными описаниями
    initializeProducts() {
        const products = [];
        
        // Красивые описания для товаров
        const sweaterDescriptions = [
            "Уютный свитер из мягкой мериносовой шерсти с ажурным узором",
            "Теплый свитер с нордическим орнаментом для холодных дней",
            "Элегантный свитер с косичками и воротником-стойкой",
            "Свитер оверсайз с объемным узором и свободным кроем",
            "Классический свитер с V-образным вырезом и резинкой",
            "Свитер с рельефным узором и удлиненной спинкой"
        ];
        
        const cardiganDescriptions = [
            "Кардиган на пуговицах с ажурными узорами и длинным поясом",
            "Укороченный кардиган с объемными косами и крупными пуговицами",
            "Длинный кардиган-пальто с поясом и накладными карманами",
            "Кардиган свободного кроя с капюшоном и боковыми карманами",
            "Элегантный кардиган с запахом и декоративным поясом",
            "Уютный кардиган с крупной вязкой и деревянными пуговицами"
        ];
        
        const scarfDescriptions = [
            "Шарф из альпаки с ажурным узором и кистями",
            "Теплый шарф-снуд с рельефным узором кос",
            "Легкий ажурный шарф с цветочным мотивом",
            "Шарф крупной вязки с объемными косами",
            "Шелковый шарф с ручной вышивкой и бахромой",
            "Кашемировый шарф с классическим узором 'елочка'"
        ];
        
        const accessoriesDescriptions = [
            "Варежки с нордическим узором и подкладкой из флиса",
            "Перчатки с ажурным узором и отделкой кружевом",
            "Носки с резинкой и декоративным жаккардовым узором"
        ];
        
        const bagsDescriptions = [
            "Сумка-шоппер из хлопковой пряжи с деревянными ручками",
            "Эко-сумка с цветочным узором и длинными ручками",
            "Мини-сумка через плечо с ажурным узором",
            "Пляжная сумка крупной вязки с кистями",
            "Клатч с бисером и вышивкой ручной работы",
            "Рюкзак из прочной пряжи с кожаными деталями"
        ];
        
        const skirtsDescriptions = [
            "Юбка-карандаш с резинкой и разрезом сзади",
            "Юбка-миди с ажурным подолом и поясом",
            "Юбка-тюльпан с рельефными вертикальными линиями",
            "Юбка-макси с волнообразным узором и широким поясом",
            "Юбка с запахом и декоративным узлом",
            "Короткая юбка с плиссировкой и поясом-резинкой"
        ];
        
        const dressesDescriptions = [
            "Платье-миди с ажурным лифом и расклешенной юбкой",
            "Платье-футляр с рельефным узором и V-образным вырезом",
            "Платье-свитер с высоким воротником и разрезами по бокам",
            "Вечернее платье с ажурными рукавами и струящимся силуэтом",
            "Платье-трапеция с объемным узором и короткими рукавами",
            "Платье с запахом и поясом, подчеркивающим талию"
        ];

        // Свитеры (6)
        for (let i = 1; i <= 6; i++) {
            products.push({
                id: `sweater-${i}`,
                name: `Свитер ${i}`,
                category: 'sweaters',
                price: 2500 + i * 100,
                oldPrice: i % 2 === 0 ? 3000 + i * 100 : null,
                image: `images/sweater${i}.jpg`,
                description: sweaterDescriptions[i-1],
                isNew: i <= 2,
                isPopular: i <= 4
            });
        }
        
        // Кардиганы (6)
        for (let i = 1; i <= 6; i++) {
            products.push({
                id: `cardigan-${i}`,
                name: `Кардиган ${i}`,
                category: 'cardigans',
                price: 2800 + i * 100,
                oldPrice: i % 3 === 0 ? 3200 + i * 100 : null,
                image: `images/cardigan${i}.jpg`,
                description: cardiganDescriptions[i-1],
                isNew: i <= 2,
                isPopular: i <= 3
            });
        }
        
        // Варежки (3)
        for (let i = 1; i <= 3; i++) {
            products.push({
                id: `mittens-${i}`,
                name: `Варежки ${i}`,
                category: 'accessories',
                subcategory: 'mittens',
                price: 800 + i * 50,
                oldPrice: i === 2 ? 1000 : null,
                image: `images/mittens${i}.jpg`,
                description: accessoriesDescriptions[i-1],
                isNew: i === 1,
                isPopular: i <= 2
            });
        }
        
        // Шарфы (6)
        for (let i = 1; i <= 6; i++) {
            products.push({
                id: `scarf-${i}`,
                name: `Шарф ${i}`,
                category: 'accessories',
                subcategory: 'scarves',
                price: 1200 + i * 100,
                oldPrice: i % 2 === 0 ? 1500 + i * 100 : null,
                image: `images/scarf${i}.jpg`,
                description: scarfDescriptions[i-1],
                isNew: i <= 2,
                isPopular: i <= 4
            });
        }
        
        // Носки (3)
        for (let i = 1; i <= 3; i++) {
            products.push({
                id: `socks-${i}`,
                name: `Носки ${i}`,
                category: 'accessories',
                subcategory: 'socks',
                price: 600 + i * 50,
                oldPrice: i === 3 ? 800 : null,
                image: `images/socks${i}.jpg`,
                description: `Уютные носки ручной работы с жаккардовым узором. Идеальны для холодных вечеров.`,
                isNew: i === 1,
                isPopular: i <= 2
            });
        }
        
        // Сумки (6)
        for (let i = 1; i <= 6; i++) {
            products.push({
                id: `bag-${i}`,
                name: `Сумка ${i}`,
                category: 'bags',
                price: 1800 + i * 100,
                oldPrice: i % 3 === 0 ? 2200 + i * 100 : null,
                image: `images/bag${i}.jpg`,
                description: bagsDescriptions[i-1],
                isNew: i <= 2,
                isPopular: i <= 3
            });
        }
        
        // Юбки (6)
        for (let i = 1; i <= 6; i++) {
            products.push({
                id: `skirt-${i}`,
                name: `Юбка ${i}`,
                category: 'skirts',
                price: 2200 + i * 100,
                oldPrice: i % 2 === 0 ? 2600 + i * 100 : null,
                image: `images/skirt${i}.jpg`,
                description: skirtsDescriptions[i-1],
                isNew: i <= 2,
                isPopular: i <= 4
            });
        }
        
        // Платья (6)
        for (let i = 1; i <= 6; i++) {
            products.push({
                id: `dress-${i}`,
                name: `Платье ${i}`,
                category: 'dresses',
                price: 3500 + i * 100,
                oldPrice: i % 3 === 0 ? 4000 + i * 100 : null,
                image: `images/dress${i}.jpg`,
                description: dressesDescriptions[i-1],
                isNew: i <= 2,
                isPopular: i <= 3
            });
        }
        
        return products;
    }
    
    // Инициализация отзывов
    initializeReviews() {
        return [
            {
                id: 1,
                author: 'Анна',
                rating: 5,
                text: 'Очень качественные вещи! Заказывала свитер и кардиган, все пришло быстро и идеально село по фигуре. Обязательно буду заказывать еще!',
                date: '2025-01-15'
            },
            {
                id: 2,
                author: 'Мария',
                rating: 4,
                text: 'Шарф просто потрясающий! Очень теплый и красивый. Единственное - доставка заняла чуть больше времени, чем ожидалось.',
                date: '2025-01-10'
            },
            {
                id: 3,
                author: 'Елена',
                rating: 5,
                text: 'Платье просто волшебное! Все подружки спрашивают, где я его купила. Качество на высоте, все швы аккуратные. Спасибо!',
                date: '2025-01-05'
            }
        ];
    }
    
    // Получение товаров по категории
    getProductsByCategory(category) {
        if (category === 'all') return this.products;
        if (category === 'new') return this.products.filter(p => p.isNew);
        if (category === 'sale') return this.products.filter(p => p.oldPrice);
        
        return this.products.filter(p => p.category === category);
    }
    
    // Получение популярных товаров
    getPopularProducts() {
        return this.products.filter(p => p.isPopular);
    }
    
    // Получение товаров со скидкой
    getSaleProducts() {
        return this.products.filter(p => p.oldPrice);
    }
    
    // Получение товара по ID
    getProductById(id) {
        return this.products.find(p => p.id === id);
    }
    
    // Добавление пользователя
    addUser(user) {
        const existingUser = this.users.find(u => u.email === user.email);
        if (existingUser) {
            return { success: false, message: 'Пользователь с таким email уже существует' };
        }
        
        user.id = Date.now().toString();
        user.favorites = [];
        this.users.push(user);
        this.saveToStorage();
        
        return { success: true, user };
    }
    
    // Авторизация пользователя
    login(email, password) {
        const user = this.users.find(u => u.email === email && u.password === password);
        if (user) {
            this.currentUser = user;
            this.saveToStorage();
            return { success: true, user };
        }
        
        return { success: false, message: 'Неверный email или пароль' };
    }
    
    // Выход пользователя
    logout() {
        this.currentUser = null;
        this.saveToStorage();
    }
    
    // Добавление товара в избранное
    addToFavorites(productId) {
        if (!this.currentUser) return { success: false, message: 'Необходимо авторизоваться' };
        
        const user = this.users.find(u => u.id === this.currentUser.id);
        if (!user.favorites.includes(productId)) {
            user.favorites.push(productId);
            this.currentUser = user;
            this.saveToStorage();
        }
        
        return { success: true };
    }
    
    // Удаление товара из избранного
    removeFromFavorites(productId) {
        if (!this.currentUser) return { success: false, message: 'Необходимо авторизоваться' };
        
        const user = this.users.find(u => u.id === this.currentUser.id);
        user.favorites = user.favorites.filter(id => id !== productId);
        this.currentUser = user;
        this.saveToStorage();
        
        return { success: true };
    }
    
    // Получение избранных товаров
    getFavorites() {
        if (!this.currentUser) return [];
        
        const user = this.users.find(u => u.id === this.currentUser.id);
        return user.favorites.map(id => this.getProductById(id)).filter(p => p);
    }
    
    // Добавление товара в корзину
    addToCart(productId, quantity = 1) {
        const existingItem = this.cart.find(item => item.productId === productId);
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.cart.push({
                productId,
                quantity
            });
        }
        
        this.saveToStorage();
        return { success: true };
    }
    
    // Обновление количества товара в корзине
    updateCartItem(productId, quantity) {
        const item = this.cart.find(item => item.productId === productId);
        
        if (item) {
            if (quantity <= 0) {
                this.cart = this.cart.filter(item => item.productId !== productId);
            } else {
                item.quantity = quantity;
            }
            
            this.saveToStorage();
        }
        
        return { success: true };
    }
    
    // Удаление товара из корзины
    removeFromCart(productId) {
        this.cart = this.cart.filter(item => item.productId !== productId);
        this.saveToStorage();
        
        return { success: true };
    }
    
    // Очистка корзины
    clearCart() {
        this.cart = [];
        this.saveToStorage();
        
        return { success: true };
    }
    
    // Получение корзины
    getCart() {
        return this.cart.map(item => {
            const product = this.getProductById(item.productId);
            return {
                ...item,
                product
            };
        }).filter(item => item.product);
    }
    
    // Получение общей суммы корзины
    getCartTotal() {
        return this.getCart().reduce((total, item) => {
            return total + (item.product.price * item.quantity);
        }, 0);
    }
    
    // Добавление отзыва
    addReview(rating, text) {
        const review = {
            id: Date.now(),
            author: this.currentUser ? this.currentUser.name : 'Аноним',
            rating,
            text,
            date: new Date().toISOString().split('T')[0]
        };
        
        this.reviews.push(review);
        this.saveToStorage();
        
        return { success: true, review };
    }
    
    // Сохранение в localStorage
    saveToStorage() {
        localStorage.setItem('knitwearShop_products', JSON.stringify(this.products));
        localStorage.setItem('knitwearShop_users', JSON.stringify(this.users));
        localStorage.setItem('knitwearShop_reviews', JSON.stringify(this.reviews));
        localStorage.setItem('knitwearShop_cart', JSON.stringify(this.cart));
        localStorage.setItem('knitwearShop_currentUser', JSON.stringify(this.currentUser));
    }
    
    // Загрузка из localStorage
    loadFromStorage(key) {
        const data = localStorage.getItem(`knitwearShop_${key}`);
        return data ? JSON.parse(data) : null;
    }
}

// Дополнительные функции для совместимости
function getPopularProducts() {
    return db.getPopularProducts();
}

function getSaleProducts() {
    return db.getSaleProducts();
}

function getProductsByCategory(category) {
    return db.getProductsByCategory(category);
}

// Создаем экземпляр базы данных
const db = new Database();