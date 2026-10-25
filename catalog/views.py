from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View,
)

from catalog.forms import ProductForm
from catalog.models import Category, Product
from catalog.services import (get_products_by_category,invalidate_products_by_category_cache, get_products)

MODERATOR_GROUP = "Модератор продуктов"


def is_moderator(user):
    """Модератор — staff или участник группы 'Модератор продуктов'."""
    return user.is_authenticated and (
        user.is_staff
        or user.groups.filter(name=MODERATOR_GROUP).exists()
    )


class OwnerOnlyMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Редактировать может только владелец."""

    def test_func(self):
        return self.get_object().owner == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied('Редактировать продукт может только его владелец.')
        return super().handle_no_permission()


class OwnerOrModeratorMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Удалять может владелец или модератор."""

    def test_func(self):
        product = self.get_object()
        return (
            product.owner == self.request.user
            or is_moderator(self.request.user)
        )

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied('Удалять продукт может только владелец или модератор.')
        return super().handle_no_permission()


class CatalogView(ListView):
    model = Product
    template_name = "catalog.html"
    context_object_name = "products"

    def get_queryset(self):
            return get_products()


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    


class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:catalog")
    success_message = "Товар «%(name_product)s» создан."

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        invalidate_products_by_category_cache(self.object.category.slug)
        return response


class ProductUpdateView(OwnerOnlyMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:catalog")

    def form_valid(self, form):
        form.instance.owner = self.object.owner
        old_name = self.get_object().name_product
        old_slug = self.object.category.slug

        response = super().form_valid(form)

        # Категория могла смениться — сбрасываем кеш и старой, и новой
        invalidate_products_by_category_cache(old_slug)
        invalidate_products_by_category_cache(self.object.category.slug)

        messages.success(self.request, f"Товар «{old_name}» обновлён.")
        return response


class ProductDeleteView(OwnerOrModeratorMixin, DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:catalog")
    raise_exception = True

    def form_valid(self, form):
        slug = self.object.category.slug
        response = super().form_valid(form)
        invalidate_products_by_category_cache(slug)
        messages.success(
            self.request,
            f"Товар «{form.instance.name_product}» удалён.",
        )
        return response


class ProductUnpublishView(LoginRequiredMixin, View):
    """Снятие продукта с публикации. Только POST, только с правом."""

    def post(self, request, pk):
        if not request.user.has_perm('catalog.can_unpublish_product'):
            raise PermissionDenied

        product = get_object_or_404(Product, pk=pk)
        if product.published:
            product.published = False
            product.save(update_fields=['published', 'updated_at'])
            messages.success(request, f"Товар «{product.name_product}» снят с публикации.")
        else:
            messages.info(request, f"Товар «{product.name_product}» и так не опубликован.")

        return redirect('catalog:catalog')


class ProductsByCategoryView(ListView):
    """Список продуктов в категории. Данные берутся из кеширующего сервиса."""
    model = Product
    template_name = "products_by_category.html"
    context_object_name = "products"

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, slug=self.kwargs["category_slug"]
        )
        return get_products_by_category(self.kwargs["category_slug"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["title"] = f"Продукты в категории: {self.category.name_category}"
        return context

   