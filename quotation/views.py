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
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from proyecto.settings import EMAIL_HOST_USER
from django.conf import settings
import resend

resend.api_key = "re_Jbvj1AbC_PVJzXGA7FMfRsYaSVP1HvTnW"

# Create your views here.
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

def enviar_correo_cotizacion(productos_info, usuario, usuario_email):
    asunto = 'Solicitud de cotización'
    lista_productos = '<br>'.join(productos_info)  # Usamos <br> para separar los productos en líneas
    mensaje = f"<p>Hola {usuario}, gracias por contactarte con nosotros. Aquí está la información solicitada:</p><p>{lista_productos}</p>"
    try:
        send_mail(
            subject=asunto,
            message='', 
            html_message=mensaje, 
            from_email=settings.EMAIL_HOST_USER, 
            recipient_list=[usuario_email],
            fail_silently=False,
        )
        print("Correo enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

class quotation(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        product_ids = request.data.get('product_ids', [])
        user_email = request.data.get('user_email', None)  # Aceptar email del usuario en la petición
        print(f'product_ids: {product_ids}, user_email: {user_email}')
        if not product_ids:
            return Response({'error': 'No se ha proporcionado ningún ID de producto.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user_email:
            return Response({'error': 'No se ha proporcionado un correo electrónico.'}, status=status.HTTP_400_BAD_REQUEST)

        productos_info = []
        for product_id in product_ids:
            try:
                producto = Product.objects.get(id=product_id)
                producto_info = f"{producto.Product_name} \nDescripción: {producto.Description[:150]}..."  # Limitar la descripción a 150 caracteres
                productos_info.append(producto_info)
            except Product.DoesNotExist:
                continue 

        usuario = "Cliente Interesado"  

        enviar_correo_cotizacion(productos_info, usuario, user_email)
        
        return Response({'mensaje': 'Solicitud de cotización enviada correctamente.'}, status=status.HTTP_200_OK)