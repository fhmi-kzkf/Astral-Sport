"""
URL configuration for Bookings app.
"""

from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('<slug:slug>/', views.create_booking, name='create'),
    path('api/calculate-price/', views.calculate_price, name='calculate_price'),
    path('api/confirm-whatsapp/', views.confirm_whatsapp, name='confirm_whatsapp'),
]
