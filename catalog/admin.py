from django.contrib import admin

from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_category', 'description'] 


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_product', 'price', 'category','description']  
    list_filter = ['category'] 
    search_fields = ['name', 'description']  
