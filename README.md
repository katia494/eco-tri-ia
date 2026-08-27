\# 🌿 ECO-TRI — Système de tri des déchets par IA



\## Description

ECO-TRI est une application web intelligente qui permet de classifier

automatiquement les déchets à partir d'images, en utilisant YOLOv8

(détection d'objets) et une API FastAPI connectée à une base PostgreSQL.



\## Architecture

\- \*\*Backend\*\* : FastAPI (Python)

\- \*\*IA\*\* : YOLOv8 (Ultralytics)

\- \*\*Base de données\*\* : PostgreSQL + SQLAlchemy

\- \*\*Frontend\*\* : React/Vite (groupe)

\- \*\*Tests\*\* : pytest + pytest-cov

\- \*\*CI/CD\*\* : GitHub Actions



\## Installation



\### 1. Cloner le repo

git clone https://github.com/katia494/eco-tri-ia.git

cd eco-tri-ia



\### 2. Créer l'environnement virtuel

python -m venv venv

venv\\Scripts\\activate



\### 3. Installer les dépendances

pip install -r requirements.txt



\### 4. Configurer les variables d'environnement

cp .env.example .env



\### 5. Lancer l'API

uvicorn backend.api.main:app --reload



\## Endpoints API

