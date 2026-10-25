from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

app_name = "catalog"

urlpatterns = [
    path("", views.CatalogView.as_view(), name="catalog"),
    path("<int:pk>/", cache_page(60)(vary_on_cookie(views.ProductDetailView.as_view())), name="product_detail"),
    path("create/", views.ProductCreateView.as_view(), name="product_create"),
    path("<int:pk>/update/", views.ProductUpdateView.as_view(), name="product_update"),
    path("<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
    path("<int:pk>/unpublish/", views.ProductUnpublishView.as_view(), name='product_unpublish'),
    path("category/<slug:category_slug>/",views.ProductsByCategoryView.as_view(),name="products_by_category"),
]