# Easy Work — Backend

API REST Django pour la plateforme Easy Work (édition d'images par IA).

## Stack

- Python 3.12, Django 6, Django REST Framework
- PostgreSQL
- JWT (djangorestframework-simplejwt) pour l'authentification
- rembg (modèle U²-Net allégé, open source) pour la suppression d'arrière-plan

## Démarrage local (sans Docker)

Prérequis : PostgreSQL qui tourne en local, avec une base et un utilisateur créés :

```bash
sudo -u postgres psql -c "CREATE USER easywork WITH PASSWORD 'easywork' CREATEDB;"
sudo -u postgres psql -c "CREATE DATABASE easywork OWNER easywork;"
```

```bash
python3 -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # ajuster si besoin

python manage.py migrate
python manage.py createsuperuser  # optionnel, pour /admin/
python manage.py runserver
```

L'API tourne sur `http://localhost:8000/`.

## Démarrage avec Docker

```bash
cp .env.example .env
cd docker
docker compose up --build
```

## Structure

```
config/                  # Réglages Django, urls racine
users/                    # Compte utilisateur (email + mot de passe), JWT
credits_app/               # Solde de crédits (10 offerts à l'inscription)
images_app/                 # Galerie "Mes images"
processing/                # Historique des traitements + endpoint IA
favorites/                # Favoris
ai/
└── background_removal/    # Service IA — découplé du reste du backend,
                            # pour pouvoir changer/ajouter des modèles
                            # facilement (cf. cahier des charges S22)
```

## Endpoints

| Méthode | URL | Description |
|---|---|---|
| POST | `/api/users/register/` | Inscription (nom, email, password, password2) |
| POST | `/api/users/login/` | Connexion — renvoie `access` + `refresh` (JWT) |
| POST | `/api/users/login/refresh/` | Rafraîchir le token d'accès |
| GET/PATCH | `/api/users/me/` | Profil de l'utilisateur connecté |
| GET | `/api/credits/me/` | Solde de crédits |
| GET | `/api/images/` | Galerie "Mes images" |
| GET | `/api/images/{id}/` | Détail d'une image |
| DELETE | `/api/images/{id}/` | Supprimer une image |
| POST | `/api/processing/background-removal/` | Upload + suppression d'arrière-plan (multipart, champ `fichier`) |
| GET | `/api/processing/historique/` | Historique des traitements |
| GET/POST | `/api/favorites/` | Lister / ajouter un favori (`{"image": <id>}`) |
| DELETE | `/api/favorites/{id}/` | Retirer un favori |

Toutes les routes (hors `register` et `login`) nécessitent l'en-tête :
`Authorization: Bearer <access_token>`.

## Statut

Testé de bout en bout : inscription → connexion → upload d'image → suppression
d'arrière-plan réelle (rembg) → décrément du crédit → historique → favoris.
Le modèle `u2netp` (~4,5 Mo) est téléchargé automatiquement au premier appel
et mis en cache localement.

À venir : les autres outils IA (S7 à S12 du cahier des charges), la
pagination, les tests automatisés (Phase 7).
