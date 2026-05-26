from django.contrib import admin
from .models import Produit, Categorie


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug']
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['nom', 'categorie', 'prix', 'quantite_stock', 'disponible', 'date_ajout']
    list_filter = ['disponible', 'categorie']
    list_editable = ['prix', 'quantite_stock', 'disponible']
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ['nom', 'description', 'marque']
    date_hierarchy = 'date_ajout'
