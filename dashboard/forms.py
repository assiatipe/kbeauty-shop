from django import forms
from products.models import Produit, Categorie
from django.utils.text import slugify


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'slug', 'description', 'prix', 'categorie', 'image',
                  'quantite_stock', 'disponible', 'marque', 'ingredients', 'type_peau', 'contenance']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'slug-auto-genere'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'quantite_stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'marque': forms.TextInput(attrs={'class': 'form-control'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'type_peau': forms.TextInput(attrs={'class': 'form-control'}),
            'contenance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '50ml'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.nom)
        if commit:
            instance.save()
        return instance


class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom', 'slug', 'description', 'image']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.nom)
        if commit:
            instance.save()
        return instance
