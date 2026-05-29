import os
import django
from decimal import Decimal
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kbeauty_shop.settings")
django.setup()

from django.contrib.auth.models import User
from django.utils.text import slugify
from products.models import Categorie, Produit

# =========================================================
# Définition des catégories
# =========================================================
CATEGORIES = [
    {"nom": "Essences & Toners", "description": "Essences, lotions et toners coréens."},
    {"nom": "Sérums & Ampoules", "description": "Sérums concentrés pour la peau."},
    {"nom": "Crèmes Hydratantes", "description": "Crèmes et gels hydratants."},
    {"nom": "Nettoyants", "description": "Nettoyants doux, baumes et mousses."},
    {"nom": "Masques Sheet", "description": "Masques en tissu hydratants et apaisants."},
    {"nom": "Protection Solaire", "description": "SPF coréens légers."},
    {"nom": "Contour des Yeux", "description": "Soins pour le contour des yeux."},
    {"nom": "Exfoliants", "description": "Exfoliants doux pour lisser la peau."},
]

# =========================================================
# Définition des produits
# Les images doivent être dans media/products/
# =========================================================
PRODUITS = [
    {"nom": "Haruharu Wonder Black Rice Hyaluronic Toner", "categorie": "Essences & Toners",
     "marque": "Haruharu Wonder", "prix": "199.00", "stock": 18, "contenance": "150 ml",
     "type_peau": "Tous types", "ingredients": "Black rice extract, hyaluronic acid",
     "description": "Toner hydratant à base de riz noir fermenté.", "image": "Anua_Heartleaf_77_Soothing_Toner.jpg"},

    {"nom": "Anua Peach 70 Niacin Serum", "categorie": "Sérums & Ampoules",
     "marque": "Anua", "prix": "249.00", "stock": 17, "contenance": "30 ml",
     "type_peau": "Peau terne, taches", "ingredients": "Peach extract, niacinamide",
     "description": "Sérum éclat à la pêche et niacinamide.", "image": "Anua_Peach_70_Niacin_Serum.webp"},

    {"nom": "Banila Co Clean It Zero Cleansing Balm Original", "categorie": "Nettoyants",
     "marque": "Banila Co", "prix": "199.00", "stock": 14, "contenance": "100 ml",
     "type_peau": "Tous types", "ingredients": "Acerola extract, vitamin C derivative",
     "description": "Baume nettoyant iconique.", "image": "Banila_Co_Clean_It_Zero_Cleansing_Balm_Original.webp"},

    {"nom": "Beauty of Joseon Dynasty Cream", "categorie": "Crèmes Hydratantes",
     "marque": "Beauty of Joseon", "prix": "249.00", "stock": 19, "contenance": "50 ml",
     "type_peau": "Peau sèche", "ingredients": "Rice bran water, ginseng root water",
     "description": "Crème hydratante inspirée des soins traditionnels coréens.", "image": "Beauty_of_Joseon_Dynasty_Cream.webp"},
]

# Fonction pour vérifier si l'image existe
def image_exists(filename):
    if not filename:
        return False
    image_path = Path("media/products") / filename
    return image_path.exists()

# Création des catégories
def create_categories():
    categories_dict = {}
    for data in CATEGORIES:
        slug = slugify(data["nom"])
        categorie, _ = Categorie.objects.update_or_create(
            slug=slug,
            defaults={"nom": data["nom"], "description": data["description"]}
        )
        categories_dict[data["nom"]] = categorie
    return categories_dict

# Création des produits
def create_products(categories_dict):
    for data in PRODUITS:
        categorie = categories_dict[data["categorie"]]
        slug = slugify(data["nom"])
        defaults = {
            "nom": data["nom"],
            "description": data["description"],
            "prix": Decimal(data["prix"]),
            "categorie": categorie,
            "quantite_stock": data["stock"],
            "disponible": True,
            "marque": data["marque"],
            "ingredients": data["ingredients"],
            "type_peau": data["type_peau"],
            "contenance": data["contenance"],
        }
        if image_exists(data["image"]):
            defaults["image"] = f"products/{data['image']}"
        Produit.objects.update_or_create(slug=slug, defaults=defaults)

# Création d’un superuser demo (si nécessaire)
def create_demo_users():
    admin_username = "admin"
    admin_password = "GlowAdmin123!"
    if not User.objects.filter(username=admin_username).exists():
        User.objects.create_superuser(
            username=admin_username,
            email="admin@glowkr.ma",
            password=admin_password,
            first_name="Admin",
            last_name="Glow"
        )

def main():
    categories_dict = create_categories()
    create_products(categories_dict)
    create_demo_users()
    print("Produits et catégories ajoutés dans Django Admin avec succès.")

if __name__ == "__main__":
    main()
