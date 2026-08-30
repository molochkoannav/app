from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
import urllib.parse
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def catalog(request) -> HttpResponse:
    """Страница каталога"""
    context = {"title": "Каталог", "content": "Каталог товаров"}
    return render(request, 'catalog.html', context)