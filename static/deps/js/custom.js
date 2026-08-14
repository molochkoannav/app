document.addEventListener('DOMContentLoaded', function() {
    // Элементы
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const pageContent = document.getElementById('pageContent');

    // Функция открытия/закрытия меню
    function toggleMenu() {
        const isOpen = sidebar.classList.toggle('open');
        overlay.classList.toggle('active');
        menuToggle.classList.toggle('active');
        pageContent.classList.toggle('shifted');

        // Меняем aria-label для доступности
        menuToggle.setAttribute('aria-label', isOpen ? 'Закрыть меню' : 'Открыть меню');
    }

    // Клик по кнопке-гамбургеру
    menuToggle.addEventListener('click', toggleMenu);

    // Клик по затемнению — закрываем меню
    overlay.addEventListener('click', toggleMenu);

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
});