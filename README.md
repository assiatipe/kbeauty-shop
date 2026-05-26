# Glow.kr — Plateforme E-Commerce K-Beauty

Projet de fin de module Django — Filières Ingénieurs EMI  
Thème : Skincare coréen | Design : Pastel K-Beauty

---

## Structure du projet

```
kbeauty_shop/
├── accounts/          # Gestion utilisateurs, profils
├── products/          # Produits, catégories, catalogue
├── cart/              # Panier d'achat
├── orders/            # Commandes, historique
├── dashboard/         # Tableau de bord admin
├── recommendation/    # IA : TF-IDF + similarité cosinus
├── reviews/           # Avis et notes clients
├── templates/         # Templates Django (thème pastel)
├── static/css/        # CSS custom K-Beauty
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── .github/workflows/ # CI/CD GitHub Actions
└── requirements.txt
```

---

## Installation locale (développement)

### 1. Cloner le projet
```bash
git clone https://github.com/VOTRE_USERNAME/glowkr-shop.git
cd glowkr-shop
```

### 2. Environnement virtuel
```bash
python -m venv venv
# Windows :
venv\Scripts\activate
# Linux/Mac :
source venv/bin/activate
```

### 3. Dépendances
```bash
pip install -r requirements.txt
```

### 4. Variables d'environnement
```bash
cp .env.example .env
# Ouvrir .env et garder USE_SQLITE=True pour le dev local
```

### 5. Migrations et démarrage
```bash
python manage.py migrate
python manage.py shell < seed_data.py    # Charge les données de démo
python manage.py runserver
```

### 6. Accès
- **Boutique** : http://127.0.0.1:8000/
- **Dashboard admin** : http://127.0.0.1:8000/dashboard/
- **Admin Django** : http://127.0.0.1:8000/admin/

**Comptes de démo :**
| Utilisateur | Mot de passe | Rôle |
|-------------|-------------|------|
| admin       | GlowAdmin123! | Administrateur |
| demo        | Demo123! | Client |

---

## Lancement avec Docker Compose

```bash
# Copier et configurer .env (mettre USE_SQLITE=False)
cp .env.example .env

# Lancer tous les services (Django + PostgreSQL + Nginx)
docker-compose up --build

# En arrière-plan
docker-compose up -d --build

# Migrations (première fois)
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell < seed_data.py
```

**Accès** : http://localhost (port 80 via Nginx)

---

## Fonctionnalité IA — Recommandation de produits

**Algorithme** : TF-IDF + Similarité cosinus (scikit-learn)

**Principe** :
1. Pour chaque produit, on construit un texte représentatif (nom, description, catégorie, marque, type de peau, ingrédients)
2. Ces textes sont vectorisés avec **TF-IDF** (Term Frequency–Inverse Document Frequency)
3. La **similarité cosinus** mesure la proximité entre le produit consulté et tous les autres
4. Les N produits les plus similaires sont recommandés

**Implémentation** : `recommendation/engine.py`

---

## Tests

```bash
python manage.py test --verbosity=2
```

Tests inclus : models, vues, authentification, panier, recommandation IA

---

## CI/CD (GitHub Actions)

Pipeline automatique à chaque push sur `main` :
1. Installation Python et dépendances
2. Migrations en environnement de test
3. Exécution des tests
4. Vérification qualité (flake8)
5. Build de l'image Docker
6. Publication sur Docker Hub

**Configuration** : `.github/workflows/ci-cd.yml`

**Secrets GitHub à configurer** :
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

---

## Sécurité

- Authentification obligatoire pour commander
- Protection CSRF active
- Mots de passe hachés par Django
- Variables sensibles dans `.env` (jamais sur GitHub)
- `DEBUG=False` en production
- Validation des fichiers uploadés
- Pages admin protégées (`@staff_member_required`)
- Clients isolés de l'administration

---

## Technologies utilisées

| Composant | Technologie |
|-----------|------------|
| Backend | Django 4.2 |
| Base de données | PostgreSQL (prod) / SQLite (dev) |
| IA | scikit-learn, TF-IDF, cosine_similarity |
| Frontend | Django Templates + CSS custom + Bootstrap grid |
| Conteneurisation | Docker + Docker Compose |
| Reverse proxy | Nginx |
| Serveur WSGI | Gunicorn |
| CI/CD | GitHub Actions |

---

*Projet EMI — Développement Web avec Django — 2025-2026*
