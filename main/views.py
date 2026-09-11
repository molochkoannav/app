from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    FormView,
    CreateView,
    ListView,
    DetailView,
)
import urllib.parse
from app import settings
from catalog.models import Category, Product
from main.models import Contact
import logging

logger = logging.getLogger(__name__)


# ============================================================
# Вспомогательные утилиты (остаются функциями — это не контроллеры)
# ============================================================

def parse_form_data(post_data):
    """
    Функция для парсинга данных формы.
    Используется для обработки сложных форм.
    """
    parsed_data = {}
    for key, value in post_data.items():
        if key != 'csrfmiddlewaretoken':
            parsed_data[key] = value
    return parsed_data


def log_form_submission(request, form_name="Форма"):
    """
    Утилита для логирования отправки формы.
    """
    print(f"\n=== {form_name} ===")
    for key, value in request.POST.items():
        if key != 'csrfmiddlewaretoken':
            print(f"{key}: {value}")
    print("=" * (len(form_name) + 8) + "\n")

    logger.info(f"{form_name} отправлена: {request.POST}")


# ============================================================
# 1. index — TemplateView
# ============================================================

class IndexView(TemplateView):
    """Главная страница."""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_products = Product.objects.all().order_by('-created_at')[:5]
        for product in latest_products:
            print(
                f"ID: {product.id}, Название: {product.name_product}, "
                f"Цена: {product.price}, Создан: {product.created_at}"
            )
        context["title"] = "Главная - продажа товаров"
        context["content"] = "Главная"
        return context


# ============================================================
# 2. orders — TemplateView
# ============================================================

class OrdersView(TemplateView):
    """Страница заказов."""
    template_name = 'orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Заказы'
        context['content'] = 'Ваши заказы'
        return context


# ============================================================
# 3. contacts — View (GET + POST)
# ============================================================

class ContactsView(View):
    """Страница контактов с обработкой формы."""

    template_name = 'contacts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        # Валидация
        if not name or not email or not message_text:
            messages.error(request, 'Пожалуйста, заполните все обязательные поля')
            return redirect('contacts')

        # Сохранение в БД
        contact = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text
        )

        print("\n=== ДАННЫЕ ИЗ ФОРМЫ ===")
        print(f"Имя: {name}")
        print(f"Email: {email}")
        print(f"Тема: {subject}")
        print(f"Сообщение: {message_text}")
        print("========================\n")

        logger.info(f"Форма контактов отправлена: {request.POST}")

        messages.success(request, 'УРА! Сообщение успешно отправлено!')
        return redirect('contacts')


# ============================================================
# 4. profile — LoginRequiredMixin + TemplateView
# ============================================================

class ProfileView(LoginRequiredMixin, TemplateView):
    """Личный кабинет пользователя."""
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        context['content'] = f'Добро пожаловать, {self.request.user.username}!'
        return context


# ============================================================
# 5. register — View (GET + POST)
# ============================================================

class RegisterView(View):
    """Регистрация пользователя."""

    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        print("\n=== РЕГИСТРАЦИЯ ===")
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken' and key != 'password2':
                print(f"{key}: {value}")
        print("====================\n")

        # TODO: логика регистрации
        messages.success(request, 'Регистрация успешна!')
        return redirect('index')


# ============================================================
# 6. custom_404 — обработчик ошибки 404
# ============================================================

def custom_404(request, exception):
    """Кастомная страница 404 (обработчик ошибок, остаётся функцией)."""
    context = {
        'title': '404 - Страница не найдена',
        'content': 'Извините, запрашиваемая страница не существует.'
    }
    return render(request, 'non_page.html', context, status=404)