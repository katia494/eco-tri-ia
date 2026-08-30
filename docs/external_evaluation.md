# Évaluation externe du modèle

## Objectif

Mesurer la généralisation de YOLOv8n-cls-v2 sur des images jamais utilisées
pour l'entraînement, la validation ou le test Kaggle.

## Protocole

- au moins cinq images par classe dans `data/external_test/<classe>` ;
- six classes équilibrées ;
- origine des images renseignée dans la commande ;
- seuil d'incertitude identique à l'API : 60 % ;
- aucune image externe ajoutée au dataset d'entraînement ;
- images non publiées dans Git afin d'éviter données personnelles et licences ;
- seuls les rapports agrégés et les chemins relatifs sont versionnés.

```powershell
python scripts/audit_dataset.py --source data/external_test --output reports/external/data_quality.json --fail-on-invalid
python scripts/evaluate_external_dataset.py --origin "photos personnelles"
```

## Sorties

- `reports/external/metrics.json` : accuracy, macro F1 et taux d'incertitude ;
- `reports/external/predictions.csv` : résultat de chaque image ;
- `reports/external/errors.csv` : erreurs à analyser ;
- `reports/external/confusion_matrix.csv` : confusions entre classes.

Les résultats externes mesurent un contexte différent du test Kaggle. Ils ne
doivent pas être fusionnés avec les métriques internes ni utilisés pour ajuster
le modèle avant d'avoir constitué un nouveau jeu externe indépendant.
