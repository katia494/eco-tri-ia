# ECO-TRI IA

Application web de classification de déchets à partir d'une photographie.
Le frontend React envoie l'image à une API FastAPI. Un modèle **YOLOv8n-cls**
classe l'image parmi six catégories, puis l'API retourne la classe, la confiance
et une consigne de tri. L'image utilisateur n'est pas conservée.

## Résultats vérifiés

- Dataset brut réel : 2 527 images, 6 catégories.
- Audit qualité : 2 527 images lisibles et 3 copies mal étiquetées exclues du pipeline v2.
- Pipeline v2 : 2 524 images uniques, réparties en 1 764 train, 377 validation et 383 test.
- Métriques v2 : **91,64 %** d'accuracy et **90,48 %** de macro F1 sur le jeu de test.
- Modèle : YOLOv8n-cls, 1,44 million de paramètres, fichier d'environ 3 Mo.
- Qualité logicielle : 28 tests backend, 86 % de couverture et 3 tests métier frontend.

Les trois copies contradictoires détectées par SHA-256 ont été exclues avant le
split déterministe (graine 42), l'entraînement et l'évaluation du modèle v2. Les
résultats historiques du modèle v1 restent disponibles dans `reports/model-v1`.

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
- signalement explicite des prédictions sous 60 % de confiance ;
- historique et statistiques des prédictions ;
- métriques applicatives et IA sur `/stats/monitoring` ;
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
npm test
npm run build
```
## Collecte multi-source (C1)

Les données image proviennent de trois sources documentées dans
[`docs/data_sources.md`](docs/data_sources.md) :

- Garbage Classification : dataset historique V2 ;
- Garbage Classification V2 : extension utilisée pour V3 ;
- RealWaste : évaluation externe, exclue de l'entraînement.

Vérifier les sources déjà présentes et générer le manifeste de traçabilité :

```powershell
python scripts\collect_sources.py

## Préparer et entraîner le modèle

```bash
pip install -r requirements-data.txt
python scripts/download_dataset.py
python scripts/audit_dataset.py --fail-on-invalid
python scripts/prepare_classification_dataset.py --destination data/classification/v2
python scripts/train_yolo_classification.py --data data/classification/v2 --epochs 20 --batch 32 --device cpu --workers 0
python scripts/evaluate_model.py --model runs/classify/runs/classify/eco_tri_yolov8n_cls/weights/best.pt --test-dir data/classification/v2/test --output-dir reports/model
```

Le split est déterministe avec la graine 42 et exclut les fichiers listés dans
`data/quality_exclusions.json`. Le modèle final doit être copié dans
`backend/models/best.pt` après l'évaluation du jeu de test.

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
| GET | `/stats/monitoring` | Erreurs, latences et incertitudes |

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

- Documentation de l’API de données sécurisée : [`docs/api_data.md`](docs/api_data.md).



Projet repris et développé individuellement par **Katia Boussad**.
