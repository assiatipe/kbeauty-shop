"""
Chatbot K-Beauty — Aide à l'achat
Utilise l'API Anthropic (Claude) pour répondre aux questions
sur les produits skincare coréens disponibles en boutique.
"""
import json
import urllib.request
import urllib.error
import os


SYSTEM_PROMPT = """Tu es l'assistante beauté de la boutique A.D.S PRODUCTS spécialisée en K-Beauty (skincare coréen).
Tu aides les clientes à choisir les bons produits selon leur type de peau, leurs problèmes cutanés et leur budget.

Tes connaissances :
- Routine K-Beauty en 10 étapes (huile nettoyante, nettoyant mousse, exfoliant, tonique, essence, sérum/ampoule, masque, contour des yeux, hydratant, SPF)
- Ingrédients actifs coréens : mucin d'escargot, centella asiatica, niacinamide, acides AHA/BHA/PHA, galactomyces, céramides, hyaluronique
- Types de peau : sèche, grasse, mixte, sensible, acnéique, terne, mature
- Marques disponibles : COSRX, Laneige, Some By Mi, Klairs, Innisfree, Skin1004, Purito, Beauty of Joseon, Dr. Jart+, Mediheal, Missha, The Ordinary, Etude House, Tony Moly, Mizon, Heimish, Pyunkang Yul

Règles :
- Réponds toujours en français.
- Sois chaleureuse, bienveillante et professionnelle.
- Pose des questions pour mieux comprendre le type de peau et les besoins.
- Recommande des produits concrets disponibles dans la boutique et explique pourquoi.
- Reste concise (3-4 phrases max par réponse).
- **Flexibilité** : Tu peux répondre aux questions générales sur la boutique (livraison gratuite dès 399 MAD, paiement à la livraison ou par carte), et tu es ouverte aux discussions plus larges sur le bien-être, le maquillage, ou la beauté en général. N'hésite pas à être conversationnelle !
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
        return get_fallback_response(messages_history[-1]['content'] if messages_history else '')
    except Exception:
        return get_fallback_response(messages_history[-1]['content'] if messages_history else '')


def get_fallback_response(user_message):
    """Réponses de secours plus flexibles basées sur des mots-clés si pas d'API key."""
    msg = user_message.lower()

    # Salutations
    if any(w in msg for w in ['bonjour', 'salut', 'hello', 'bonsoir', 'coucou']):
        return "Bonjour ! Je suis l'assistante K-Beauty de A.D.S PRODUCTS. ✨ Quel est votre type de peau et quels sont vos besoins aujourd'hui ?"

    # Remerciements
    if any(w in msg for w in ['merci', 'thank', 'super', 'génial', 'top', 'parfait']):
        return "Avec grand plaisir ! 🥰 N'hésitez pas si vous avez d'autres questions sur nos produits ou votre routine."

    # Questions de boutique (livraison, paiement)
    if any(w in msg for w in ['livraison', 'expedition', 'délai', 'livrer']):
        return "La livraison est offerte à partir de 399 MAD d'achat ! 📦 Nous livrons partout au Maroc en 24h à 48h jours ouvrés."
    if any(w in msg for w in ['paiement', 'payer', 'carte', 'cash']):
        return "Vous pouvez payer en toute sécurité par carte bancaire sur le site, ou opter pour le paiement à la livraison (Cash on Delivery) ! 💳"

    # Skincare - Types de peau
    if any(w in msg for w in ['sèche', 'seche', 'tiraillement', 'déshydrat']):
        return "Pour une peau sèche, je vous recommande vivement l'**Essence COSRX Snail Mucin 96%** pour l'hydratation profonde, associée au **Laneige Water Sleeping Mask** le soir. 💧"
    if any(w in msg for w in ['grasse', 'brillance', 'pores', 'sébum']):
        return "Pour une peau grasse, le **Some By Mi AHA BHA PHA Toner** désobstrue les pores et contrôle le sébum. Le **The Ordinary Niacinamide 10%** est excellent pour réduire la brillance. ✨"
    if any(w in msg for w in ['acné', 'bouton', 'imperfection', 'cicatrice']):
        return "Pour l'acné, le duo **COSRX Low pH Cleanser** + **COSRX Snail 96 Serum** est très efficace. Le BHA nettoie les pores, et le mucin d'escargot répare les cicatrices. 🌿"
    if any(w in msg for w in ['sensible', 'rouge', 'réactive', 'irrité']):
        return "Pour une peau sensible, la **Skin1004 Centella Ampoule** calme les rougeurs immédiatement. Le **Klairs Toner** sans alcool ni parfum est également idéal pour apaiser. 🌸"
    if any(w in msg for w in ['mature', 'rides', 'anti-âge', 'anti age', 'vieillissement']):
        return "Pour l'anti-âge, misez sur la **Missha Time Revolution Night Repair Ampoule** (souvent comparée au sérum Estée Lauder) et la crème **Beauty of Joseon Dynasty Cream** au ginseng et eau de riz ! 🌟"
    
    # Préoccupations spécifiques
    if any(w in msg for w in ['tache', 'hyperpigmentation', 'teint', 'lumineux', 'éclat']):
        return "Pour les taches et l'éclat, le **Some By Mi Yuja Niacin Serum** est très efficace. Associez-le avec un bon SPF comme le **Beauty of Joseon Relief Sun** pour prévenir de nouvelles taches. ☀️"
    if any(w in msg for w in ['soleil', 'spf', 'protection', 'solaire']):
        return "Le **Beauty of Joseon Relief Sun SPF50+** est notre grand best-seller : texture ultralégère, aucun fini blanc. Le **Isntree Hyaluronic Acid Watery Sun Gel** est aussi exceptionnel pour l'hydratation. ☀️"
    if any(w in msg for w in ['vegan', 'cruelty-free', 'cruelty free', 'animal']):
        return "Beaucoup de nos marques coréennes sont cruelty-free ! **COSRX**, **Klairs**, et **Purito** proposent d'excellentes gammes 100% vegan et respectueuses des animaux. 🐰💚"

    # Routine et autres
    if any(w in msg for w in ['routine', 'commencer', 'débutant', 'étape']):
        return "Pour débuter, commencez par 3 étapes : **1) Nettoyant** (ex: COSRX Low pH), **2) Hydratant** (ex: Sérum ou Crème Centella), **3) Protection Solaire** le matin. Vous pourrez ajouter des étapes ensuite ! 🧴"
    if any(w in msg for w in ['masque', 'sheet mask']):
        return "Pour les masques en tissu (sheet masks), la gamme **Mediheal** est numéro 1 en Corée pour l'hydratation express ! 💦"
    if any(w in msg for w in ['prix', 'budget', 'pas cher', 'abordable']):
        return "K-Beauty rime avec accessibilité ! D'excellents produits abordables incluent la marque **The Ordinary**, le nettoyant **COSRX**, ou les petits masques **Tony Moly**. 💸"

    # Si rien ne correspond, une réponse d'attente amicale et ouverte
    return "Je vois ! Mon système est actuellement en mode simplifié (hors-ligne), mais je peux tout à fait vous conseiller sur les routines de peau, les problèmes spécifiques (acné, taches, hydratation), ou les infos pratiques de notre boutique (livraison, paiement). Que souhaitez-vous savoir ? ✨"
