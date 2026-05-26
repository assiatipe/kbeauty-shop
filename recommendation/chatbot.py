"""
Chatbot K-Beauty — Aide à l'achat
Utilise l'API Anthropic (Claude) pour répondre aux questions
sur les produits skincare coréens disponibles en boutique.
"""
import json
import urllib.request
import urllib.error
import os


SYSTEM_PROMPT = """Tu es Glow, l'assistante beauté de la boutique Glow.kr spécialisée en K-Beauty (skincare coréen).
Tu aides les clientes à choisir les bons produits selon leur type de peau, leurs problèmes cutanés et leur budget.

Tes connaissances :
- Routine K-Beauty en 10 étapes (huile nettoyante, nettoyant mousse, exfoliant, tonique, essence, sérum/ampoule, masque, contour des yeux, hydratant, SPF)
- Ingrédients actifs coréens : mucin d'escargot, centella asiatica, niacinamide, acides AHA/BHA/PHA, galactomyces, céramides, hyaluronique
- Types de peau : sèche, grasse, mixte, sensible, acnéique, terne
- Marques disponibles : COSRX, Laneige, Some By Mi, Klairs, Innisfree, Skin1004, Purito, Beauty of Joseon, Dr. Jart+, Mediheal, Missha, The Ordinary, Etude House, Tony Moly, Mizon, Heimish, Pyunkang Yul

Règles :
- Réponds toujours en français
- Sois chaleureuse, bienveillante et professionnelle
- Pose des questions pour mieux comprendre le type de peau et les besoins
- Recommande des produits concrets disponibles dans la boutique
- Explique pourquoi tu recommandes chaque produit
- Reste concise (3-4 phrases max par réponse)
- Si on te demande quelque chose hors beauté/skincare, recentre poliment la conversation
"""


def get_chatbot_response(messages_history):
    """
    Envoie l'historique de conversation à l'API Claude et retourne la réponse.
    messages_history : liste de dicts {'role': 'user'|'assistant', 'content': str}
    """
    api_key = os.getenv('ANTHROPIC_API_KEY', '')

    if not api_key:
        return get_fallback_response(messages_history[-1]['content'] if messages_history else '')

    payload = json.dumps({
        'model': 'claude-haiku-4-5-20251001',
        'max_tokens': 400,
        'system': SYSTEM_PROMPT,
        'messages': messages_history,
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01',
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data['content'][0]['text']
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return get_fallback_response(messages_history[-1]['content'] if messages_history else '')
    except Exception:
        return get_fallback_response(messages_history[-1]['content'] if messages_history else '')


def get_fallback_response(user_message):
    """Réponses de secours basées sur des mots-clés si pas d'API key."""
    msg = user_message.lower()

    if any(w in msg for w in ['bonjour', 'salut', 'hello', 'bonsoir']):
        return "Bonjour ! Je suis Glow, votre assistante K-Beauty. Quel est votre type de peau et quels sont vos besoins en skincare aujourd'hui ?"

    if any(w in msg for w in ['sèche', 'seche', 'tiraillement', 'déshydrat']):
        return "Pour une peau sèche, je vous recommande l'**Essence COSRX Snail Mucin 96%** pour l'hydratation profonde, associée à la **Laneige Water Sleeping Mask** le soir. Le **Klairs Supple Preparation Toner** sans alcool est aussi parfait comme première étape."

    if any(w in msg for w in ['grasse', 'brillance', 'pores', 'sébum']):
        return "Pour une peau grasse, le **Some By Mi AHA BHA PHA Toner** désobstrue les pores et contrôle le sébum. Le **The Ordinary Niacinamide 10%** est excellent pour réduire la brillance. Choisissez des textures gel légères."

    if any(w in msg for w in ['acné', 'bouton', 'imperfection', 'cicatrice']):
        return "Pour l'acné, le duo **COSRX Low pH Cleanser** + **COSRX Snail 96 Serum** est très efficace. Le BHA du nettoyant nettoie les pores, et le mucin d'escargot répare les cicatrices. Ajoutez le **Some By Mi Toner** pour un traitement complet."

    if any(w in msg for w in ['sensible', 'rouge', 'réactive', 'irrité']):
        return "Pour une peau sensible, la **Skin1004 Centella Ampoule** calme les rougeurs immédiatement. Le **Klairs Toner** sans alcool ni parfum est idéal. Évitez les acides forts et commencez doucement avec la routine."

    if any(w in msg for w in ['tache', 'hyperpigmentation', 'teint', 'lumineux', 'éclat']):
        return "Pour les taches et l'éclat, le **Some By Mi Yuja Niacin Serum** est très efficace en 30 jours. La **Missha Time Revolution Essence** aux ferments illumine le teint. Associez avec un bon SPF comme le **Beauty of Joseon Relief Sun**."

    if any(w in msg for w in ['soleil', 'spf', 'protection', 'solaire']):
        return "Pour la protection solaire, le **Beauty of Joseon Relief Sun SPF50+** est notre best-seller : texture ultraléger, fini naturel. Le **Purito Daily Sunscreen** est parfait pour les peaux sensibles ou enceintes."

    if any(w in msg for w in ['routine', 'commencer', 'débutant', 'étape']):
        return "Pour débuter la routine K-Beauty, commencez avec 3 étapes simples : **1) Nettoyant** (Banila Co Balm + COSRX Foam), **2) Hydratant** (COSRX Snail Essence), **3) SPF** (Beauty of Joseon). Ajoutez des étapes progressivement !"

    if any(w in msg for w in ['masque', 'sheet mask']):
        return "Pour les masques sheet, le **Mediheal N.M.F Aquaring** est le plus populaire au monde pour l'hydratation. Le **Skin1004 Centella Mask** est parfait après une exposition au soleil ou pour calmer la peau irritée."

    if any(w in msg for w in ['prix', 'budget', 'pas cher', 'abordable']):
        return "Excellents rapports qualité-prix : **Tony Moly Sheet Mask** (35 MAD), **The Ordinary Niacinamide** (139 MAD), **COSRX Low pH Cleanser** (159 MAD). Ces produits coréens sont efficaces sans se ruiner !"

    return "Je suis là pour vous aider à construire votre routine K-Beauty ! Pouvez-vous me décrire votre type de peau (sèche, grasse, mixte, sensible) et vos principales préoccupations (hydratation, acné, taches, rides...) ?"
