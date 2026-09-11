from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    preview_image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name='Превью изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=False, verbose_name='Признак публикации')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

# Create your models here.
