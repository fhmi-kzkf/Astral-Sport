"""
URL configuration for Bikes app.
"""

from django.urls import path
from . import views

app_name = 'bikes'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('<slug:slug>/', views.detail, name='detail'),
    path('stock/<int:pk>/', views.stock_badge, name='stock_badge'),
]
