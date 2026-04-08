"""
Admin configuration for Bikes app.
"""

from django.contrib import admin
from .models import BikeCategory, Bike


@admin.register(BikeCategory)
class BikeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'price_per_hour', 'price_per_day',
        'available_units', 'total_units', 'status', 'is_featured'
    ]
    list_filter = ['category', 'status', 'terrain_type', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['available_units', 'status', 'is_featured']
    search_fields = ['name', 'description']
