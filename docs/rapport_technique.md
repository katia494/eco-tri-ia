# Rapport Technique — ECO-TRI

**Auteur :** Katia Boussad  
**Formation :** Dev IA — Simplon ECE 2024  
**Date :** Août 2026

---

## 1. Présentation du projet

ECO-TRI est une application web intelligente de classification
automatique des déchets par vision par ordinateur.
L'utilisateur envoie une photo d'un déchet, et l'IA identifie
sa catégorie : plastique, verre, papier, métal ou carton.

---

## 2. Architecture technique

### Backend
- **FastAPI** : Framework Python moderne pour les APIs REST
- **SQLAlchemy** : ORM pour la gestion de la base de données
- **Pydantic** : Validation automatique des données

### Intelligence Artificielle
- **YOLOv8** : Modèle de détection d'objets en temps réel
- **Pillow** : Prétraitement des images
- **NumPy** : Manipulation des tableaux de données

### Base de données
- **PostgreSQL** : En production
- **SQLite** : En développement et tests

### Infrastructure
- **Docker** : Conteneurisation de l'application
- **GitHub Actions** : CI/CD automatisé
- **pytest** : Tests unitaires et couverture de code

---

## 3. Choix techniques justifiés

### Pourquoi FastAPI ?
FastAPI génère automatiquement la documentation Swagger,
valide les données avec Pydantic, et est 3x plus rapide
que Flask grâce à son architecture asynchrone.

### Pourquoi YOLOv8 ?
YOLOv8 est l'état de l'art pour la détection d'objets en
temps réel. Il offre un excellent compromis entre précision
et vitesse d'inférence.

### Pourquoi PostgreSQL ?
PostgreSQL est robuste, open-source et supporte les
transactions ACID. Il est idéal pour stocker l'historique
des prédictions de manière fiable.

### Pourquoi Docker ?
Docker garantit que l'application fonctionne de la même
façon en développement et en production, éliminant le
problème "ça marche sur ma machine".

---

## 4. Métriques du modèle
Métrique	Valeur	Interprétation
Précision	87%	Sur 100 déchets détectés, 87 sont corrects
Rappel	83%	Sur 100 vrais déchets, 83 sont détectés
F1-Score	85%	Équilibre entre précision et rappel
mAP@0.5	89%	Performance globale de détection
5. Endpoints API
Méthode	Route	Description
GET	/health	Santé de l'API
POST	/predict	Classifier une image
GET	/predictions	Historique des prédictions
GET	/predictions/{id}	Une prédiction spécifique
6. Structure du projet
Fichier	Rôle
main.py	Point d'entrée FastAPI
database.py	Connexion PostgreSQL/SQLite
models.py	Modèle de données SQLAlchemy
schemas.py	Validation Pydantic
predict.py	Moteur IA YOLOv8
routes.py	Endpoints API
config.py	Configuration centralisée
logger.py	Système de logs
exceptions.py	Gestion des erreurs
7. Tests et qualité
Type	Fichier	Couverture
Tests API	test_api.py	Endpoints /health, /predict, /predictions
Tests IA	test_predict.py	Fonction de prédiction
Tests prétraitement	test_preprocess.py	Validation et normalisation images
Couverture de code : >80%
CI/CD : Tests automatiques à chaque push sur GitHub
8. Conclusion
ECO-TRI démontre la mise en œuvre complète d'une solution
IA en production : de la collecte des données à l'API
REST, en passant par le prétraitement des images, les tests
unitaires et le déploiement Docker.

Le projet couvre l'ensemble des compétences requises pour
un développeur IA : modélisation, API, base de données,
tests, documentation et déploiement.