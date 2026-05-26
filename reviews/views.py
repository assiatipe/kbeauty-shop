from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Avis
from products.models import Produit


@login_required
def ajouter_avis(request, produit_slug):
    produit = get_object_or_404(
        Produit,
        slug=produit_slug,
        disponible=True
    )

    if request.method == 'POST':
        try:
            note = int(request.POST.get('note', 0))
        except ValueError:
            messages.error(request, 'Note invalide.')
            return redirect('detail_produit', slug=produit_slug)

        commentaire = request.POST.get('commentaire', '').strip()

        if not (1 <= note <= 5):
            messages.error(request, 'Note invalide.')
            return redirect('detail_produit', slug=produit_slug)

        if not commentaire:
            messages.error(request, 'Le commentaire est requis.')
            return redirect('detail_produit', slug=produit_slug)

        avis, created = Avis.objects.get_or_create(
            produit=produit,
            auteur=request.user,
            defaults={
                'note': note,
                'commentaire': commentaire
            }
        )

        if not created:
            avis.note = note
            avis.commentaire = commentaire
            avis.save()
            messages.success(request, 'Avis mis à jour.')
        else:
            messages.success(request, 'Avis ajouté avec succès.')

    return redirect('detail_produit', slug=produit_slug)


@login_required
@require_POST
def supprimer_avis(request, avis_id):
    avis = get_object_or_404(
        Avis,
        id=avis_id,
        auteur=request.user
    )

    slug = avis.produit.slug
    avis.delete()

    messages.info(request, 'Avis supprimé.')
    return redirect('detail_produit', slug=slug)