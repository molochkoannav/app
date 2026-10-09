from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """Менеджер для модели без username — логин по email."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True')
        return self._create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    """Кастомная модель авторизации пользователя"""
    username = None  
    avatar_image = models.ImageField(upload_to='avatar_images/', verbose_name='Изображение', blank=True, null=True, help_text= 'Загрузите свой аватар')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True, help_text= 'Введите номер телефона')
    country = models.CharField(max_length=50, verbose_name='Страна', blank=True, null=True, help_text= 'Введите страну')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()  
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
