# Sources de données et collecte reproductible

## Objectif

ECO-TRI IA classe une image de déchet parmi six catégories :

- cardboard ;
- glass ;
- metal ;
- paper ;
- plastic ;
- trash.

Le projet utilise trois sources distinctes. Deux sources servent à constituer
le jeu d'entraînement, tandis que RealWaste est réservé à l'évaluation externe.

## Registre des sources

| ID | Source | Origine | Données brutes | Rôle |
|---|---|---|---:|---|
| `garbage_classification_v1` | Garbage Classification | Kaggle | 2 527 images | Base historique du modèle V2 |
| `garbage_classification_v2` | Garbage Classification V2 | Kaggle | 11 503 images, 10 classes | Extension du jeu V3 |
| `realwaste` | RealWaste | Dépôt scientifique GitHub | 4 752 images, 9 classes | Évaluation externe uniquement |

## Source 1 — Garbage Classification

- URL : <https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification>
- Format : images JPG organisées par classe.
- Rôle : dataset historique du modèle V2.
- Volume brut : 2 527 images.
- Après audit qualité : 2 524 images ont été conservées.
- Les trois copies contradictoires détectées par empreinte SHA-256 ont été
  exclues avant le split, l'entraînement et l'évaluation.
- Données personnelles : aucune donnée personnelle recherchée ou conservée.

## Source 2 — Garbage Classification V2

- URL : <https://www.kaggle.com/datasets/sumn2u/garbage-classification-v2>
- Format : images classées dans les dossiers `original`,
  `standardized_256` et `standardized_384`.
- Rôle : extension du jeu d'entraînement V3.
- Seul le dossier `original` est utilisé : les deux dossiers standardisés sont
  des redimensionnements des mêmes images et ne doivent pas être mélangés.
- Volume brut dans `original` : 11 503 images réparties dans dix classes.
- Classes retenues pour ECO-TRI : cardboard, glass, metal, paper, plastic,
  trash, soit 7 463 images avant dédoublonnage avec le dataset historique.
- Classes exclues du périmètre : battery, biological, clothes et shoes.
- Données personnelles : aucune donnée personnelle recherchée ou conservée.

## Source 3 — RealWaste

- URL : <https://github.com/sam-single/realwaste>
- Format : images JPG classées dans neuf catégories.
- Rôle : évaluation externe indépendante ; ce dataset n'est jamais utilisé
  pour entraîner, valider ou régler le modèle.
- Volume brut : 4 752 images.
- Classes compatibles avec ECO-TRI après mapping : 3 587 images.
- Mapping : `Miscellaneous Trash` devient `trash`.
- Classes exclues : Food Organics, Textile Trash et Vegetation.
- Licence : CC BY-NC-SA 4.0 ; attribution obligatoire et usage non commercial.
- Données personnelles : aucune donnée personnelle recherchée ou conservée.

## Prévention de la fuite de données

Les deux sources d'entraînement ont été comparées par empreinte SHA-256.
Le contrôle a détecté 2 218 doublons entre le dataset historique et
l'extension V2. Ces doublons ont été exclus du nouveau jeu avant le split V3.

Le jeu RealWaste a également été comparé avec le jeu V3. Aucun doublon exact
n'a été détecté. Il reste donc un jeu de test externe indépendant.

## Reproduire la collecte

Installer les dépendances de données :

```powershell
pip install -r requirements-data.txt