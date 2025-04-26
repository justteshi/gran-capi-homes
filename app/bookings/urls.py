# urls.py

from django.urls import path
from .views import home_view, guest_info_view, guest_info_success_view, check_reservation

urlpatterns = [
    path('', home_view, name='home'),
    path('checkin/<str:code>/', guest_info_view, name='guest-info'),  # Updated URL pattern
    path('guest-info/<str:code>/success/', guest_info_success_view, name='guest_info_success'),
    path('check/', check_reservation, name='check_reservation'),
]