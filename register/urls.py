from django.urls import path
from . import views

urlpatterns = [
    path('registercustomer/', views.register_customer, name='register-customer'),
    path('loginuser/', views.login_user, name='login-user'),
]
