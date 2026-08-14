from django.shortcuts import render
from django.http import HttpResponse

def index(request) -> HttpResponse:
    context = {"title": "Главная - продажа товаров", "content": "Главная"}
    return render(request, 'index.html', context)

def catalog(request) -> HttpResponse:
    context = {"title": "Каталог", "content": "Каталог товаров"}
    return render(request, 'catalog.html', context)

