"""
URL configuration for Astral Sport.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('bikes/', include('apps.bikes.urls')),
    path('booking/', include('apps.bookings.urls')),
    path('ai/', include('apps.ai_concierge.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
