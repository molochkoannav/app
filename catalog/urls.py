from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.CatalogView.as_view(), name="catalog"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("create/", views.ProductCreateView.as_view(), name="product_create"),
    path("<int:pk>/update/", views.ProductUpdateView.as_view(), name="product_update"),
    path("<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
]