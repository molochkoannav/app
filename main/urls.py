from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
]


handler404 = 'app.views.custom_404'