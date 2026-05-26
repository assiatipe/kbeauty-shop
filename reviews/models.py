from django.db import models
from django.contrib.auth.models import User
from products.models import Produit
from django.core.validators import MinValueValidator, MaxValueValidator


class Avis(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='avis')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avis')
    note = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    commentaire = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avis de {self.auteur.username} sur {self.produit.nom} ({self.note}/5)"

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"
        unique_together = ['produit', 'auteur']
        ordering = ['-date_creation']
