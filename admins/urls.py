from django.urls import path, include
from . import views

urlpatterns = [
    path('admins/', views.admin, name='adminsOversight'),
]
