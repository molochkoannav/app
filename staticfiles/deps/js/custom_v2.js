
// ===== ПОЛНАЯ ОЧИСТКА ВСЕХ ОБРАБОТЧИКОВ =====
(function() {
    const allBtns = document.querySelectorAll('.btn-buy, .catalog-btn, button');
    allBtns.forEach(function(btn) {
        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);
    });
    console.log('✅ Все обработчики кнопок удалены (v2)');
})();

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ custom_v2.js загружен');

    // ===== ЭЛЕМЕНТЫ САЙДБАРА =====
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const pageContent = document.getElementById('pageContent');

    function toggleMenu() {
        const isOpen = sidebar.classList.toggle('open');
        overlay.classList.toggle('active');
        menuToggle.classList.toggle('active');
        pageContent.classList.toggle('shifted');
        menuToggle.setAttribute('aria-label', isOpen ? 'Закрыть меню' : 'Открыть меню');
    }

    if (menuToggle) menuToggle.addEventListener('click', toggleMenu);
    if (overlay) overlay.addEventListener('click', toggleMenu);

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('open')) {
            toggleMenu();
        }
    });

    // ===== ПУНКТЫ МЕНЮ =====
    const menuItems = document.querySelectorAll('.sidebar-menu li');
    menuItems.forEach(function(item) {
        item.addEventListener('click', function() {
            menuItems.forEach(function(li) { li.classList.remove('active'); });
            item.classList.add('active');
            if (window.innerWidth <= 768) toggleMenu();
        });
    });

    // ===== ВЫПАДАЮЩЕЕ МЕНЮ ПОЛЬЗОВАТЕЛЯ =====
    const userToggle = document.getElementById('userDropdownToggle');
    const userMenu = document.getElementById('userDropdownMenu');

    if (userToggle && userMenu) {
        userToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            userToggle.classList.toggle('active');
            userMenu.classList.toggle('show');
        });

        document.addEventListener('click', function(e) {
            if (!e.target.closest('.user-dropdown')) {
                userToggle.classList.remove('active');
                userMenu.classList.remove('show');
            }
        });
    }

    // ===== ГЛАВНЫЙ ОБРАБОТЧИК КНОПОК =====
    document.addEventListener('click', function(e) {
        const button = e.target.closest('button');
        if (!button) return;
        
        // Проверка: это кнопка каталога?
        if (button.classList.contains('catalog-btn')) {
            e.preventDefault();
            e.stopPropagation();
            const url = button.getAttribute('data-url');
            console.log('🔗 ПЕРЕХОД В КАТЕГОРИЮ:', url);
            if (url) {
                window.location.href = url;
            }
            return;
        }
        
        // Проверка: это кнопка "Купить"?
        if (button.classList.contains('btn-buy') && !button.classList.contains('catalog-btn')) {
            e.preventDefault();
            e.stopPropagation();
            
            const productCard = button.closest('.product-card');
            const productName = productCard ? productCard.querySelector('.product-name').textContent : 'Товар';
            
            const originalText = button.textContent;
            button.textContent = ' ✅ Добавлено!';
            button.style.background = '#72f052';
            button.disabled = true;
            
            setTimeout(function() {
                button.textContent = originalText;
                button.style.background = '';
                button.disabled = false;
            }, 1500);
            
            showNotification(`Товар "${productName}" добавлен в корзину!`);
            console.log('🛒 Товар добавлен:', productName);
        }
    });

    function showNotification(message) {
        const oldNotification = document.querySelector('.notification-toast');
        if (oldNotification) oldNotification.remove();

        const notification = document.createElement('div');
        notification.className = 'notification-toast';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed; bottom: 30px; right: 30px;
            background: #280f44; color: white;
            padding: 16px 24px; border-radius: 12px;
            font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500;
            box-shadow: 0 8px 30px rgba(0,0,0,0.3);
            z-index: 9999;
            transform: translateY(100px); opacity: 0;
            transition: all 0.4s cubic-bezier(0.4,0,0.2,1);
            max-width: 400px;
        `;
        document.body.appendChild(notification);
        
        requestAnimationFrame(function() {
            notification.style.transform = 'translateY(0)';
            notification.style.opacity = '1';
        });
        
        setTimeout(function() {
            notification.style.transform = 'translateY(100px)';
            notification.style.opacity = '0';
            setTimeout(function() {
                if (notification.parentNode) notification.remove();
            }, 400);
        }, 3000);
    }

    // ===== ПОДСВЕТКА ТЕКУЩЕЙ СТРАНИЦЫ =====
    const currentPath = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.sidebar-menu li');
    sidebarLinks.forEach(function(item) {
        const link = item.querySelector('a');
        if (link && link.getAttribute('href') && currentPath.includes(link.getAttribute('href'))) {
            sidebarLinks.forEach(function(li) { li.classList.remove('active'); });
            item.classList.add('active');
        }
    });

    console.log('📊 Найдено кнопок каталога (.catalog-btn):', document.querySelectorAll('.catalog-btn').length);
});