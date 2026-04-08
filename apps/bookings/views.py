"""
Views for Bookings app — 3-click booking flow.
"""

import urllib.parse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from apps.bikes.models import Bike




def create_booking(request, slug):
    """Step 1: Show duration picker for selected bike."""
    bike = get_object_or_404(Bike, slug=slug)

    from apps.bookings.models import Booking
    duration_choices = Booking.DURATION_CHOICES

    return render(request, 'bookings/create.html', {
        'bike': bike,
        'duration_choices': duration_choices,
    })


def calculate_price(request):
    """Step 2: HTMX endpoint — calculate price based on duration."""
    bike_id = request.POST.get('bike_id')
    duration = int(request.POST.get('duration', 1))

    bike = get_object_or_404(Bike, pk=bike_id)

    if duration >= 24:
        days = duration // 24
        remaining = duration % 24
        total = int(days * bike.price_per_day + remaining * bike.price_per_hour)
    else:
        total = int(duration * bike.price_per_hour)

    return render(request, 'bookings/partials/_price_summary.html', {
        'bike': bike,
        'duration': duration,
        'total_price': total,
    })


def confirm_whatsapp(request):
    """Step 3: Generate WhatsApp deep link with pre-filled message."""
    bike_id = request.POST.get('bike_id')
    duration = request.POST.get('duration')
    total_price = request.POST.get('total_price')
    customer_name = request.POST.get('customer_name', '')

    bike = get_object_or_404(Bike, pk=bike_id)

    # Build WhatsApp message
    message = (
        f"Halo Astral Sport! 🚴‍♂️\n\n"
        f"Saya ingin menyewa:\n"
        f"🔹 Sepeda: {bike.name}\n"
        f"🔹 Durasi: {duration} jam\n"
        f"🔹 Estimasi Harga: Rp {int(float(total_price)):,}\n"
    )
    if customer_name:
        message += f"🔹 Nama: {customer_name}\n"
    message += "\nMohon konfirmasi ketersediaan. Terima kasih! 🙏"

    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/{settings.WHATSAPP_NUMBER}?text={encoded_message}"

    return render(request, 'bookings/partials/_whatsapp_link.html', {
        'bike': bike,
        'duration': duration,
        'total_price': total_price,
        'whatsapp_url': whatsapp_url,
        'customer_name': customer_name,
    })
