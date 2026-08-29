# Rapport d'incident - rupture du pipeline de prédiction

## Résumé

Après plusieurs changements de modèle, la branche principale ne pouvait plus
exécuter les tests ni démarrer l'API. Les trois dernières GitHub Actions étaient rouges.

## Symptôme

```text
ModuleNotFoundError: No module named 'joblib'
```

Après installation manuelle, `predict.py` attendait également
`model_eco_tri_xgb.pkl` et `label_encoder.pkl`, absents du dépôt.

## Cause racine

Le modèle avait été remplacé dans le code sans mise à jour atomique des artefacts,
dépendances, tests, configuration et documentation. Le dépôt mélangeait YOLOv8,
Random Forest et XGBoost.

## Correction

- décision unique : YOLOv8n-cls ;
- entraînement sur les 2 527 vraies images ;
- ajout de `backend/models/best.pt` ;
- service d'inférence paresseux ;
- dépendances centralisées dans `requirements.txt` ;
- tests avec simulation contrôlée de l'inférence ;
- CI backend et frontend ;
- documentation harmonisée.

## Test de non-régression

- import de l'application sans charger le modèle ;
- 21 tests backend passent ;
- le frontend passe lint et build ;
- une prédiction réelle a été exécutée avec `best.pt` ;
- l'évaluation séparée atteint 91,15 % sur 384 images de test.

## Prévention

Toute nouvelle version doit inclure dans la même pull request : modèle, version,
dépendances, test, métriques, documentation et workflow vert.
