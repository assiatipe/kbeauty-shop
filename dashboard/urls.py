from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('produits/', views.liste_produits, name='liste_produits'),
    path('produits/ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('produits/modifier/<int:produit_id>/', views.modifier_produit, name='modifier_produit'),
    path('produits/supprimer/<int:produit_id>/', views.supprimer_produit, name='supprimer_produit'),
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/ajouter/', views.ajouter_categorie, name='ajouter_categorie'),
    path('categories/modifier/<int:cat_id>/', views.modifier_categorie, name='modifier_categorie'),
    path('categories/supprimer/<int:cat_id>/', views.supprimer_categorie, name='supprimer_categorie'),
    path('commandes/', views.gestion_commandes, name='gestion_commandes'),
    path('commandes/<int:commande_id>/', views.detail_commande_admin, name='detail_commande_admin'),
    path('clients/', views.gestion_clients, name='gestion_clients'),
    path('stocks/', views.gestion_stocks, name='gestion_stocks'),
]
