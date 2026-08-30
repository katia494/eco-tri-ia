# Règles de nettoyage et de qualité du dataset

## Objectif

Garantir que chaque fichier utilisé pour l'entraînement est une image lisible,
associée à l'une des six classes et qu'aucun doublon exact ne fausse les splits.

## Contrôles automatisés

Le script `scripts/audit_dataset.py` applique les règles suivantes :

1. présence des six dossiers de classes attendus ;
2. extension JPG, JPEG ou PNG ;
3. ouverture et vérification réelle avec Pillow ;
4. dimensions, mode colorimétrique et format relevés ;
5. détection des doublons exacts par SHA-256 ;
6. génération de `reports/data_quality.json`.

Commande reproductible :

```bash
python scripts/audit_dataset.py --fail-on-invalid
```

## Traitement

- une image corrompue est exclue avant la préparation des splits ;
- un format inattendu est signalé pour décision manuelle ;
- un seul exemplaire d'un doublon exact doit être conservé ;
- les images ne sont pas redimensionnées dans les données sources ; le
  redimensionnement et la normalisation sont réalisés par le pipeline YOLO.

Les résultats annoncés dans le rapport doivent provenir du JSON généré, jamais
d'une valeur saisie manuellement dans un notebook.

## Résultat de l'audit du 30 août 2026

- 2 527 fichiers JPEG lisibles ;
- 0 image corrompue ;
- 3 copies exactes avec des étiquettes contradictoires ;
- 2 524 images retenues pour le dataset traité v2.

Les trois exclusions sont justifiées dans `data/quality_exclusions.json`. Les
données brutes restent intactes ; le script de préparation applique les exclusions.
