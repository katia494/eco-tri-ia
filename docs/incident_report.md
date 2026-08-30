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
- entraînement v1 sur les 2 527 images brutes ;
- ajout de `backend/models/best.pt` ;
- service d'inférence paresseux ;
- dépendances centralisées dans `requirements.txt` ;
- tests avec simulation contrôlée de l'inférence ;
- CI backend et frontend ;
- documentation harmonisée.

## Test de non-régression

- import de l'application sans charger le modèle ;
- 28 tests backend et 3 tests métier frontend passent ;
- le frontend passe lint et build ;
- une prédiction réelle a été exécutée avec `best.pt` ;
- l'évaluation v1 séparée atteint 91,15 % sur 384 images de test ;
- après audit des doublons, la v2 atteint 91,64 % sur 383 images de test.

## Prévention

Toute nouvelle version doit inclure dans la même pull request : modèle, version,
dépendances, test, métriques, documentation et workflow vert.

## Incident 2 — parcours bloqué et confiance trompeuse

### Symptômes

- après une prédiction, aucun bouton ne permettait d'analyser une deuxième photo ;
- les compteurs de points et de déchets étaient simulés ;
- une photo externe de métal a été classée `paper` avec seulement 52 % de confiance.

### Cause

L'interface ne distinguait pas assez une prédiction fiable d'une prédiction
incertaine et mélangeait démonstration visuelle et données réelles.

### Correction et non-régression

- seuil de confiance porté à 60 % ;
- champ API `is_uncertain` ;
- aucune consigne catégorique sous le seuil ;
- bouton « Analyser une autre image » ;
- compteurs remplacés par les statistiques SQLite ;
- test backend de faible confiance et trois tests métier frontend.
