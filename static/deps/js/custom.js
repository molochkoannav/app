document.addEventListener('DOMContentLoaded', function() {
    // ===== ЭЛЕМЕНТЫ САЙДБАРА =====
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const pageContent = document.getElementById('pageContent');

    // ===== Функция открытия/закрытия меню =====
    function toggleMenu() {
        const isOpen = sidebar.classList.toggle('open');
        overlay.classList.toggle('active');
        menuToggle.classList.toggle('active');
        pageContent.classList.toggle('shifted');

        // Меняем aria-label для доступности
        menuToggle.setAttribute('aria-label', isOpen ? 'Закрыть меню' : 'Открыть меню');
    }

    // Клик по кнопке-гамбургеру
    if (menuToggle) {
        menuToggle.addEventListener('click', toggleMenu);
    }

    // Клик по затемнению — закрываем меню
    if (overlay) {
        overlay.addEventListener('click', toggleMenu);
    }

    // Закрытие меню при нажатии ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('open')) {
            toggleMenu();
        }
    });

    // Клик по пунктам меню
    const menuItems = document.querySelectorAll('.sidebar-menu li');
    menuItems.forEach(function(item) {
        item.addEventListener('click', function() {
            // Убираем активный класс у всех пунктов
            menuItems.forEach(function(li) {
                li.classList.remove('active');
            });
            // Добавляем активный класс текущему
            item.classList.add('active');

            // Закрываем меню после выбора пункта (на мобильных удобно)
            if (window.innerWidth <= 768) {
                toggleMenu();
            }
        });
    });

    // ===== ВЫПАДАЮЩЕЕ МЕНЮ ПОЛЬЗОВАТЕЛЯ =====
    const userToggle = document.getElementById('userDropdownToggle');
    const userMenu = document.getElementById('userDropdownMenu');

    if (userToggle && userMenu) {
        // Открытие/закрытие по клику на кнопку пользователя
        userToggle.addEventListener('click', function(e) {
            e.stopPropagation(); // Останавливаем всплытие, чтобы не закрылось сразу
            userToggle.classList.toggle('active');
            userMenu.classList.toggle('show');
        });

        // Закрытие при клике вне меню
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.user-dropdown')) {
                userToggle.classList.remove('active');
                userMenu.classList.remove('show');
            }
        });

        // Закрытие при клике на пункт меню (Профиль или Выход)
        const menuLinks = userMenu.querySelectorAll('a');
        menuLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                userToggle.classList.remove('active');
                userMenu.classList.remove('show');
            });
        });

        // Закрытие при нажатии ESC (если открыто меню пользователя)
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && userMenu.classList.contains('show')) {
                userToggle.classList.remove('active');
                userMenu.classList.remove('show');
            }
        });

        // Закрытие при скролле (опционально)
        let scrollTimeout;
        window.addEventListener('scroll', function() {
            if (userMenu.classList.contains('show')) {
                clearTimeout(scrollTimeout);
                scrollTimeout = setTimeout(function() {
                    userToggle.classList.remove('active');
                    userMenu.classList.remove('show');
                }, 100);
            }
        });
    }

    // ===== ОБРАБОТКА КНОПОК "КУПИТЬ" =====
    const buyButtons = document.querySelectorAll('.btn-buy');
    buyButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const productCard = this.closest('.product-card');
            const productName = productCard ? productCard.querySelector('.product-name').textContent : 'Товар';
            
            // Визуальная обратная связь
            const originalText = this.textContent;
            this.textContent = '✅ Добавлено!';
            this.style.background = '#1f8b4c';
            this.disabled = true;
            
            setTimeout(function() {
                this.textContent = originalText;
                this.style.background = '';
                this.disabled = false;
            }.bind(this), 1500);
            
            // Здесь можно добавить AJAX-запрос для добавления в корзину
            console.log(`Товар "${productName}" добавлен в корзину`);
            
            // Опционально: показываем уведомление
            showNotification(`Товар "${productName}" добавлен в корзину!`);
        });
    });

    // ===== ФУНКЦИЯ ДЛЯ УВЕДОМЛЕНИЙ =====
    function showNotification(message) {
        // Удаляем старое уведомление, если есть
        const oldNotification = document.querySelector('.notification-toast');
        if (oldNotification) {
            oldNotification.remove();
        }

        const notification = document.createElement('div');
        notification.className = 'notification-toast';
        notification.textContent = message;
        
        // Стилизуем уведомление
        notification.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #280f44;
            color: white;
            padding: 16px 24px;
            border-radius: 12px;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            font-weight: 500;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
            z-index: 9999;
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            max-width: 400px;
        `;
        
        document.body.appendChild(notification);
        
        // Анимация появления
        requestAnimationFrame(function() {
            notification.style.transform = 'translateY(0)';
            notification.style.opacity = '1';
        });
        
        // Автоматическое скрытие через 3 секунды
        setTimeout(function() {
            notification.style.transform = 'translateY(100px)';
            notification.style.opacity = '0';
            setTimeout(function() {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 400);
        }, 3000);
    }

    // ===== ОБРАБОТКА АКТИВНЫХ ССЫЛОК В САЙДБАРЕ =====
    // Подсвечиваем текущую страницу в меню
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('.sidebar-menu li');
    menuLinks.forEach(function(item) {
        const link = item.querySelector('a');
        if (link) {
            const href = link.getAttribute('href');
            if (href && currentPath.includes(href)) {
                menuLinks.forEach(function(li) {
                    li.classList.remove('active');
                });
                item.classList.add('active');
            }
        }
    });
});