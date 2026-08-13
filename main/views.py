from django.shortcuts import render
from django.http import HttpResponse

def index(request) -> HttpResponse:
    context = {"title": "Home page", "content": "Page content"}
    return render(request, 'index.html', context)

def about(request) -> HttpResponse:
    return HttpResponse('About page')

