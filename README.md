# ECO-TRI IA

Application web de tri des déchets par vision artificielle.

Le frontend React/Vite envoie une image à une API FastAPI. Le modèle
**YOLOv8n-cls V3** classe l'objet parmi six catégories et retourne une
consigne de tri. Les images envoyées par l'utilisateur ne sont pas conservées.

## Résultats vérifiés

| Évaluation | Images | Accuracy | Macro F1 | Interprétation |
|---|---:|---:|---:|---|
| V3 interne | 793 | **93,69 %** | **92,87 %** | Périmètre proche de l'entraînement |
| V3 sur ancien test V2 verrouillé | 383 | **88,51 %** | **87,00 %** | Comparaison contrôlée |
| V3 externe RealWaste | 3 587 | **41,96 %** | **40,98 %** | Généralisation limitée hors périmètre |

Le modèle reconnaît : `cardboard`, `glass`, `metal`, `paper`, `plastic` et
`trash`.

L'évaluation RealWaste est séparée de l'entraînement. ECO-TRI IA est un
prototype pédagogique d'aide au tri : ce n'est pas un système municipal
généralisable.

## Données et qualité

- Catalogue SQLite : **7 769 images canoniques** et **9 985 liens de provenance**.
- Sources d'entraînement documentées : Garbage Classification V1 et V2.
- RealWaste est réservé à l'évaluation externe.
- Les doublons sont détectés par SHA-256.
- Modèle final : `yolov8n-cls-v3`.

## Qualité logicielle

- **46 tests Pytest réussis** ;
- **89 % de couverture backend** ;
- CI GitHub Actions exécutée à chaque push ;
- build Docker et route `/health` validés localement.

## Architecture

```text
Utilisateur → React/Vite → FastAPI → YOLOv8n-cls V3
                              ├─ SQLite : catalogue et prédictions
                              ├─ API de données protégée par clé
                              └─ logs, métriques et monitoring
```

## Fonctionnalités

- import ou capture d'une image JPG/PNG ;
- validation du type, du contenu et de la taille ;
- prédiction avec confiance et consigne de tri ;
- seuil d'incertitude à 60 % ;
- historique, statistiques et points de collecte ;
- monitoring sur `/stats/monitoring` ;
- documentation OpenAPI sur `/docs`.

## Installation locale

Prérequis : Python 3.12 et Node.js 22.

```powershell
git clone https://github.com/katia494/eco-tri-ia.git
cd eco-tri-ia
python -m venv .venv
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

Ouvrir l'interface sur `http://localhost:5173` et l'API sur
`http://localhost:8000/docs`.

> Renseigner une valeur privée pour `DATA_API_KEY` dans `.env`. Ne jamais
> versionner le fichier `.env`.

## Vérifications

```powershell
python -m pytest -q
cd frontend
npm run lint
npm test
npm run build
```

## Docker

```powershell
docker compose build
docker compose up -d
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" | ConvertTo-Json
```

La réponse attendue contient `status: "ok"` et `model: "yolov8n-cls-v3"`.

Pour arrêter le service :

```powershell
docker compose down
```

Le conteneur utilise un volume SQLite persistant et démarre l'API avec un
utilisateur non-root.

## API principale

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/health` | État de l'API |
| GET | `/model/info` | Version du modèle et classes |
| POST | `/predict` | Classification d'une image |
| GET | `/predictions` | Historique des prédictions |
| GET | `/stats/` | Statistiques globales |
| GET | `/stats/monitoring` | Erreurs, latences et incertitudes |
| GET | `/records` | Catalogue, protégé par `x-api-key` |
| GET | `/search` | Recherche, protégée par `x-api-key` |

## Confidentialité et limites

- aucune image utilisateur n'est conservée ;
- seules les métadonnées nécessaires sont stockées ;
- les routes de données sont protégées par `DATA_API_KEY` ;
- le modèle se limite aux six catégories apprises ;
- toute prédiction externe doit être vérifiée ;
- la prédiction n'est pas une consigne municipale officielle.

## Documentation

Les documents de conception, RGPD, veille, benchmark, évaluation externe,
monitoring, incident et preuves sont disponibles dans [`docs/`](docs/).

Projet repris et développé individuellement par **Katia Boussad**.