from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webapps2024/', views.home, name="home-page"),
    path('webapps2024/', include('staff.urls')),
    path('webapps2024/', include('register.urls')),
    path('webapps2024/', include('customers.urls')),
    path('logout/', LogoutView.as_view(next_page='/webapps2024/'), name='logout'),
    path('conversion/', include('conversion_api.urls')),
]
