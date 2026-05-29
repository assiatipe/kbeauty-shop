from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from .models import Produit, Categorie
from reviews.models import Avis
from recommendation.engine import get_recommendations


def home(request):
    """
    Page d'accueil Glow.kr.

    Affiche :
    - les catégories ;
    - les marques disponibles ;
    - les produits vedettes ;
    - les nouveautés ;
    - les étapes de la routine K-Beauty ;
    - quelques avis clients.
    """

    categories = Categorie.objects.all().order_by('nom')

    produits_disponibles = Produit.objects.filter(
        disponible=True
    ).select_related('categorie')

    produits_count = produits_disponibles.count()

    # Produits vedettes : on privilégie les produits en stock.
    produits_vedette = produits_disponibles.filter(
        quantite_stock__gt=0
    ).order_by('-date_ajout')[:4]

    # Nouveautés : derniers produits ajoutés.
    nouveautes = produits_disponibles.order_by('-date_ajout')[:4]

    # Marques dynamiques depuis les produits existants.
    marques = list(
        produits_disponibles
        .exclude(marque='')
        .values_list('marque', flat=True)
        .distinct()
        .order_by('marque')[:8]
    )

    # Si aucun produit n'a encore de marque, on affiche des marques de démonstration.
    if not marques:
        marques = [
            'COSRX',
            'Beauty of Joseon',
            'Anua',
            'Some By Mi',
            'SKIN1004',
            'Missha',
            'Laneige',
            'Innisfree',
        ]

    etapes_routine = [
        'Huile nettoyante',
        'Nettoyant mousse',
        'Exfoliant',
        'Tonique',
        'Essence',
        'Sérum',
        'Masque sheet',
        'Contour des yeux',
        'Crème hydratante',
        'Protection solaire',
    ]

    # Avis clients récents avec une bonne note.
    temoignages = Avis.objects.select_related(
        'auteur',
        'produit'
    ).filter(
        note__gte=4
    ).order_by('-date_creation')[:3]

    return render(request, 'products/home.html', {
        'categories': categories,
        'produits_count': produits_count,
        'produits_vedette': produits_vedette,
        'nouveautes': nouveautes,
        'marques': marques,
        'etapes_routine': etapes_routine,
        'temoignages': temoignages,
    })


def catalogue(request):
    produits = Produit.objects.filter(
        disponible=True
    ).select_related('categorie')

    categories = Categorie.objects.annotate(
        produit_count=Count('produits', filter=Q(produits__disponible=True))
    ).order_by('nom')

    categorie_slug = request.GET.get('categorie')
    q = request.GET.get('q', '').strip()
    tri = request.GET.get('tri', 'date')
    en_stock = request.GET.get('en_stock')

    if en_stock == 'on' or en_stock == 'true':
        produits = produits.filter(quantite_stock__gt=0)

    if categorie_slug:
        produits = produits.filter(categorie__slug=categorie_slug)

    if q:
        words = q.split()
        query = Q()
        for word in words:
            query |= (
                Q(nom__icontains=word) |
                Q(description__icontains=word) |
                Q(marque__icontains=word) |
                Q(ingredients__icontains=word) |
                Q(type_peau__icontains=word) |
                Q(categorie__nom__icontains=word)
            )
        produits = produits.filter(query).distinct()

    if tri == 'prix_asc':
        produits = produits.order_by('prix')
    elif tri == 'prix_desc':
        produits = produits.order_by('-prix')
    elif tri == 'date':
        produits = produits.order_by('-date_ajout')
    elif tri == 'note':
        # Ici on transforme le QuerySet en liste, car note_moyenne est une propriété Python.
        produits = sorted(
            produits,
            key=lambda p: p.note_moyenne,
            reverse=True
        )
    else:
        produits = produits.order_by('-date_ajout')

    categorie_active = None

    if categorie_slug:
        try:
            categorie_active = Categorie.objects.get(slug=categorie_slug)
        except Categorie.DoesNotExist:
            categorie_active = None

    return render(request, 'products/catalogue.html', {
        'produits': produits,
        'categories': categories,
        'categorie_active': categorie_active,
        'q': q,
        'tri': tri,
        'en_stock': en_stock,
    })


def detail_produit(request, slug):
    produit = get_object_or_404(
        Produit.objects.select_related('categorie'),
        slug=slug,
        disponible=True
    )

    avis_list = Avis.objects.filter(
        produit=produit
    ).select_related(
        'auteur'
    ).order_by('-date_creation')

    recommendations = get_recommendations(produit, n=4)

    user_avis = None

    if request.user.is_authenticated:
        try:
            user_avis = Avis.objects.get(
                produit=produit,
                auteur=request.user
            )
        except Avis.DoesNotExist:
            user_avis = None

    return render(request, 'products/detail.html', {
        'produit': produit,
        'avis_list': avis_list,
        'recommendations': recommendations,
        'user_avis': user_avis,
    })