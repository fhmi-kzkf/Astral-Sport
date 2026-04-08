"""
Views for AI Concierge — chat endpoint.
"""

import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .services import get_ai_response


@require_POST
def chat(request):
    """Handle AI chat messages via HTMX."""
    message = request.POST.get('message', '').strip()

    if not message:
        return render(request, 'ai_concierge/_message.html', {
            'role': 'assistant',
            'content': 'Silakan ketik pertanyaan Anda.',
        })

    # Get chat history from session
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    chat_history = request.session['chat_history']

    # Get AI response
    response_text = get_ai_response(message, chat_history)

    # Save to session history (keep last 20 messages)
    chat_history.append({'role': 'user', 'content': message})
    chat_history.append({'role': 'assistant', 'content': response_text})
    request.session['chat_history'] = chat_history[-20:]

    return render(request, 'ai_concierge/_message.html', {
        'role': 'assistant',
        'content': response_text,
    })


def clear_chat(request):
    """Clear chat history."""
    request.session['chat_history'] = []
    return JsonResponse({'status': 'cleared'})
