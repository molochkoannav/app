from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from .forms import LoginForm, RegisterForm


# ============================================================
# Вход
# ============================================================

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('users:profile')


# ============================================================
# Выход
# ============================================================

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')


# ============================================================
# Профиль
# ============================================================

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # get_username() вернёт email или username в зависимости от USERNAME_FIELD
        context['title'] = 'Личный кабинет'
        context['content'] = f'Добро пожаловать, {user.get_username()}!'
        return context


# ============================================================
# Регистрация
# ============================================================

class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:profile')
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)          # сразу логиним после регистрации
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('users:profile')

        messages.error(request, 'Исправьте ошибки в форме')
        return render(request, self.template_name, {'form': form})