// Функции для работы с авторизацией
class AuthManager {
    constructor() {
        this.updateAuthUI();
    }
    
    // Обновление интерфейса в зависимости от статуса авторизации
    updateAuthUI() {
        const accountLink = document.getElementById('account-link');
        const favoritesLink = document.getElementById('favorites-link');
        
        if (db.currentUser) {
            accountLink.textContent = db.currentUser.name;
            favoritesLink.style.display = 'block';
        } else {
            accountLink.textContent = 'Личный кабинет';
            favoritesLink.style.display = 'none';
        }
    }
    
    // Регистрация
    register(name, email, password) {
        const result = db.addUser({ name, email, password });
        
        if (result.success) {
            db.login(email, password);
            this.updateAuthUI();
            return { success: true };
        }
        
        return result;
    }
    
    // Авторизация
    login(email, password) {
        const result = db.login(email, password);
        
        if (result.success) {
            this.updateAuthUI();
            return { success: true };
        }
        
        return result;
    }
    
    // Выход
    logout() {
        db.logout();
        this.updateAuthUI();
        return { success: true };
    }
}

// Создаем экземпляр менеджера авторизации
const authManager = new AuthManager();