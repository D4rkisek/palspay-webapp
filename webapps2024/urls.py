from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home-page"),
    path('', include('staff.urls')),
    path('', include('register.urls')),
    path('', include('members.urls')),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
