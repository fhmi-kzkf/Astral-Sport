"""
Context processors for global template variables.
"""

from django.conf import settings


def global_context(request):
    """Inject global variables into all templates."""
    return {
        'WHATSAPP_NUMBER': settings.WHATSAPP_NUMBER,
        'SITE_NAME': 'ASTRAL SPORT',
        'SITE_TAGLINE': 'Premium Bike Rental',
    }
