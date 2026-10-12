from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product


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


class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:catalog")


    def form_valid(self, form):
        old_name = self.get_object().name_product   
        response = super().form_valid(form)       
        messages.success(self.request, f"Товар «{old_name}» обновлён.")
        return response


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:catalog")

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Товар «{self.object.name_product}» удалён.",
        )
        return super().form_valid(form)