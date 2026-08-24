from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
import urllib.parse
import logging

logger = logging.getLogger(__name__)

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
    """Страница контактов с обработкой формы"""
    if request.method == 'POST':
        print("\n=== ДАННЫЕ ИЗ ФОРМЫ ===")
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':  
                print(f"{key}: {value}")
        print("========================\n")
      
        logger.info(f"Форма контактов отправлена: {request.POST}")
     
        messages.success(request, 'Сообщение отправлено!')
     
        return redirect('contacts')
    
    context = {
        'title': 'Контакты',
        'content': 'Свяжитесь с нами'
    }
    return render(request, 'contacts.html', context)

@login_required
def profile(request):
    """Личный кабинет пользователя"""
    context = {
        'title': 'Личный кабинет',
        'content': f'Добро пожаловать, {request.user.username}!'
    }
    return render(request, 'profile.html', context)

def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        print("\n=== РЕГИСТРАЦИЯ ===")
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken' and key != 'password2':
                print(f"{key}: {value}")
        print("====================\n")
        
        #логика регистрации
        messages.success(request, 'Регистрация успешна!')
        return redirect('index')
    
    return render(request, 'register.html')

def mens_socks(request):
    """Страница категории 'Носки мужские'"""
    context = {
        'title': 'Носки мужские',
        'category': 'mens'
    }
    return render(request, 'mens_socks.html', context)

def womens_socks(request):
    """Страница категории 'Носки женские'"""
    context = {
        'title': 'Носки женские',
        'category': 'womens'
    }
    return render(request, 'women_socks.html', context)

def kids_socks(request):
    """Страница категории 'Носки детские'"""
    context = {
        'title': 'Носки детские',
        'category': 'kids'
    }
    return render(request, 'kids_socks.html', context)

def wool_socks(request):
    """Страница категории 'Носки шерстяные'"""
    context = {
        'title': 'Носки шерстяные',
        'category': 'wool'
    }
    return render(request, 'wool_socks.html', context)

def custom_404(request, exception):
    """Кастомная страница 404"""
    context = {
        'title': '404 - Страница не найдена',
        'content': 'Извините, запрашиваемая страница не существует.'
    }
    return render(request, 'non_page.html', context, status=404)



def parse_form_data(post_data):
    """
    Функция для парсинга данных формы
    Используется для обработки сложных форм
    """
    parsed_data = {}
    for key, value in post_data.items():
        if key != 'csrfmiddlewaretoken':
            parsed_data[key] = value
    return parsed_data

def log_form_submission(request, form_name="Форма"):
    """
    Утилита для логирования отправки формы
    """
    print(f"\n=== {form_name} ===")
    for key, value in request.POST.items():
        if key != 'csrfmiddlewaretoken':
            print(f"{key}: {value}")
    print("=" * (len(form_name) + 8) + "\n")
    
    logger.info(f"{form_name} отправлена: {request.POST}")