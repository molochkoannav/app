from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
import urllib.parse
import logging

from catalog.forms import ProductForm
from catalog.models import Product

logger = logging.getLogger(__name__)

# Create your views here.
def catalog(request):
    products = Product.objects.all()
    return render(request, "catalog.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(
        request,
        "product_detail.html",
        {"product": product},
    )
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("catalog:catalog")
    return render(request, "product_form.html", {"form": form})