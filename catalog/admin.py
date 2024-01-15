from django.contrib import admin
from catalog.models import Category, Product, ProductVersion


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category__name',)
    search_fields = ('name', 'description')


@admin.register(ProductVersion)
class ProductVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'number', 'name', 'current')
    list_filter = ('current',)
