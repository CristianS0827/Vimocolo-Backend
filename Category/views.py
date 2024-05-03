from rest_framework import permissions, viewsets

from .serializer import CategorySerializer, SubCategorySerializer
from .models import Category, SubCategory


### clase para permitir solo el metodo GET
class readOnlyUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
            return request.method == 'GET'

class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [readOnlyUserPermission]
    queryset = Category.objects.all()

    
class SubCategoryView(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    permission_classes = [readOnlyUserPermission]
    queryset = SubCategory.objects.all()
