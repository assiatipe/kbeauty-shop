from django import forms


class CommandeForm(forms.Form):
    adresse_livraison = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Votre adresse complète'}),
        label='Adresse de livraison'
    )
    ville_livraison = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Casablanca'}),
        label='Ville'
    )
    code_postal_livraison = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '20000'}),
        label='Code postal'
    )
    pays_livraison = forms.CharField(
        initial='Maroc',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Pays'
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Instructions spéciales (optionnel)'}),
        label='Notes'
    )
