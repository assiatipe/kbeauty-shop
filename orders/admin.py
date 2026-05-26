from django.contrib import admin
from .models import Commande, LigneCommande


class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 0
    readonly_fields = ['sous_total']


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'statut', 'montant_total', 'date_commande']
    list_filter = ['statut', 'date_commande']
    list_editable = ['statut']
    search_fields = ['client__username', 'client__email']
    inlines = [LigneCommandeInline]
    date_hierarchy = 'date_commande'
