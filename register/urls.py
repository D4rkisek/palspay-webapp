from django.urls import path
from . import views

urlpatterns = [
    path('register-user/', views.register_user, name='register-user'),
    path('login-user/', views.login_user, name='login-user'),
]
