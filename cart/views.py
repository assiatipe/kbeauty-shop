from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Panier, LignePanier
from products.models import Produit


def get_or_create_panier(user):
    panier, _ = Panier.objects.get_or_create(client=user)
    return panier


@login_required
def voir_panier(request):
    panier = get_or_create_panier(request.user)
    return render(request, 'cart/panier.html', {
        'panier': panier,
    })


@login_required
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(
        Produit,
        id=produit_id,
        disponible=True
    )

    panier = get_or_create_panier(request.user)

    ligne, created = LignePanier.objects.get_or_create(
        panier=panier,
        produit=produit
    )

    if not created:
        if ligne.quantite < produit.quantite_stock:
            ligne.quantite += 1
            ligne.save()
            messages.success(
                request,
                f'Quantité mise à jour pour {produit.nom}.'
            )
        else:
            messages.warning(request, 'Stock insuffisant.')
    else:
        if produit.quantite_stock > 0:
            messages.success(
                request,
                f'{produit.nom} ajouté au panier.'
            )
        else:
            ligne.delete()
            messages.warning(request, 'Ce produit est en rupture de stock.')

    next_url = request.POST.get('next') or request.GET.get('next') or 'voir_panier'
    return redirect(next_url)


@login_required
def modifier_quantite(request, ligne_id):
    ligne = get_object_or_404(
        LignePanier,
        id=ligne_id,
        panier__client=request.user
    )

    try:
        quantite = int(request.POST.get('quantite', 1))
    except ValueError:
        messages.error(request, 'Quantité invalide.')
        return redirect('voir_panier')

    if quantite <= 0:
        ligne.delete()
        messages.info(request, 'Produit retiré du panier.')

    elif quantite <= ligne.produit.quantite_stock:
        ligne.quantite = quantite
        ligne.save()
        messages.success(request, 'Quantité mise à jour.')

    else:
        messages.warning(request, 'Stock insuffisant.')

    return redirect('voir_panier')


@login_required
def supprimer_du_panier(request, ligne_id):
    ligne = get_object_or_404(
        LignePanier,
        id=ligne_id,
        panier__client=request.user
    )

    nom = ligne.produit.nom
    ligne.delete()

    messages.info(request, f'{nom} retiré du panier.')
    return redirect('voir_panier')


@login_required
def vider_panier(request):
    panier = get_or_create_panier(request.user)
    panier.lignes.all().delete()

    messages.info(request, 'Panier vidé.')
    return redirect('voir_panier')