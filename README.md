# ECO-TRI IA

Application web de classification de déchets à partir d'une photographie.
Le frontend React envoie l'image à une API FastAPI. Un modèle **YOLOv8n-cls**
classe l'image parmi six catégories, puis l'API retourne la classe, la confiance
et une consigne de tri. L'image utilisateur n'est pas conservée.

## Résultats vérifiés

- Dataset réel : 2 527 images, 6 catégories.
- Split reproductible : 1 766 train, 377 validation, 384 test.
- Accuracy sur le jeu de test jamais vu : **91,15 %**.
- Macro F1-score sur le jeu de test : **90,47 %**.
- Modèle : YOLOv8n-cls, 1,44 million de paramètres, fichier de 2,9 Mo.
- Tests backend : 21 tests, 85 % de couverture mesurée.

Les métriques détaillées et la matrice de confusion sont disponibles dans
[`reports/model`](reports/model).

## Architecture

```text
Utilisateur -> React/Vite -> FastAPI -> YOLOv8n-cls
                              |-> SQLite (métadonnées uniquement)
                              |-> logs (statut et latence)
```

## Fonctionnalités principales

- upload ou capture d'une image JPG/PNG ;
- validation du type, du contenu et de la taille (10 Mo maximum) ;
- classification en `cardboard`, `glass`, `metal`, `paper`, `plastic`, `trash` ;
- score de confiance et consigne de tri ;
- historique et statistiques des prédictions ;
- documentation OpenAPI sur `/docs` ;
- tests automatisés backend, lint et build frontend dans GitHub Actions.

## Installation locale

Prérequis : Python 3.12 et Node.js 22.

```bash
git clone https://github.com/katia494/eco-tri-ia.git
cd eco-tri-ia
python -m venv .venv
```

Sous Windows PowerShell :

```powershell
.venv\Scripts\Activate.ps1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
copy .env.example .env
uvicorn backend.api.main:app --reload
```

Dans un second terminal :

```powershell
cd frontend
npm ci
npm run dev
```

Ouvrir `http://localhost:5173` et la documentation API sur
`http://localhost:8000/docs`.

## Vérifications

```bash
pytest tests/ -v --cov=backend --cov-report=term-missing
cd frontend
npm run lint
npm run build
```

## Préparer et entraîner le modèle

```bash
pip install -r requirements-data.txt
python scripts/download_dataset.py
python scripts/prepare_classification_dataset.py
python scripts/train_yolo_classification.py --epochs 20 --batch 64
python scripts/evaluate_model.py
```

Le split est déterministe avec la graine 42. Le modèle final doit être copié
dans `backend/models/best.pt`.

## API

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/health` | État de l'API |
| GET | `/model/info` | Modèle, tâche et classes |
| POST | `/predict` | Classification d'une image |
| GET | `/predictions` | Historique paginé simplement |
| GET | `/predictions/{id}` | Prédiction par identifiant |
| GET | `/stats/` | Statistiques globales |
| GET | `/stats/by-class` | Statistiques par classe |

## Docker

```bash
docker compose build
docker compose up -d
curl http://localhost:8000/health
```

Le conteneur utilise SQLite dans un volume persistant et fonctionne sans clé
ni mot de passe inscrit dans le dépôt.

## Confidentialité et limites

- aucune image envoyée par l'utilisateur n'est sauvegardée ;
- seules la classe, la confiance, la date et le nom du fichier sont enregistrés ;
- le modèle est limité aux six classes apprises ;
- une image contenant plusieurs objets ou un déchet très différent du dataset
  peut produire une confiance faible ou une erreur de classification ;
- la prédiction reste une aide et non une instruction municipale officielle.

## Documentation

Les choix techniques, le RGPD, la veille, le benchmark, le monitoring,
l'incident et la carte des compétences sont regroupés dans [`docs/`](docs/).

Projet repris et développé individuellement par **Katia Boussad**.
