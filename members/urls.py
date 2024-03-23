from django.urls import path, include
from . import views

urlpatterns = [
    path('member/', views.member_view, name='members-home-page'),
    #path('<str:username>/transactions/', views.member_transactions, name='user-transactions'),
]
