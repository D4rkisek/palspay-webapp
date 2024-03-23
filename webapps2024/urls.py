from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
from payapp.views import transfer_money

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home-page"),
    path('', include('admins.urls')),
    path('', include('register.urls')),
    path('', include('members.urls')),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('transfer/', transfer_money, name='transfer-money'),
]
