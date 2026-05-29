from django.db import models
from django.utils import timezone


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"


class Produit(models.Model):
    nom = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    quantite_stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    date_ajout = models.DateTimeField(default=timezone.now)
    marque = models.CharField(max_length=100, blank=True)
    ingredients = models.TextField(blank=True, help_text='Ingrédients du produit')
    type_peau = models.CharField(max_length=200, blank=True, help_text='Types de peau recommandés')
    contenance = models.CharField(max_length=50, blank=True, help_text='Ex: 50ml, 150ml')
    en_promotion = models.BooleanField(default=False)
    prix_promotion = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def prix_actuel(self):
        if self.en_promotion and self.prix_promotion is not None:
            return self.prix_promotion
        return self.prix

    def __str__(self):
        return self.nom

    @property
    def note_moyenne(self):
        from reviews.models import Avis
        avis = Avis.objects.filter(produit=self)
        if avis.exists():
            return round(sum(a.note for a in avis) / avis.count(), 1)
        return 0

    @property
    def nombre_avis(self):
        from reviews.models import Avis
        return Avis.objects.filter(produit=self).count()

    @property
    def en_stock(self):
        return self.quantite_stock > 0 and self.disponible

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-date_ajout']
