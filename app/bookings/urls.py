# urls.py

from django.urls import path
from .views import guest_info_view, guest_info_success_view

urlpatterns = [
    path('checkin/<str:code>/', guest_info_view, name='guest-info'),  # Updated URL pattern
    path('guest-info/<str:code>/success/', guest_info_success_view, name='guest_info_success'),
]