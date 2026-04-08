"""
Views for Bikes app — catalog, detail, and stock API.
"""

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Bike, BikeCategory


def catalog(request):
    """Display the bike catalog with optional category filtering."""
    categories = BikeCategory.objects.all()
    category_slug = request.GET.get('category', '')

    bikes = Bike.objects.select_related('category').filter(status='available')

    if category_slug:
        bikes = bikes.filter(category__slug=category_slug)

    # If HTMX request, return only the bike grid partial
    if request.htmx:
        return render(request, 'bikes/partials/_bike_grid.html', {
            'bikes': bikes,
        })

    return render(request, 'bikes/catalog.html', {
        'bikes': bikes,
        'categories': categories,
        'active_category': category_slug,
    })


def detail(request, slug):
    """Display detailed bike page with specs and booking CTA."""
    bike = get_object_or_404(Bike.objects.select_related('category'), slug=slug)

    # Calculate data insights for a sample 10km ride
    sample_distance = 10
    calories = float(bike.calories_per_km) * sample_distance
    co2_saved = float(bike.co2_saved_per_km) * sample_distance

    return render(request, 'bikes/detail.html', {
        'bike': bike,
        'sample_distance': sample_distance,
        'calories': int(calories),
        'co2_saved': int(co2_saved),
    })


def stock_badge(request, pk):
    """Return live stock badge HTML partial (polled by HTMX)."""
    bike = get_object_or_404(Bike, pk=pk)
    return render(request, 'bikes/partials/_stock_badge.html', {
        'bike': bike,
    })
