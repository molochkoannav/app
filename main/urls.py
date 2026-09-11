from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
]


handler404 = 'app.views.custom_404'