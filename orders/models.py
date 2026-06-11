from django.db import models
from django.contrib.auth.models import User
from products.models import Produit


class Commande(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('en_preparation', 'En préparation'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]

    MODES_PAIEMENT = [
        ('livraison', 'Paiement à la livraison'),
        ('carte', 'Carte Bancaire'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commandes')
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    mode_paiement = models.CharField(max_length=20, choices=MODES_PAIEMENT, default='livraison')
    date_commande = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    adresse_livraison = models.TextField()
    ville_livraison = models.CharField(max_length=100)
    code_postal_livraison = models.CharField(max_length=10)
    pays_livraison = models.CharField(max_length=100, default='Maroc')
    notes = models.TextField(blank=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Commande #{self.id} - {self.client.username}"

    def calculer_total(self):
        self.montant_total = sum(l.sous_total for l in self.lignes.all())
        self.save()

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-date_commande']


class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True)
    nom_produit = models.CharField(max_length=200)  # snapshot au moment de la commande
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantite}x {self.nom_produit}"

    @property
    def sous_total(self):
        return self.prix_unitaire * self.quantite

    class Meta:
        verbose_name = "Ligne Commande"
        verbose_name_plural = "Lignes Commande"


class DemandeProduit(models.Model):
    STATUTS = [
        ('recue', 'Reçue'),
        ('commandee', 'Commandée sur YesStyle'),
        ('arrivee_espagne', 'Arrivée en Espagne 🇪🇸'),
        ('en_route_maroc', 'En route vers le Maroc 🇲🇦'),
        ('livree', 'Livrée au client'),
        ('annulee', 'Annulée'),
    ]

    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='demandes_produits')
    nom_produit = models.CharField(max_length=250, verbose_name="Nom / Marque du produit")
    lien_yesstyle = models.URLField(max_length=500, verbose_name="Lien YesStyle", help_text="Copiez-collez le lien du produit sur YesStyle")
    quantite = models.PositiveIntegerField(default=1, verbose_name="Quantité")
    options = models.CharField(max_length=200, blank=True, verbose_name="Teinte / Taille / Options", help_text="Ex: Teinte #21, Taille unique, etc.")
    
    nom_client = models.CharField(max_length=100, verbose_name="Votre Nom complet")
    contact_client = models.CharField(max_length=100, verbose_name="Téléphone / WhatsApp ou Email")
    notes = models.TextField(blank=True, verbose_name="Notes additionnelles")
    
    statut = models.CharField(max_length=30, choices=STATUTS, default='recue')
    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demande de {self.nom_client} - {self.nom_produit}"

    class Meta:
        verbose_name = "Demande de produit personnalisé"
        verbose_name_plural = "Demandes de produits personnalisés"
        ordering = ['-date_soumission']
