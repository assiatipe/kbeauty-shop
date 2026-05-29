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
                mode_paiement=form.cleaned_data.get('mode_paiement', 'livraison'),
            )
            for ligne in panier.lignes.all():
                LigneCommande.objects.create(
                    commande=commande,
                    produit=ligne.produit,
                    nom_produit=ligne.produit.nom,
                    prix_unitaire=ligne.produit.prix_actuel,
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


@login_required
def client_action_commande(request, commande_id, action):
    commande = get_object_or_404(Commande, id=commande_id, client=request.user)
    
    if action == 'annuler':
        if commande.statut == 'en_attente':
            commande.statut = 'annulee'
            commande.save()
            messages.success(request, f"Votre commande #{commande.id} a été annulée.")
        else:
            messages.error(request, "Vous ne pouvez plus annuler cette commande.")
            
    elif action == 'valider_reception':
        if commande.statut == 'expediee':
            commande.statut = 'livree'
            commande.save()
            messages.success(request, f"Merci d'avoir confirmé la réception de la commande #{commande.id}.")
        else:
            messages.error(request, "Cette commande ne peut pas encore être marquée comme livrée.")
            
    return redirect('detail_commande', commande_id=commande.id)


from django.http import JsonResponse
from django.utils.timezone import now

def recent_purchases_api(request):
    """API endpoint to return recent purchases for social proof toasts."""
    recent_lignes = LigneCommande.objects.select_related('commande__client', 'produit').order_by('-commande__date_commande')[:10]
    
    purchases = []
    for ligne in recent_lignes:
        client_name = ligne.commande.client.first_name or ligne.commande.client.username
        ville = ligne.commande.ville_livraison or 'Maroc'
        produit_nom = ligne.nom_produit
        
        delta = now() - ligne.commande.date_commande
        minutes = int(delta.total_seconds() / 60)
        
        if minutes == 0:
            time_str = "À l'instant"
        elif minutes < 60:
            time_str = f"Il y a {minutes} min"
        elif minutes < 1440:
            heures = minutes // 60
            time_str = f"Il y a {heures} h"
        else:
            jours = minutes // 1440
            time_str = f"Il y a {jours} j"

        purchases.append({
            'name': client_name,
            'city': ville,
            'product': produit_nom,
            'time': time_str,
        })
        
    return JsonResponse({'purchases': purchases})
