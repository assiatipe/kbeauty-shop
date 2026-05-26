from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Commande, LigneCommande
from cart.models import Panier
from .forms import CommandeForm


@login_required
def valider_commande(request):
    try:
        panier = Panier.objects.get(client=request.user)
    except Panier.DoesNotExist:
        messages.error(request, 'Votre panier est vide.')
        return redirect('catalogue')

    if not panier.lignes.exists():
        messages.error(request, 'Votre panier est vide.')
        return redirect('voir_panier')

    # Vérification des stocks
    for ligne in panier.lignes.all():
        if ligne.quantite > ligne.produit.quantite_stock:
            messages.error(request, f'Stock insuffisant pour {ligne.produit.nom}.')
            return redirect('voir_panier')

    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = Commande.objects.create(
                client=request.user,
                adresse_livraison=form.cleaned_data['adresse_livraison'],
                ville_livraison=form.cleaned_data['ville_livraison'],
                code_postal_livraison=form.cleaned_data['code_postal_livraison'],
                pays_livraison=form.cleaned_data['pays_livraison'],
                notes=form.cleaned_data.get('notes', ''),
            )
            for ligne in panier.lignes.all():
                LigneCommande.objects.create(
                    commande=commande,
                    produit=ligne.produit,
                    nom_produit=ligne.produit.nom,
                    prix_unitaire=ligne.produit.prix,
                    quantite=ligne.quantite,
                )
                # Diminuer le stock
                ligne.produit.quantite_stock -= ligne.quantite
                ligne.produit.save()

            commande.calculer_total()
            panier.lignes.all().delete()

            messages.success(request, f'Commande #{commande.id} passée avec succès !')
            return redirect('confirmation_commande', commande_id=commande.id)
    else:
        # Pré-remplir avec les infos du profil
        initial = {}
        try:
            profil = request.user.profil
            initial = {
                'adresse_livraison': profil.adresse,
                'ville_livraison': profil.ville,
                'code_postal_livraison': profil.code_postal,
                'pays_livraison': profil.pays,
            }
        except:
            pass
        form = CommandeForm(initial=initial)

    return render(request, 'orders/valider_commande.html', {
        'form': form,
        'panier': panier,
    })


@login_required
def confirmation_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, client=request.user)
    return render(request, 'orders/confirmation.html', {'commande': commande})


@login_required
def historique_commandes(request):
    commandes = Commande.objects.filter(client=request.user).order_by('-date_commande')
    return render(request, 'orders/historique.html', {'commandes': commandes})


@login_required
def detail_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, client=request.user)
    return render(request, 'orders/detail.html', {'commande': commande})
