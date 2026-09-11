from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Blog
from django.conf import settings
from .forms import BlogPostForm


class BlogListView(ListView):
    model = Blog
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Детальная страница поста"""
    model = Blog
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        obj.views_count += 1
        obj.save(update_fields=['views_count'])

        if obj.views_count == 100:
            self.send_congrats_email(obj)

        return obj

    def send_congrats_email(self, blog):
        """Поздравление при достижении 100 просмотров."""
        try:
            send_mail(
                subject=f'Статья «{blog.title}» набрала 100 просмотров!',
                message=(
                    f'Поздравляем!\n\n'
                    f'Ваша статья «{blog.title}» достигла {blog.views_count} просмотров.\n'
                    f'Так держать!'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f'Не удалось отправить письмо: {e}')


class BlogPostCreateView(CreateView):
    """CREATE"""
    model = Blog
    form_class = BlogPostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('blog:post_list')


class BlogPostUpdateView(UpdateView):
    """UPDATE"""
    model = Blog
    form_class = BlogPostForm
    template_name = 'post_form.html'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    """DELETE"""
    model = Blog
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')