from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required  # ← ДОБАВЬТЕ ЭТУ СТРОКУ

def index(request) -> HttpResponse:
    context = {"title": "Главная - продажа товаров", "content": "Главная"}
    return render(request, 'index.html', context)

def catalog(request) -> HttpResponse:
    """Страница каталога"""
    context = {"title": "Каталог", "content": "Каталог товаров"}
    return render(request, 'catalog.html', context)

def orders(request):
    """Страница заказов"""
    context = {
        'title': 'Заказы',
        'content': 'Ваши заказы'
    }
    return render(request, 'orders.html', context)

def contacts(request):
    """Страница контактов"""
    context = {
        'title': 'Контакты',
        'content': 'Свяжитесь с нами'
    }
    return render(request, 'contacts.html', context)

@login_required  # ← ТЕПЕРЬ РАБОТАЕТ
def profile(request):
    """Личный кабинет пользователя"""
    context = {
        'title': 'Личный кабинет',
        'content': f'Добро пожаловать, {request.user.username}!'
    }
    return render(request, 'profile.html', context)

def register(request):
    """Регистрация пользователя"""
    # Здесь будет логика регистрации
    return render(request, 'register.html')

def mens_socks(request):
    """Страница категории 'Носки мужские'"""
    return render(request, 'mens_socks.html')