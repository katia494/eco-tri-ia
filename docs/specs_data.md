# Spécifications des données

## Source et objectif

- source : [Garbage Classification sur Kaggle](https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification) ;
- méthode : téléchargement automatisé avec `kagglehub` ;
- volume brut vérifié : 2 527 images JPEG, six classes ;
- usage : entraînement et évaluation d'un classifieur pédagogique de déchets ;
- date de collecte documentée : 28 août 2026.

## Contraintes

| Contrainte | Traitement dans le projet |
|---|---|
| Accès | Connexion Kaggle nécessaire lors du premier téléchargement |
| Format | Images JPEG classées par dossiers |
| Confidentialité | Dataset public ; aucune image utilisateur ajoutée au dataset |
| Qualité | Audit Pillow + SHA-256 avant préparation |
| Licence | Vérifier les conditions affichées par Kaggle avant toute redistribution |
| Volume Git | Le script permet de reproduire la collecte sans dépendre uniquement du dépôt |

## Résultat de collecte

Le rapport `reports/data_quality.json` confirme 2 527 images lisibles. Trois
copies contradictoires sont conservées dans les données brutes pour la
traçabilité, puis exclues du dataset traité par `data/quality_exclusions.json`.

## Commandes

```bash
python scripts/download_dataset.py
python scripts/audit_dataset.py --fail-on-invalid
python scripts/prepare_classification_dataset.py
```
