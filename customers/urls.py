from django.urls import path

from payapp.views import transfer_money, request_money, respond_to_request
from .views import member_view, manage_requests


urlpatterns = [
    path('member/', member_view, name='members-homepage'),
    path('transfer/', transfer_money, name='transfer-money'),
    path('request/', request_money, name='request-money'),
    path('managerequests/', respond_to_request, name='manage-requests'),
]
