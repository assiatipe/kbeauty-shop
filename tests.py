"""
Tests complets pour le projet Glow.kr
Couvre : models, views, authentication, cart, orders
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Produit, Categorie
from cart.models import Panier, LignePanier
from orders.models import Commande, LigneCommande
from reviews.models import Avis


class CategorieModelTest(TestCase):
    def setUp(self):
        self.categorie = Categorie.objects.create(
            nom='Sérums', slug='serums', description='Sérums K-Beauty'
        )

    def test_categorie_str(self):
        self.assertEqual(str(self.categorie), 'Sérums')

    def test_categorie_slug(self):
        self.assertEqual(self.categorie.slug, 'serums')


class ProduitModelTest(TestCase):
    def setUp(self):
        self.categorie = Categorie.objects.create(nom='Toners', slug='toners')
        self.produit = Produit.objects.create(
            nom='Toner Hydratant Cerave',
            slug='toner-hydratant-cerave',
            description='Toner doux pour peau sensible',
            prix=149.90,
            categorie=self.categorie,
            quantite_stock=10,
            disponible=True,
            marque='CeraVe'
        )

    def test_produit_str(self):
        self.assertEqual(str(self.produit), 'Toner Hydratant Cerave')

    def test_produit_en_stock(self):
        self.assertTrue(self.produit.en_stock)

    def test_produit_rupture(self):
        self.produit.quantite_stock = 0
        self.produit.save()
        self.assertFalse(self.produit.en_stock)

    def test_note_moyenne_sans_avis(self):
        self.assertEqual(self.produit.note_moyenne, 0)


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='TestPass123!',
            email='test@example.com', first_name='Assia'
        )

    def test_inscription_page(self):
        response = self.client.get(reverse('inscription'))
        self.assertEqual(response.status_code, 200)

    def test_connexion_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_connexion_valide(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser', 'password': 'TestPass123!'
        })
        self.assertEqual(response.status_code, 302)

    def test_profil_non_connecte(self):
        response = self.client.get(reverse('profil'))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profil/')


class ProductViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.categorie = Categorie.objects.create(nom='Essences', slug='essences')
        self.produit = Produit.objects.create(
            nom='Essence Snail Cosrx',
            slug='essence-snail-cosrx',
            description='Essence réparatrice au mucin d\'escargot',
            prix=289.00,
            categorie=self.categorie,
            quantite_stock=15,
            disponible=True
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_catalogue_page(self):
        response = self.client.get(reverse('catalogue'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Essence Snail Cosrx')

    def test_detail_produit(self):
        response = self.client.get(reverse('detail_produit', args=['essence-snail-cosrx']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Essence Snail Cosrx')

    def test_catalogue_recherche(self):
        response = self.client.get(reverse('catalogue'), {'q': 'Snail'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Essence Snail Cosrx')

    def test_catalogue_filtre_categorie(self):
        response = self.client.get(reverse('catalogue'), {'categorie': 'essences'})
        self.assertEqual(response.status_code, 200)


class CartTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='shopper', password='Pass123!')
        self.categorie = Categorie.objects.create(nom='Masques', slug='masques')
        self.produit = Produit.objects.create(
            nom='Sheet Mask Etude House',
            slug='sheet-mask-etude-house',
            description='Masque hydratant',
            prix=35.00,
            categorie=self.categorie,
            quantite_stock=20,
            disponible=True
        )

    def test_panier_non_connecte(self):
        response = self.client.get(reverse('voir_panier'))
        self.assertEqual(response.status_code, 302)

    def test_ajouter_au_panier(self):
        self.client.login(username='shopper', password='Pass123!')
        response = self.client.post(reverse('ajouter_au_panier', args=[self.produit.id]))
        self.assertEqual(response.status_code, 302)
        panier = Panier.objects.get(client=self.user)
        self.assertEqual(panier.lignes.count(), 1)


class RecommendationTest(TestCase):
    def setUp(self):
        self.categorie = Categorie.objects.create(nom='Crèmes', slug='cremes')
        for i in range(5):
            Produit.objects.create(
                nom=f'Crème Test {i}',
                slug=f'creme-test-{i}',
                description=f'Crème hydratante texture légère pour peau sèche produit coréen {i}',
                prix=100 + i * 10,
                categorie=self.categorie,
                quantite_stock=10,
                disponible=True
            )

    def test_recommendations_retourne_produits(self):
        from recommendation.engine import get_recommendations
        produit = Produit.objects.first()
        recommendations = get_recommendations(produit, n=3)
        self.assertIsInstance(recommendations, list)
        self.assertNotIn(produit, recommendations)
