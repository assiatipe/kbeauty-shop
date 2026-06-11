from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.contrib.auth.models import User
from products.models import Produit, Categorie
from orders.models import Commande, LigneCommande, DemandeProduit
from django.utils import timezone
from datetime import timedelta
from .forms import ProduitForm, CategorieForm


@staff_member_required
def dashboard(request):
    total_produits = Produit.objects.count()
    total_clients = User.objects.filter(is_staff=False).count()
    total_commandes = Commande.objects.count()
    chiffre_affaires = Commande.objects.filter(
        statut__in=['confirmee', 'en_preparation', 'expediee', 'livree']
    ).aggregate(total=Sum('montant_total'))['total'] or 0
    statuts_data = Commande.objects.values('statut').annotate(count=Count('id'))
    statuts = {item['statut']: item['count'] for item in statuts_data}
    produits_vendus = LigneCommande.objects.values(
        'produit__nom', 'produit__slug'
    ).annotate(total_vendu=Sum('quantite')).order_by('-total_vendu')[:5]
    commandes_recentes = Commande.objects.select_related('client').order_by('-date_commande')[:10]
    produits_rupture = Produit.objects.filter(quantite_stock=0)
    date_debut = timezone.now() - timedelta(days=30)
    revenus_recents = Commande.objects.filter(
        date_commande__gte=date_debut,
        statut__in=['confirmee', 'en_preparation', 'expediee', 'livree']
    ).aggregate(total=Sum('montant_total'))['total'] or 0
    return render(request, 'dashboard/index.html', {
        'total_produits': total_produits,
        'total_clients': total_clients,
        'total_commandes': total_commandes,
        'chiffre_affaires': chiffre_affaires,
        'statuts': statuts,
        'produits_vendus': produits_vendus,
        'commandes_recentes': commandes_recentes,
        'produits_rupture': produits_rupture,
        'revenus_recents': revenus_recents,
    })


@staff_member_required
def liste_produits(request):
    q = request.GET.get('q', '')
    cat = request.GET.get('cat', '')
    produits = Produit.objects.select_related('categorie').order_by('-date_ajout')
    if q:
        produits = produits.filter(Q(nom__icontains=q) | Q(marque__icontains=q))
    if cat:
        produits = produits.filter(categorie__slug=cat)
    categories = Categorie.objects.all()
    return render(request, 'dashboard/produits/liste.html', {
        'produits': produits, 'categories': categories, 'q': q, 'cat': cat
    })


@staff_member_required
def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save()
            messages.success(request, f'Produit "{produit.nom}" ajouté avec succès.')
            return redirect('liste_produits')
    else:
        form = ProduitForm()
    return render(request, 'dashboard/produits/form.html', {'form': form, 'titre': 'Ajouter un produit'})


@staff_member_required
def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, f'Produit "{produit.nom}" modifié.')
            return redirect('liste_produits')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'dashboard/produits/form.html', {'form': form, 'titre': 'Modifier le produit', 'produit': produit})


@staff_member_required
def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == 'POST':
        nom = produit.nom
        produit.delete()
        messages.success(request, f'Produit "{nom}" supprimé.')
        return redirect('liste_produits')
    return render(request, 'dashboard/produits/supprimer.html', {'produit': produit})


@staff_member_required
def liste_categories(request):
    categories = Categorie.objects.annotate(nb_produits=Count('produits')).order_by('nom')
    return render(request, 'dashboard/categories/liste.html', {'categories': categories})


@staff_member_required
def ajouter_categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f'Catégorie "{cat.nom}" ajoutée.')
            return redirect('liste_categories')
    else:
        form = CategorieForm()
    return render(request, 'dashboard/categories/form.html', {'form': form, 'titre': 'Ajouter une catégorie'})


@staff_member_required
def modifier_categorie(request, cat_id):
    categorie = get_object_or_404(Categorie, id=cat_id)
    if request.method == 'POST':
        form = CategorieForm(request.POST, request.FILES, instance=categorie)
        if form.is_valid():
            form.save()
            messages.success(request, f'Catégorie "{categorie.nom}" modifiée.')
            return redirect('liste_categories')
    else:
        form = CategorieForm(instance=categorie)
    return render(request, 'dashboard/categories/form.html', {'form': form, 'titre': 'Modifier la catégorie'})


