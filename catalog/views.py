from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin , PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from catalog.forms import ProductForm
from catalog.models import Product


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from catalog.forms import ProductForm
from catalog.models import Product

MODERATOR_GROUP = "Модератор продуктов"
def is_moderator(user):
    """Модератор — staff или участник группы 'moderators'."""
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
        return (product.owner == self.request.user
            or is_moderator(self.request.user))

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied('Удалять продукт может только владелец или модератор.')
        return super().handle_no_permission()



class CatalogView(ListView):
    model = Product
    template_name = "catalog.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def form_valid(self, form):
        messages.success(self.request, f"Товар «{self.object.name_product}» удалён.")

        return super().form_valid(form)


class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:catalog")
    success_message = "Товар «%(name_product)s» создан."

    def form_valid(self, form):
            form.instance.owner = self.request.user
            return super().form_valid(form)


class ProductUpdateView(OwnerOnlyMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:catalog")


    def form_valid(self, form):
        form.instance.owner = self.object.owner
        old_name = self.get_object().name_product
        response = super().form_valid(form)
        messages.success(self.request, f"Товар «{old_name}» обновлён.")
        return response

class ProductDeleteView(OwnerOrModeratorMixin, DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:catalog")
    permission_required = 'catalog.delete_product'
    raise_exception = True

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Товар «{self.object.name_product}» удалён.",
        )
        return super().form_valid(form)

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