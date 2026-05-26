from django.db import models
from django.contrib.auth.models import User
from products.models import Produit


class Panier(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE, related_name='panier')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Panier de {self.client.username}"

    @property
    def total(self):
        return sum(ligne.sous_total for ligne in self.lignes.all())

    @property
    def nombre_articles(self):
        return sum(ligne.quantite for ligne in self.lignes.all())

    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"


class LignePanier(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantite}x {self.produit.nom}"

    @property
    def sous_total(self):
        return self.produit.prix * self.quantite

    class Meta:
        verbose_name = "Ligne Panier"
        verbose_name_plural = "Lignes Panier"
        unique_together = ['panier', 'produit']
