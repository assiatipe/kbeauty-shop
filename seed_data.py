import os
import django
from decimal import Decimal
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kbeauty_shop.settings")
django.setup()

from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings

from products.models import Categorie, Produit


# ============================
# CATÉGORIES
# ============================

CATEGORIES = [
    {
        "nom": "Essences & Toners",
        "description": "Essences, lotions et toners coréens pour hydrater, équilibrer et préparer la peau.",
    },
    {
        "nom": "Sérums & Ampoules",
        "description": "Soins concentrés pour cibler l’acné, les taches, l’éclat, les pores et l’hydratation.",
    },
    {
        "nom": "Crèmes Hydratantes",
        "description": "Crèmes et gels hydratants pour renforcer la barrière cutanée.",
    },
    {
        "nom": "Nettoyants",
        "description": "Nettoyants doux, baumes et mousses pour une routine K-Beauty efficace.",
    },
    {
        "nom": "Masques Sheet",
        "description": "Masques en tissu hydratants, apaisants et éclat.",
    },
    {
        "nom": "Protection Solaire",
        "description": "SPF coréens légers, confortables et adaptés à un usage quotidien.",
    },
    {
        "nom": "Contour des Yeux",
        "description": "Soins spécifiques pour le contour des yeux, poches et ridules.",
    },
    {
        "nom": "Exfoliants",
        "description": "Exfoliants AHA, BHA, PHA et peelings doux pour lisser le grain de peau.",
    },
]


# ============================
# PRODUITS
# image = nom du fichier à mettre dans media/products/
# Exemple : media/products/haruharu-black-rice-toner.jpg
# ============================

