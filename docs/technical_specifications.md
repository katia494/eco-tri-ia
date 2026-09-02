# Spécifications techniques

## Architecture retenue

```text
Navigateur React/Vite
        |
        | multipart/form-data
        v
API FastAPI -> validation -> YOLOv8n-cls
        |                       |
        | métadonnées           | classe + probabilité
        v                       |
      SQLite <------------------+
        |
        +-> logs de statut et de latence
```

## Composants

| Composant | Technologie | Responsabilité |
|---|---|---|
| Interface | React, Vite | Capture, upload, affichage et erreurs |
| API | FastAPI, Pydantic | Contrat HTTP, validation et OpenAPI |
| Modèle | YOLOv8n-cls | Classification parmi six catégories |
| Stockage | SQLite, SQLAlchemy | Métadonnées des prédictions |
| Qualité | pytest, ESLint, Vite build | Non-régression et livrabilité |
| CI | GitHub Actions | Tests backend, couverture, lint et build |

## Contrat de prédiction

Entrée : un champ multipart `file`, MIME `image/jpeg` ou `image/png`, 10 Mo maximum.

Sortie :

```json
{
  "waste_class": "plastic",
  "confidence": 0.91,
  "model": "yolov8n-cls-v3",
  "image_name": "bouteille.jpg",
  "sorting_instruction": "Videz l'emballage...",
  "message": "Déchet classifié comme plastic avec 91.0 % de confiance.",
  "is_uncertain": false
}
```

## Choix et compromis

- SQLite est retenu pour un MVP local reproductible ; PostgreSQL est une évolution.
- Le fichier unique `data/eco_tri.db` est généré localement et n'est pas versionné.
- Si l'ancien schéma français est détecté, la table est conservée sous le nom
  `predictions_legacy` avant la création du schéma unifié.
- Le modèle est chargé paresseusement une fois, afin que `/health` reste disponible.
- Les tests API simulent l'inférence ; l'évaluation séparée utilise le vrai modèle.
- L'API ne conserve pas les images afin de minimiser les données.
