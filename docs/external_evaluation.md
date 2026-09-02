# Évaluation externe — RealWaste

## Objectif

Mesurer la capacité de généralisation du modèle YOLOv8n-cls V3 sur un dataset
indépendant, jamais utilisé pour l’entraînement, la validation ou le test interne.

RealWaste est réservé à cette évaluation externe. Il n’est pas ajouté au
catalogue d’entraînement ni à la base SQLite des images canoniques.

## Jeu évalué

| Élément | Valeur |
|---|---|
| Source | RealWaste |
| Rôle | Évaluation externe uniquement |
| Images évaluées | 3 587 |
| Classes communes | cardboard, glass, metal, paper, plastic, trash |
| Modèle | YOLOv8n-cls V3 |
| Seuil d’incertitude | 60 % |

Le dataset contient des images plus variées et plus proches de situations
réelles que les images Kaggle utilisées pour l’entraînement.

## Résultats

| Indicateur | Résultat |
|---|---:|
| Accuracy | 41,96 % |
| Macro F1 | 40,98 % |
| Prédictions sous le seuil de confiance | 503 |
| Taux de prédictions incertaines | 14,02 % |
| Erreurs de classification | 2 082 |

Les résultats détaillés sont disponibles dans :

- `reports/external-realwaste-v3/metrics.json` ;
- `reports/external-realwaste-v3/confusion_matrix.csv` ;
- `reports/external-realwaste-v3/errors.csv` ;
- `reports/external-realwaste-v3/predictions.csv`.

## Analyse

La V3 obtient de très bons résultats sur son jeu interne, mais les performances
baissent fortement sur RealWaste. Cette différence montre un décalage entre les
images d’entraînement et des images plus réalistes : cadrage, lumière, arrière-plan,
état des déchets et variabilité des objets.

La classe `metal` est la mieux reconnue sur RealWaste avec un F1 de 56,22 %.
Les classes `cardboard`, `glass` et `trash` restent plus difficiles à
généraliser.

## Décision produit

Le modèle peut être présenté comme une démonstration technique locale de
classification parmi six catégories. Il ne doit pas être présenté comme un
système prêt pour une utilisation municipale réelle.

L’API signale les prédictions sous 60 % de confiance afin d’éviter une consigne
de tri trop catégorique lorsque le modèle hésite.

## Pistes d’amélioration

1. ajouter des images prises dans des conditions réelles ;
2. diversifier les arrière-plans et les niveaux de dégradation ;
3. analyser les erreurs par classe avant tout nouvel entraînement ;
4. conserver RealWaste comme jeu de test externe indépendant ;
5. mesurer toute nouvelle version du modèle avec le même protocole.
