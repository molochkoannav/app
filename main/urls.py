from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("", views.index, name = "index"),
    path("catalog/mens/", views.mens_socks, name="mens_socks"),
    path("catalog/womens/", views.womens_socks, name="womens_socks"),
    path("catalog/kids/", views.kids_socks, name="kids_socks"),
    path("catalog/wool/", views.wool_socks, name="wool_socks"),
    path('orders/', views.orders, name='orders'),
    path('contacts/', views.contacts, name='contacts'),
    path('profile/', views.profile, name='profile'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
]

