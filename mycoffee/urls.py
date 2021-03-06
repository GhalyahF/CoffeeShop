from django.urls import path
from . import views

app_name= 'mycoffee'

urlpatterns = [
    path('signup/', views.usersignup, name="signup"),
    path('login/', views.userlogin, name="login"),
    path('logout/', views.userlogout, name="logout"),

    path('create_coffee/', views.create_coffee, name='create_coffee'),
    path('ajax_price/', views.ajax_price, name="ajax_price"),
    path('', views.coffee_list, name='coffee_list'),
    path('coffee_detail/<coffee_id>/', views.coffee_detail, name="coffee_detail"),
]
