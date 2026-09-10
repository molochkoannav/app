from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Blog
from .forms import BlogPostForm

class BlogListView(ListView):
    model = Blog
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 5 

    def get_queryset(self):
        return Blog.objects.filter(is_published=True) 

class BlogPostDetailView(DetailView):
    """Детально страницы постов"""
    model = Blog
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj

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
    success_url = reverse_lazy('blog:post_list')

class BlogPostDeleteView(DeleteView):
    """DELETE"""
    model = Blog
    form_class = BlogPostForm 
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
