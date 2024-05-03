from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from rest_framework import  viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializer import ProductSerializer
from .models import Product
from Category.views import readOnlyUserPermission
from Category.models import Category

class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [readOnlyUserPermission]
    queryset = Product.objects.all()

    def get_queryset(self):  
        Products = None
        categories = None 
        category_slug = self.kwargs.get('category_slug')

        if  category_slug == 'products':         
            Products = Product.objects.all().filter(Is_available=True)
        
        elif category_slug != None:
             categories = get_object_or_404(Category, Slug=category_slug)
             Products = Product.objects.filter(Category=categories) 
         
        return Products
    
@method_decorator(csrf_exempt, name='dispatch')
class product_detail(APIView):
    def get(self, request):
        product_id = request.data.get('product_id')

        try: 
            single_product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        Product_serializer = model_to_dict(single_product) 
        context = {
            'single_product': Product_serializer,
        }
        return Response(context, status=status.HTTP_200_OK)
    
    
    
