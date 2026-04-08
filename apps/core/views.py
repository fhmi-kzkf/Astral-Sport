"""
Views for Core app — homepage and shared views.
"""

from django.shortcuts import render
from apps.bikes.models import Bike


def home(request):
    """Render the homepage with hero section and featured bikes."""
    featured_bikes = Bike.objects.select_related('category').filter(
        is_featured=True, status='available'
    )[:6]

    all_bikes = Bike.objects.select_related('category').filter(
        status='available'
    )[:8]

    # Use featured bikes if available, otherwise use all bikes
    bikes = featured_bikes if featured_bikes.exists() else all_bikes

    return render(request, 'core/home.html', {
        'featured_bikes': bikes,
    })
