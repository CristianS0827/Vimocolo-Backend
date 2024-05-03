from django.db import models
from django.urls import reverse

from Category.models import SubCategory, Category

class Product(models.Model):
    Product_name = models.CharField(max_length=200, unique=True)
    Slug = models.CharField(max_length=200, unique=True)
    Description = models.CharField(max_length=500, blank=True)
    Images = models.CharField( max_length=250)
    Is_available = models.BooleanField(default=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    SubCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True)
    Created_date = models.DateTimeField( auto_now_add=True)
    Modified_date = models.DateTimeField( auto_now=True)

    
    def get_url(self):
        return reverse('product_detail', args=[self.Category.Slug, self.Slug])

    def __str__(self):
        return self.Product_name


