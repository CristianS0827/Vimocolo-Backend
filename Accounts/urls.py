from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('register/',views.register, name='register'),
    path('login/',views.Login.as_view(), name='login'),
    path('logout/',views.Logout.as_view(), name='logout'),

]

