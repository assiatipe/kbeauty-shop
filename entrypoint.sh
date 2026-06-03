#!/bin/sh

echo "Démarrage de l'application Django..."

echo "Application des migrations..."
python manage.py migrate --noinput

echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "Copie automatique des images produits..."
mkdir -p /app/media/products
if [ -d "/app/static/seed_images/products" ]; then
  cp -n /app/static/seed_images/products/* /app/media/products/ 2>/dev/null || true
fi

echo "Ajout automatique des catégories et produits..."
python seed_data.py || true

echo "Création du superutilisateur admin..."
python manage.py shell <<'ADMINEOF'
from django.contrib.auth.models import User
user, created = User.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@glowkr.com', 'first_name': 'Admin', 'last_name': 'Glow.kr'}
)
user.set_password('admin123')
user.is_staff = True
user.is_superuser = True
user.save()
print("Superuser 'admin' créé." if created else "Superuser 'admin' mis à jour.")
ADMINEOF

echo "Attribution automatique des images aux produits..."
python manage.py shell <<'PYEOF'
from pathlib import Path
from products.models import Produit

media_dir = Path("/app/media/products")
images = sorted([
    p.name for p in media_dir.iterdir()
    if p.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
]) if media_dir.exists() else []

produits = list(Produit.objects.all().order_by("id"))

if not images:
    print("Aucune image trouvée dans /app/media/products")
else:
    for i, produit in enumerate(produits):
        if not produit.image:
            matched_img = None
            slug = produit.slug.lower()
            for img in images:
                img_normalized = img.lower().replace("_", "-").replace(" ", "-")
                if slug in img_normalized or img_normalized.startswith(slug):
                    matched_img = img
                    break
            if not matched_img:
                matched_img = images[i % len(images)]
            produit.image = f"products/{matched_img}"
            produit.save()
    print(f"{len(images)} images disponibles.")
    print(f"{Produit.objects.exclude(image='').count()} produits ont une image.")

print("Nombre total de produits =", Produit.objects.count())
PYEOF

echo "Lancement de l'application..."
exec "$@"