@staff_member_required
def supprimer_categorie(request, cat_id):
    categorie = get_object_or_404(Categorie, id=cat_id)
    if request.method == 'POST':
        nom = categorie.nom
        categorie.delete()
        messages.success(request, f'Catégorie "{nom}" supprimée.')
        return redirect('liste_categories')
    return render(request, 'dashboard/categories/supprimer.html', {'categorie': categorie})


@staff_member_required
def gestion_commandes(request):
    statut_filtre = request.GET.get('statut', '')
    commandes = Commande.objects.select_related('client').order_by('-date_commande')
    if statut_filtre:
        commandes = commandes.filter(statut=statut_filtre)
    if request.method == 'POST':
        commande_id = request.POST.get('commande_id')
        nouveau_statut = request.POST.get('statut')
        try:
            commande = Commande.objects.get(id=commande_id)
            commande.statut = nouveau_statut
            commande.save()
            messages.success(request, f'Commande #{commande_id} mise à jour.')
        except Commande.DoesNotExist:
            pass
        return redirect('gestion_commandes')
    return render(request, 'dashboard/commandes.html', {
        'commandes': commandes,
        'statuts': Commande.STATUTS,
        'statut_filtre': statut_filtre,
    })


@staff_member_required
def detail_commande_admin(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == 'POST':
        commande.statut = request.POST.get('statut')
        commande.save()
        messages.success(request, 'Statut mis à jour.')
        return redirect('detail_commande_admin', commande_id=commande_id)
    return render(request, 'dashboard/detail_commande.html', {
        'commande': commande, 'statuts': Commande.STATUTS,
    })


@staff_member_required
def gestion_clients(request):
    q = request.GET.get('q', '')
    clients = User.objects.filter(is_staff=False).order_by('-date_joined')
    if q:
        clients = clients.filter(Q(username__icontains=q) | Q(email__icontains=q) | Q(first_name__icontains=q))
    return render(request, 'dashboard/clients.html', {'clients': clients, 'q': q})


@staff_member_required
def gestion_stocks(request):
    if request.method == 'POST':
        produit_id = request.POST.get('produit_id')
        nouvelle_quantite = request.POST.get('quantite')
        try:
            produit = Produit.objects.get(id=produit_id)
            produit.quantite_stock = int(nouvelle_quantite)
            produit.save()
            messages.success(request, f'Stock de "{produit.nom}" : {nouvelle_quantite} unités.')
        except (Produit.DoesNotExist, ValueError):
            messages.error(request, 'Erreur de mise à jour.')
        return redirect('gestion_stocks')

    produits = Produit.objects.select_related('categorie').order_by('quantite_stock')
    produits_rupture_count = produits.filter(quantite_stock=0).count()
    produits_stock_faible_count = produits.filter(quantite_stock__gt=0, quantite_stock__lt=5).count()

    return render(request, 'dashboard/stocks.html', {
        'produits': produits,
        'produits_rupture_count': produits_rupture_count,
        'produits_stock_faible_count': produits_stock_faible_count,
    })


@staff_member_required
def gestion_demandes(request):
    statut_filtre = request.GET.get('statut', '')
    demandes = DemandeProduit.objects.select_related('client').order_by('-date_soumission')
    if statut_filtre:
        demandes = demandes.filter(statut=statut_filtre)
        
    if request.method == 'POST':
        demande_id = request.POST.get('demande_id')
        nouveau_statut = request.POST.get('statut')
        try:
            demande = DemandeProduit.objects.get(id=demande_id)
            demande.statut = nouveau_statut
            demande.save()
            messages.success(request, f'Demande de {demande.nom_client} mise à jour.')
        except DemandeProduit.DoesNotExist:
            messages.error(request, 'Demande introuvable.')
        return redirect('gestion_demandes')
        
    return render(request, 'dashboard/demandes.html', {
        'demandes': demandes,
        'statuts': DemandeProduit.STATUTS,
        'statut_filtre': statut_filtre,
    })