from django import forms
from .models import Blog


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'preview_image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок поста',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Введите текст поста...',
            }),
            'preview_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'preview_image': 'Превью-изображение',
            'is_published': 'Опубликовать',
        }
        help_texts = {
            'preview_image': 'Загрузите изображение для превью (jpg, png).',
            'is_published': 'Снять галочку, чтобы сохранить как черновик.',
        }