PRODUITS = [
    {
        "nom": "Haruharu Wonder Black Rice Hyaluronic Toner",
        "categorie": "Essences & Toners",
        "marque": "Haruharu Wonder",
        "prix": "199.00",
        "stock": 18,
        "contenance": "150 ml",
        "type_peau": "Tous types de peau, peau déshydratée, peau terne",
        "ingredients": "Black rice extract, hyaluronic acid, beta-glucan, ginseng root extract",
        "description": "Toner hydratant à base de riz noir fermenté et d’acide hyaluronique. Il aide à repulper la peau, améliorer l’éclat et préparer la peau aux soins suivants.",
        "image": "haruharu-black-rice-toner.jpg",
    },
    {
        "nom": "Anua Heartleaf 77% Soothing Toner",
        "categorie": "Essences & Toners",
        "marque": "Anua",
        "prix": "189.00",
        "stock": 22,
        "contenance": "250 ml",
        "type_peau": "Peau sensible, peau réactive, peau mixte",
        "ingredients": "Heartleaf extract, houttuynia cordata extract, panthenol",
        "description": "Toner apaisant formulé avec 77% d’extrait de Heartleaf. Il calme les rougeurs, hydrate légèrement et convient aux peaux sensibles.",
        "image": "anua-heartleaf-toner.jpg",
    },
    {
        "nom": "COSRX Advanced Snail 96 Mucin Power Essence",
        "categorie": "Essences & Toners",
        "marque": "COSRX",
        "prix": "219.00",
        "stock": 25,
        "contenance": "100 ml",
        "type_peau": "Peau déshydratée, peau abîmée, peau à cicatrices",
        "ingredients": "Snail secretion filtrate, sodium hyaluronate, allantoin, panthenol",
        "description": "Essence culte à la mucine d’escargot. Elle hydrate, aide à réparer la barrière cutanée et améliore l’apparence des marques post-acné.",
        "image": "cosrx-snail-96-essence.jpg",
    },
    {
        "nom": "I'm From Rice Toner",
        "categorie": "Essences & Toners",
        "marque": "I'm From",
        "prix": "239.00",
        "stock": 14,
        "contenance": "150 ml",
        "type_peau": "Peau terne, peau sèche, peau normale",
        "ingredients": "Rice extract, niacinamide, adenosine",
        "description": "Toner au riz qui aide à illuminer le teint, hydrater et donner un fini doux et lumineux à la peau.",
        "image": "im-from-rice-toner.jpg",
    },

    {
        "nom": "Anua Peach 70 Niacin Serum",
        "categorie": "Sérums & Ampoules",
        "marque": "Anua",
        "prix": "249.00",
        "stock": 17,
        "contenance": "30 ml",
        "type_peau": "Peau terne, taches, pores visibles",
        "ingredients": "Peach extract, niacinamide, vitamin B12, hyaluronic acid",
        "description": "Sérum éclat à la pêche et à la niacinamide. Il aide à améliorer la luminosité du teint, lisser la texture et réduire l’apparence des pores.",
        "image": "anua-peach-70-niacin-serum.jpg",
    },
    {
        "nom": "SKIN1004 Madagascar Centella Ampoule",
        "categorie": "Sérums & Ampoules",
        "marque": "SKIN1004",
        "prix": "199.00",
        "stock": 20,
        "contenance": "55 ml",
        "type_peau": "Peau sensible, rougeurs, peau acnéique",
        "ingredients": "Centella asiatica extract",
        "description": "Ampoule minimaliste à la centella asiatica de Madagascar. Elle apaise la peau, réduit les sensations d’inconfort et soutient la barrière cutanée.",
        "image": "skin1004-centella-ampoule.jpg",
    },
    {
        "nom": "Beauty of Joseon Glow Serum Propolis + Niacinamide",
        "categorie": "Sérums & Ampoules",
        "marque": "Beauty of Joseon",
        "prix": "209.00",
        "stock": 16,
        "contenance": "30 ml",
        "type_peau": "Peau à imperfections, peau terne, peau mixte",
        "ingredients": "Propolis extract, niacinamide, turmeric root extract",
        "description": "Sérum glow à la propolis et niacinamide. Il aide à calmer les imperfections, illuminer le teint et donner un aspect plus sain à la peau.",
        "image": "beauty-of-joseon-glow-serum.jpg",
    },
    {
        "nom": "COSRX The Vitamin C 23 Serum",
        "categorie": "Sérums & Ampoules",
        "marque": "COSRX",
        "prix": "249.00",
        "stock": 10,
        "contenance": "20 g",
        "type_peau": "Taches, teint terne, irrégularités",
        "ingredients": "Ascorbic acid, tocopherol, allantoin, sodium hyaluronate",
        "description": "Sérum concentré en vitamine C pour aider à améliorer l’éclat, atténuer les taches et uniformiser le teint.",
        "image": "cosrx-vitamin-c-23-serum.jpg",
    },
    {
        "nom": "Some By Mi Yuja Niacin 30 Days Blemish Care Serum",
        "categorie": "Sérums & Ampoules",
        "marque": "Some By Mi",
        "prix": "229.00",
        "stock": 13,
        "contenance": "50 ml",
        "type_peau": "Taches, teint terne, hyperpigmentation",
        "ingredients": "Yuja extract, niacinamide, glutathione, arbutin",
        "description": "Sérum éclat au yuja et à la niacinamide. Il aide à améliorer l’uniformité du teint et l’apparence des taches.",
        "image": "some-by-mi-yuja-niacin-serum.jpg",
    },

    {
        "nom": "Beauty of Joseon Dynasty Cream",
        "categorie": "Crèmes Hydratantes",
        "marque": "Beauty of Joseon",
        "prix": "249.00",
        "stock": 19,
        "contenance": "50 ml",
        "type_peau": "Peau sèche, peau normale, peau terne",
        "ingredients": "Rice bran water, ginseng root water, squalane, niacinamide",
        "description": "Crème hydratante riche et confortable inspirée des soins traditionnels coréens. Elle nourrit, adoucit et donne un bel éclat naturel.",
        "image": "beauty-of-joseon-dynasty-cream.jpg",
    },
    {
        "nom": "Torriden DIVE-IN Soothing Cream",
        "categorie": "Crèmes Hydratantes",
        "marque": "Torriden",
        "prix": "199.00",
        "stock": 15,
        "contenance": "100 ml",
        "type_peau": "Peau déshydratée, peau sensible, peau mixte",
        "ingredients": "Low molecular hyaluronic acid, panthenol, allantoin",
        "description": "Crème-gel hydratante légère à l’acide hyaluronique. Elle apporte une hydratation fraîche sans effet gras.",
        "image": "torriden-dive-in-cream.jpg",
    },
    {
        "nom": "Dr. Jart+ Cicapair Tiger Grass Cream",
        "categorie": "Crèmes Hydratantes",
        "marque": "Dr. Jart+",
        "prix": "329.00",
        "stock": 8,
        "contenance": "50 ml",
        "type_peau": "Peau sensible, rougeurs, peau fragilisée",
        "ingredients": "Centella asiatica, madecassoside, herbs complex",
        "description": "Crème réparatrice inspirée de la centella asiatica. Elle aide à calmer les rougeurs et renforcer les peaux fragilisées.",
        "image": "dr-jart-cicapair-cream.jpg",
    },
    {
        "nom": "Illiyoon Ceramide Ato Concentrate Cream",
        "categorie": "Crèmes Hydratantes",
        "marque": "Illiyoon",
        "prix": "189.00",
        "stock": 20,
        "contenance": "200 ml",
        "type_peau": "Peau sèche, peau sensible, barrière cutanée abîmée",
        "ingredients": "Ceramide NP, cholesterol, fatty acids",
        "description": "Crème aux céramides pour nourrir intensément et soutenir la barrière cutanée. Idéale pour les peaux sèches et sensibles.",
        "image": "illiyoon-ceramide-ato-cream.jpg",
    },

    {
        "nom": "COSRX Low pH Good Morning Gel Cleanser",
        "categorie": "Nettoyants",
        "marque": "COSRX",
        "prix": "159.00",
        "stock": 30,
        "contenance": "150 ml",
        "type_peau": "Peau mixte, peau grasse, peau acnéique",
        "ingredients": "Tea tree leaf oil, betaine salicylate, allantoin",
        "description": "Nettoyant doux au pH bas, idéal le matin ou le soir. Il nettoie sans décaper et aide les peaux sujettes aux imperfections.",
        "image": "cosrx-low-ph-cleanser.jpg",
    },
    {
        "nom": "Round Lab 1025 Dokdo Cleanser",
        "categorie": "Nettoyants",
        "marque": "Round Lab",
        "prix": "139.00",
        "stock": 26,
        "contenance": "150 ml",
        "type_peau": "Tous types de peau, peau sensible",
        "ingredients": "Deep sea water, panthenol, allantoin",
        "description": "Nettoyant mousse doux enrichi en eau profonde. Il nettoie efficacement tout en respectant l’équilibre de la peau.",
        "image": "round-lab-dokdo-cleanser.jpg",
    },
    {
        "nom": "Heimish All Clean Balm",
        "categorie": "Nettoyants",
        "marque": "Heimish",
        "prix": "179.00",
        "stock": 18,
        "contenance": "120 ml",
        "type_peau": "Tous types de peau, maquillage, double nettoyage",
        "ingredients": "Shea butter, coconut extract, citrus herb oil",
        "description": "Baume démaquillant fondant pour retirer maquillage, SPF et impuretés. Première étape parfaite du double nettoyage coréen.",
        "image": "heimish-all-clean-balm.jpg",
    },
    {
        "nom": "Banila Co Clean It Zero Cleansing Balm Original",
        "categorie": "Nettoyants",
        "marque": "Banila Co",
        "prix": "199.00",
        "stock": 14,
        "contenance": "100 ml",
        "type_peau": "Tous types de peau, double nettoyage",
        "ingredients": "Acerola extract, vitamin C derivative, botanical oils",
        "description": "Baume nettoyant iconique qui dissout le maquillage et les filtres solaires. Texture sorbet très agréable.",
        "image": "banila-clean-it-zero.jpg",
    },

    {
        "nom": "Mediheal Tea Tree Essential Mask",
        "categorie": "Masques Sheet",
        "marque": "Mediheal",
        "prix": "29.00",
        "stock": 60,
        "contenance": "1 masque",
        "type_peau": "Peau grasse, peau à imperfections",
        "ingredients": "Tea tree extract, centella asiatica, chamomile extract",
        "description": "Masque sheet apaisant au tea tree. Il aide à calmer les imperfections et rafraîchir la peau.",
        "image": "mediheal-tea-tree-mask.jpg",
    },
    {
        "nom": "Mediheal N.M.F Aquaring Ampoule Mask",
        "categorie": "Masques Sheet",
        "marque": "Mediheal",
        "prix": "35.00",
        "stock": 55,
        "contenance": "1 masque",
        "type_peau": "Peau sèche, peau déshydratée",
        "ingredients": "NMF complex, hyaluronic acid, ceramide",
        "description": "Masque hydratant très populaire pour repulper la peau et apporter un effet frais immédiat.",
        "image": "mediheal-nmf-mask.jpg",
    },
    {
        "nom": "Dr. Jart+ Dermask Water Jet Vital Hydra Solution",
        "categorie": "Masques Sheet",
        "marque": "Dr. Jart+",
        "prix": "49.00",
        "stock": 35,
        "contenance": "1 masque",
        "type_peau": "Peau sèche, peau terne, peau déshydratée",
        "ingredients": "Hyaluronic acid, xylitol, algae extract",
        "description": "Masque intensément hydratant pour redonner confort, souplesse et éclat aux peaux déshydratées.",
        "image": "dr-jart-hydra-mask.jpg",
    },

    {
        "nom": "Beauty of Joseon Relief Sun Rice + Probiotics SPF50+",
        "categorie": "Protection Solaire",
        "marque": "Beauty of Joseon",
        "prix": "189.00",
        "stock": 28,
        "contenance": "50 ml",
        "type_peau": "Tous types de peau, peau sensible",
        "ingredients": "Rice extract, probiotics, niacinamide, UV filters",
        "description": "Crème solaire légère SPF50+ à la texture confortable. Elle ne laisse pas de fini lourd et convient à un usage quotidien.",
        "image": "beauty-of-joseon-relief-sun.jpg",
    },
    {
        "nom": "SKIN1004 Madagascar Centella Hyalu-Cica Water-Fit Sun Serum SPF50+",
        "categorie": "Protection Solaire",
        "marque": "SKIN1004",
        "prix": "199.00",
        "stock": 24,
        "contenance": "50 ml",
        "type_peau": "Peau sensible, peau déshydratée",
        "ingredients": "Centella asiatica, hyaluronic acid, chemical UV filters",
        "description": "Sunscreen-sérum léger avec centella et acide hyaluronique. Texture fraîche et fini naturel.",
        "image": "skin1004-hyalu-cica-sun-serum.jpg",
    },
    {
        "nom": "Isntree Hyaluronic Acid Watery Sun Gel SPF50+",
        "categorie": "Protection Solaire",
        "marque": "Isntree",
        "prix": "185.00",
        "stock": 20,
        "contenance": "50 ml",
        "type_peau": "Peau sèche, peau normale, peau déshydratée",
        "ingredients": "Hyaluronic acid, ceramide, centella asiatica, UV filters",
        "description": "Protection solaire hydratante avec texture gel aqueuse. Elle laisse un fini lumineux et confortable.",
        "image": "isntree-watery-sun-gel.jpg",
    },
    {
        "nom": "Round Lab Birch Juice Moisturizing Sunscreen SPF50+",
        "categorie": "Protection Solaire",
        "marque": "Round Lab",
        "prix": "199.00",
        "stock": 18,
        "contenance": "50 ml",
        "type_peau": "Peau normale, peau sèche, peau sensible",
        "ingredients": "Birch juice, hyaluronic acid, niacinamide, UV filters",
        "description": "Solaire hydratant au jus de bouleau, apprécié pour sa texture confortable et son fini naturel.",
        "image": "round-lab-birch-sunscreen.jpg",
    },

    {
        "nom": "Beauty of Joseon Revive Eye Serum Ginseng + Retinal",
        "categorie": "Contour des Yeux",
        "marque": "Beauty of Joseon",
        "prix": "199.00",
        "stock": 16,
        "contenance": "30 ml",
        "type_peau": "Ridules, contour des yeux terne, perte de fermeté",
        "ingredients": "Ginseng root extract, retinal, niacinamide",
        "description": "Sérum contour des yeux au ginseng et retinal. Il aide à améliorer l’apparence des ridules et du regard fatigué.",
        "image": "beauty-of-joseon-eye-serum.jpg",
    },
    {
        "nom": "Mizon Snail Repair Eye Cream",
        "categorie": "Contour des Yeux",
        "marque": "Mizon",
        "prix": "159.00",
        "stock": 12,
        "contenance": "25 ml",
        "type_peau": "Ridules, sécheresse, contour des yeux sensible",
        "ingredients": "Snail secretion filtrate, peptides, adenosine",
        "description": "Crème contour des yeux à la mucine d’escargot. Elle hydrate, adoucit et aide à lisser les ridules.",
        "image": "mizon-snail-eye-cream.jpg",
    },
    {
        "nom": "Benton Fermentation Eye Cream",
        "categorie": "Contour des Yeux",
        "marque": "Benton",
        "prix": "179.00",
        "stock": 11,
        "contenance": "30 g",
        "type_peau": "Contour des yeux fatigué, peau mature",
        "ingredients": "Galactomyces ferment filtrate, bifida ferment lysate, peptides",
        "description": "Soin contour des yeux aux ferments et peptides pour hydrater et améliorer l’apparence du regard.",
        "image": "benton-fermentation-eye-cream.jpg",
    },

    {
        "nom": "Some By Mi AHA BHA PHA 30 Days Miracle Toner",
        "categorie": "Exfoliants",
        "marque": "Some By Mi",
        "prix": "199.00",
        "stock": 18,
        "contenance": "150 ml",
        "type_peau": "Peau grasse, pores, imperfections",
        "ingredients": "AHA, BHA, PHA, tea tree extract, niacinamide",
        "description": "Toner exfoliant doux aux AHA, BHA et PHA. Il aide à lisser la peau, désobstruer les pores et améliorer les imperfections.",
        "image": "some-by-mi-miracle-toner.jpg",
    },
    {
        "nom": "COSRX BHA Blackhead Power Liquid",
        "categorie": "Exfoliants",
        "marque": "COSRX",
        "prix": "219.00",
        "stock": 13,
        "contenance": "100 ml",
        "type_peau": "Points noirs, pores, peau grasse",
        "ingredients": "Betaine salicylate, willow bark water, niacinamide",
        "description": "Exfoliant BHA liquide pour aider à réduire les points noirs et affiner l’apparence des pores.",
        "image": "cosrx-bha-blackhead-liquid.jpg",
    },
    {
        "nom": "Isntree Chestnut AHA 8% Clear Essence",
        "categorie": "Exfoliants",
        "marque": "Isntree",
        "prix": "199.00",
        "stock": 9,
        "contenance": "100 ml",
        "type_peau": "Texture irrégulière, teint terne, peau normale",
        "ingredients": "Glycolic acid, lactic acid, chestnut shell extract",
        "description": "Essence exfoliante AHA pour lisser le grain de peau et améliorer l’éclat du teint.",
        "image": "isntree-chestnut-aha-essence.jpg",
    },
    {
        "nom": "Beauty of Joseon Apricot Blossom Peeling Gel",
        "categorie": "Exfoliants",
        "marque": "Beauty of Joseon",
        "prix": "169.00",
        "stock": 15,
        "contenance": "100 ml",
        "type_peau": "Peau terne, peau sensible, exfoliation douce",
        "ingredients": "Apricot blossom extract, cellulose, green tea extract",
        "description": "Gel peeling doux à l’abricot pour retirer les cellules mortes sans agresser la peau.",
        "image": "beauty-of-joseon-peeling-gel.jpg",
    },
]


