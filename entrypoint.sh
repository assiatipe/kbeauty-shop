#!/bin/sh

echo "Démarrage de l'application Django..."

echo "Application des migrations..."
python manage.py migrate --noinput

echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "Ajout automatique des catégories et produits..."
python seed_data.py || echo "seed_data.py non exécuté ou déjà appliqué"

echo "Lancement de l'application..."
exec "$@"
