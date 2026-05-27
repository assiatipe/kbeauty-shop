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
            produit.image = f"products/{images[i % len(images)]}"
            produit.save()
    print(f"{len(images)} images disponibles.")
    print(f"{Produit.objects.exclude(image='').count()} produits ont une image.")

print("Nombre total de produits =", Produit.objects.count())
PYEOF

echo "Lancement de l'application..."
exec "$@"