def image_exists(filename):
    if not filename:
        return False

    image_path = Path(settings.MEDIA_ROOT) / "products" / filename
    return image_path.exists()


def create_categories():
    categories_dict = {}

    for data in CATEGORIES:
        slug = slugify(data["nom"])

        categorie, created = Categorie.objects.update_or_create(
            slug=slug,
            defaults={
                "nom": data["nom"],
                "description": data["description"],
            }
        )

        categories_dict[data["nom"]] = categorie

        if created:
            print(f"Catégorie créée : {categorie.nom}")
        else:
            print(f"Catégorie mise à jour : {categorie.nom}")

    return categories_dict


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

        produit, created = Produit.objects.update_or_create(
            slug=slug,
            defaults=defaults
        )

        if created:
            print(f"Produit créé : {produit.nom}")
        else:
            print(f"Produit mis à jour : {produit.nom}")


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
        print("Superuser créé : admin / GlowAdmin123!")
    else:
        print("Superuser admin existe déjà.")

    demo_username = "demo"
    demo_password = "GlowDemo123!"

    if not User.objects.filter(username=demo_username).exists():
        User.objects.create_user(
            username=demo_username,
            email="demo@glowkr.ma",
            password=demo_password,
            first_name="Client",
            last_name="Demo"
        )
        print("Client demo créé : demo / GlowDemo123!")
    else:
        print("Client demo existe déjà.")


def main():
    print("Initialisation des données Glow.kr...")
    print("----------------------------------------")

    categories_dict = create_categories()
    create_products(categories_dict)
    create_demo_users()

    print("----------------------------------------")
    print("Données de démonstration créées avec succès.")
    print("")
    print("Comptes de test :")
    print("Admin : admin / GlowAdmin123!")
    print("Client : demo / GlowDemo123!")
    print("")
    print("Images produits :")
    print("Pour afficher les vraies images, place les fichiers dans :")
    print("media/products/")
    print("avec les noms indiqués dans la clé image de chaque produit.")


if __name__ == "__main__":
    main()