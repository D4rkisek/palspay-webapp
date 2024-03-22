from django.urls import path, include
from . import views

urlpatterns = [
    path('admins/', views.admin_view, name='adminsOversight'),
    path('memberstransaction/', views.admin_view_transaction, name='transaction-page'),
]