from django.contrib import admin
from .models import Category, SubCategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'Slug': ('Category_name',)}
    list_display = ('Category_name', 'Slug')

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'Slug': ('SubCategory_name',)}
    list_display = ('SubCategory_name', 'Slug','FKCategory_name')
