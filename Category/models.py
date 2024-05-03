from django.db import models
from django.urls import reverse

class Category(models.Model):
    Category_name = models.CharField(max_length=30, unique=True)
    Description = models.CharField(max_length=255, blank=True)
    Slug = models.CharField(max_length=100, unique=True)
    Cat_image = models.CharField( max_length=250)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.Slug])
    
    def __str__(self):
        return self.Category_name
    
class SubCategory(models.Model):
    FKCategory_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    SubCategory_name = models.CharField(max_length=30, unique=True)
    Description = models.CharField(max_length=255, blank=True)
    Slug = models.CharField(max_length=100, unique=True)
    at_image = models.CharField( max_length=250)
    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'

    def get_url(self):
        return reverse('products_by_Subcategory', args=[self.Slug])
    
    def __str__(self):
        return self.SubCategory_name
