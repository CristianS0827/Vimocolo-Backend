from django.db import models

from Accounts.models import Account
from Products. models import Product

class Cart(models.Model):
    Cart_id = models.CharField(max_length=250, blank= True)
    date_added = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.Cart_id

class CartItem(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.Product.Product_name
    
class Quotation(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.user.email