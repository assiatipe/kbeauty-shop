"""
Moteur de recommandation IA basé sur TF-IDF et similarité cosinus.
Utilise les descriptions, catégories, marques et types de peau pour
recommander des produits similaires.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_product_text(produit):
    """Construit un texte représentatif du produit pour le TF-IDF."""
    parts = [
        produit.nom,
        produit.description,
        produit.categorie.nom,
        produit.marque or '',
        produit.type_peau or '',
        produit.ingredients or '',
    ]
    # Répéter le nom et la catégorie pour leur donner plus de poids
    parts += [produit.nom] * 2
    parts += [produit.categorie.nom] * 2
    return ' '.join(filter(None, parts)).lower()


def get_recommendations(produit_cible, n=4):
    """
    Retourne les n produits les plus similaires au produit_cible.
    
    Algorithme :
    1. Récupération de tous les produits disponibles
    2. Construction des vecteurs TF-IDF
    3. Calcul de la similarité cosinus
    4. Tri par similarité décroissante
    5. Retour des top-n (hors produit cible)
    """
    try:
        from products.models import Produit
        tous_produits = list(Produit.objects.filter(disponible=True))

        if len(tous_produits) < 2:
            return []

        # Construire les textes
        textes = [build_product_text(p) for p in tous_produits]

        # Vectorisation TF-IDF
        vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 2),
            min_df=1,
        )
        matrice_tfidf = vectorizer.fit_transform(textes)

        # Index du produit cible
        try:
            idx_cible = tous_produits.index(produit_cible)
        except ValueError:
            return []

        # Calcul de la similarité cosinus
        vecteur_cible = matrice_tfidf[idx_cible]
        similarites = cosine_similarity(vecteur_cible, matrice_tfidf).flatten()

        # Trier par similarité (exclure le produit lui-même)
        indices_tries = np.argsort(similarites)[::-1]
        recommandes = []
        for idx in indices_tries:
            if idx != idx_cible and tous_produits[idx] != produit_cible:
                recommandes.append(tous_produits[idx])
            if len(recommandes) >= n:
                break

        return recommandes

    except Exception as e:
        # En cas d'erreur (ex: pas assez de données), retour vide
        print(f"Erreur de recommandation : {e}")
        return []
