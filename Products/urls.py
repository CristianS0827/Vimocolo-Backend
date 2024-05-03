from django.urls import path, include
from rest_framework import routers

from .views import ProductView, product_detail


router_products = routers.DefaultRouter()
router_products.register(r'', ProductView, 'products')

urlpatterns = [
    path('productDetail/',product_detail.as_view(), name= 'product_detail'),
    path('<slug:category_slug>/', include(router_products.urls), name= 'product'),
]
