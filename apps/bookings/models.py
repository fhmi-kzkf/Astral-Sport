"""
Booking models for Astral Sport.
"""

from django.db import models
from apps.bikes.models import Bike


class Booking(models.Model):
    """Rental booking record."""

    STATUS_CHOICES = [
        ('pending', 'Menunggu Konfirmasi'),
        ('confirmed', 'Dikonfirmasi'),
        ('completed', 'Selesai'),
        ('cancelled', 'Dibatalkan'),
    ]

    DURATION_CHOICES = [
        (1, '1 Jam'),
        (2, '2 Jam'),
        (3, '3 Jam'),
        (4, '4 Jam'),
        (8, 'Setengah Hari (8 Jam)'),
        (24, 'Sehari Penuh (24 Jam)'),
    ]

    bike = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20)
    duration_hours = models.PositiveIntegerField(choices=DURATION_CHOICES)
    total_price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_name} - {self.bike.name} ({self.duration_hours}h)"

    def calculate_price(self):
        """Calculate total price based on duration."""
        if self.duration_hours >= 24:
            days = self.duration_hours // 24
            remaining_hours = self.duration_hours % 24
            self.total_price = (
                days * self.bike.price_per_day +
                remaining_hours * self.bike.price_per_hour
            )
        else:
            self.total_price = self.duration_hours * self.bike.price_per_hour
        return self.total_price

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.calculate_price()
        super().save(*args, **kwargs)
