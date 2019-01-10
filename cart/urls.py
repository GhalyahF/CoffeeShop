from django.urls import path
from . import views



app_name= 'cart'

urlpatterns=[
    path('',views.cart, name="mycart"),
    path('create_address/', views.create_address, name="create_address"),
    path('select_address/', views.select_address, name="select_address"),
    path('checkout/', views.checkout, name="checkout")

]
