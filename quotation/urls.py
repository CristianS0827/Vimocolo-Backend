from django.urls import path

from . import views

urlpatterns = [
    path("", views.cart.as_view(), name="cart"),
    path('add_cart/',views.add_cart.as_view(), name='add_cart' ),
    path('remove_cart/',views.remove_cart.as_view(), name='remove_cart'),
    path('quotation/',views.quotation.as_view(), name='quotation'),
    
]
