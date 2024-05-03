from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.sessions.models import Session
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Cart, CartItem, Quotation
from Products.models import Product
from django.contrib.auth.decorators import login_required
from Accounts.models import Account
from django.core.mail import EmailMessage
from rest_framework.permissions import IsAuthenticated


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.save() 
        cart = request.session.session_key 
    return cart
      
# @method_decorator(csrf_exempt, name='dispatch')
class add_cart(APIView):
    permission_classes = [IsAuthenticated]
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def post(self, request):
        product_id = request.data.get('product_id')
        product = Product.objects.get(id=product_id)  
        try:
            cart = Cart.objects.get(Cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(Cart_id=_cart_id(request))
            cart.save()
        
        try:
            cart_item = CartItem.objects.get(Product=product, Cart=cart)
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(Product=product, Cart=cart)
            cart_item.save()
        return Response('item add to cart successfully', status=status.HTTP_200_OK)
    # else: 
    #     return Response({'error':'acccess denied, user not authenticated '}, status=status.HTTP_401_UNAUTHORIZED)
    
@method_decorator(csrf_exempt, name='dispatch')  
class remove_cart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        product_id = request.data.get('product_id')
        cart = Cart.objects.get(Cart_id = _cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(Product=product, Cart=cart)
        cart_item.delete()

        return Response('item remove to cart susesfully', status=status.HTTP_200_OK)

def get_cart_data(request):
    cart_items = []

    try:
        cart = Cart.objects.get(Cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(Cart=cart)
                
    except ObjectDoesNotExist:
        pass

    cart_items_serialized = [model_to_dict(item) for item in cart_items]

    context = {
        'cart_items': cart_items_serialized,
    }

    return context

@method_decorator(csrf_exempt, name='dispatch')
class cart(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        context = get_cart_data(request)
        return Response({'cart': context}, status=status.HTTP_200_OK)
from django.contrib.auth import get_user_model

def enviar_correo_cotizacion(productos, usuario, usuario_gmail):
    asunto = 'Solicitud de cotización'
    mensaje = f'Hola {usuario} gracias por contactarte con nosotros en poco tiempo te estaremos brindando mas informacion de los siguientes productos: {productos}'
    send_mail = EmailMessage(asunto, mensaje,to=[usuario_gmail])
    send_mail.send()
    
@method_decorator(csrf_exempt, name='dispatch')
class quotation(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cart_context = get_cart_data(request)
        cart_items = cart_context.get('cart_items', [])
        cart = Cart.objects.get(Cart_id=_cart_id(request))

        productos = []

        for item in cart_items:
            product_id = item.get('Product')

            try:
                producto = Product.objects.get(id=product_id)
                productos.append(producto.Product_name)
            except producto.DoesNotExist:
                pass
            
        User = get_user_model()
        user = request.user

        
        usuario = user.first_name
        correo_usuario = user.email
        enviar_correo_cotizacion(productos,usuario, correo_usuario)
        quotation = Quotation.objects.create(user=user, cart=cart)
        quotation.save()
        
        return Response({'mensaje': 'Solicitud de cotización enviada correctamente.'}, status=status.HTTP_200_OK)