from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'Slug':('Product_name',)}
    list_display = ('Product_name', 'SubCategory','Modified_date','Is_available')

