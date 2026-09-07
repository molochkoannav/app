from django.urls import path
from . import views

from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("catalog/", views.catalog, name="catalog"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/create/", views.product_create, name="product_create"),
]