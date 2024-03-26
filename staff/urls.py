from django.urls import path
from . import views

urlpatterns = [
    path('staff/', views.staff_view, name='staff-homepage'),
    path('registerstaff/', views.register_staff, name='register-staff')
]
