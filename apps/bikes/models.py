"""
Bike inventory models for Astral Sport.
"""

from django.db import models
from django.urls import reverse


class BikeCategory(models.Model):
    """Category of bikes (Road, Mountain, Gravel, etc.)."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")

    class Meta:
        verbose_name_plural = "Bike Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Bike(models.Model):
    """Individual bike available for rental."""

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Maintenance'),
    ]

    TERRAIN_CHOICES = [
        ('asphalt', 'Aspal'),
        ('offroad', 'Off-Road'),
        ('mixed', 'Mixed Terrain'),
    ]

    # Basic info
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        BikeCategory,
        on_delete=models.CASCADE,
        related_name='bikes'
    )
    description = models.TextField()
    tagline = models.CharField(max_length=200, blank=True)

    # Media
    image = models.ImageField(upload_to='bikes/', blank=True, null=True)

    # Pricing
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=0)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=0)

    # Specs
    terrain_type = models.CharField(max_length=20, choices=TERRAIN_CHOICES, default='asphalt')
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, default=10.0)
    frame_material = models.CharField(max_length=100, default='Aluminium Alloy')
    gear_system = models.CharField(max_length=100, blank=True, default='Shimano 21-Speed')
    wheel_size = models.CharField(max_length=50, blank=True, default='700c')

    # Inventory
    total_units = models.PositiveIntegerField(default=1)
    available_units = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    # Data insights
    calories_per_km = models.DecimalField(
        max_digits=5, decimal_places=1, default=40.0,
        help_text="Estimated calories burned per km"
    )
    co2_saved_per_km = models.DecimalField(
        max_digits=5, decimal_places=1, default=210.0,
        help_text="CO2 grams saved vs driving per km"
    )

    # Featured
    is_featured = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bikes:detail', kwargs={'slug': self.slug})

    @property
    def is_available(self):
        return self.available_units > 0 and self.status == 'available'

    @property
    def stock_label(self):
        if self.available_units == 0:
            return 'Habis'
        elif self.available_units <= 2:
            return f'{self.available_units} Unit Tersisa'
        return f'{self.available_units} Unit'

    @property
    def stock_urgency(self):
        """Returns CSS class for stock urgency indicator."""
        if self.available_units == 0:
            return 'stock-empty'
        elif self.available_units <= 2:
            return 'stock-low'
        return 'stock-normal'
