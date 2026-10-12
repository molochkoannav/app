from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/',    views.UserLoginView.as_view(),  name='login'),
    path('logout/',   views.UserLogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.RegisterView.as_view(),   name='register'),
    path('profile/',  views.ProfileView.as_view(),    name='profile'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name='password_change.html',
             success_url=reverse_lazy('users:profile')
         ),
         name='password_change'),
]