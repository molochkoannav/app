from django.db import models
from django.conf import settings

class Category(models.Model):
    name_category = models.CharField(max_length=50, verbose_name='Наименование')
    description = models.CharField(max_length=150, verbose_name='Описание')
    slug = models.SlugField(max_length=60, null=True, unique=True, blank=True, verbose_name='URL-код (слаг)')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_category)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name_category}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name_product = models.CharField(max_length=50, verbose_name='Наименование')
    description = models.CharField(max_length=150, verbose_name='Описание')
    image = models.ImageField(upload_to='product_images/', verbose_name='Изображение', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    published = models.BooleanField(default=False, verbose_name='Опубликован')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products', verbose_name='Владелец')
                                                                
    def __str__(self):
        return f'{self.name_product} {self.description}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]