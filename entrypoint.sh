#!/bin/sh

echo "Démarrage de l'application Django..."

echo "Application des migrations..."
python manage.py migrate --noinput

echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "Lancement de l'application..."
exec "$@"
