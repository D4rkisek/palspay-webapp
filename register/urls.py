from django.urls import path
from . import views

urlpatterns = [
    path('registeruser/', views.register_user, name='register-user'),
    path('loginuser/', views.login_user, name='login-user'),
]
