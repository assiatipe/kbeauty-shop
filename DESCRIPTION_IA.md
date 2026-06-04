# 🧠 Description des Fonctionnalités IA — GlowKr (K-Beauty Shop)

L'application **GlowKr** (K-Beauty Shop) intègre trois types de fonctionnalités d'intelligence (générative et algorithmique) pour guider et conseiller de manière personnalisée l'utilisateur dans sa routine de cosmétiques coréens :

---

### 1. Le Chatbot Beauté Intelligent (IA Générative - LLM)
* **Technologie :** Intégration de l'API de modèle de langage (**Anthropic Claude** / **OpenAI**) via un module Python asynchrone.
* **Fonctionnement :**
  * Le chatbot agit comme un conseiller virtuel expert en soins et cosmétiques K-Beauty.
  * Il est configuré avec un *System Prompt* spécifique qui le structure pour adopter un ton chaleureux et guider ses conseils en priorité vers les marques et les produits réels disponibles dans la base de données de la boutique.
  * L'historique des requêtes est maintenu en mémoire de session Django pour assurer la continuité naturelle de la conversation.
* **Fichiers associés dans le code :** [recommendation/chatbot.py](file:///Users/assiakharbouch/Desktop/kbeauty_shop/recommendation/chatbot.py) et [recommendation/views.py](file:///Users/assiakharbouch/Desktop/kbeauty_shop/recommendation/views.py).

---

### 2. Le Diagnostic de Peau Personnalisé
* **Technologie :** Système expert de recommandation basé sur le profil cutané.
* **Fonctionnement :**
  * L'utilisateur remplit un formulaire interactif ciblant son **type de peau** (sèche, mixte, grasse, sensible) et ses **objectifs** (acné, taches, hydratation, éclat).
  * L'algorithme analyse ces réponses et effectue un filtrage croisé sur la base de données des produits pour composer et suggérer une **routine K-Beauty complète en 4 étapes** (Nettoyer, Préparer/Tonifier, Traiter/Sérum, Hydrater/Protéger) sur mesure.
* **Fichiers associés dans le code :** `diagnostic_page` dans [recommendation/views.py](file:///Users/assiakharbouch/Desktop/kbeauty_shop/recommendation/views.py).

---

### 3. Le Moteur de Recommandations Hybrides
* **Technologie :** Filtrage basé sur le contenu (*Content-Based Filtering*).
* **Fonctionnement :**
  * Intégré sur chaque fiche produit, cet algorithme suggère 4 produits complémentaires ou similaires en calculant un score d'affinité.
  * Le score prend en compte le croisement de la catégorie, des ingrédients clés, de la compatibilité des types de peaux et donne la priorité aux produits actuellement en stock.
* **Fichiers associés dans le code :** [recommendation/engine.py](file:///Users/assiakharbouch/Desktop/kbeauty_shop/recommendation/engine.py).
