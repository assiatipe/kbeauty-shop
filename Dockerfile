FROM python:3.12-slim

# Empêcher Python de créer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Afficher les logs directement dans Docker
ENV PYTHONUNBUFFERED=1

# Dossier de travail dans le conteneur
WORKDIR /app

# Dépendances système nécessaires à mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier les dépendances Python
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY . .

# Copier et rendre exécutable le script de démarrage
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Port utilisé par Django
EXPOSE 8041

# Script lancé au démarrage du conteneur
ENTRYPOINT ["/entrypoint.sh"]

# Commande par défaut : version atelier avec runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8041"]