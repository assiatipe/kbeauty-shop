import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from products.models import Produit
from .engine import get_recommendations
from .chatbot import get_chatbot_response


def recommandations_produit(request, produit_id):
    try:
        produit = Produit.objects.get(id=produit_id, disponible=True)
        recommendations = get_recommendations(produit, n=4)

        return render(request, 'recommendation/widget.html', {
            'recommendations': recommendations,
            'produit': produit,
        })

    except Produit.DoesNotExist:
        return render(request, 'recommendation/widget.html', {
            'recommendations': [],
        })


@require_http_methods(["POST"])
def chatbot_api(request):
    """Endpoint API sécurisé pour le chatbot."""
    try:
        data = json.loads(request.body.decode('utf-8'))
        messages = data.get('messages', [])

        if not messages:
            return JsonResponse({
                'error': 'Messages requis'
            }, status=400)

        # Limiter l'historique à 10 messages pour ne pas dépasser le contexte
        messages = messages[-10:]

        response_text = get_chatbot_response(messages)

        return JsonResponse({
            'response': response_text
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'JSON invalide'
        }, status=400)

    except Exception:
        return JsonResponse({
            'error': 'Une erreur est survenue lors du traitement du message.'
        }, status=500)


def chatbot_page(request):
    """Page dédiée au chatbot."""
    return render(request, 'recommendation/chatbot.html')