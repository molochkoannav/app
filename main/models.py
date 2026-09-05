from django.db import models

class Contact(models.Model):
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email')
    subject = models.CharField('Тема', max_length=200)
    message = models.TextField('Сообщение')
    created_at = models.DateTimeField('Дата отправки', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.email}"