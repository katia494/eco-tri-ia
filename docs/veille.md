# Veille technique - classification d'images de déchets

## Problématique

Quel modèle permet de classifier six catégories de déchets avec environ 2 500
images, tout en restant léger, local et intégrable dans une API FastAPI ?

## Méthode de veille

- fréquence pendant le projet : revue hebdomadaire puis revue avant chaque choix majeur ;
- sources prioritaires : documentations officielles, articles scientifiques et dépôts des éditeurs ;
- critères : adéquation à la classification, besoin d'annotations, coût, RGPD,
  qualité attendue, vitesse CPU, taille et facilité d'intégration.

## Sources retenues

| Source | Information utile | Impact sur ECO-TRI |
|---|---|---|
| Documentation Ultralytics - Classification | Une image entière peut être classée sans bounding boxes | Choix de YOLOv8n-cls et non YOLO Detect |
| Documentation Ultralytics - Train/Val/Export | Entraînement, validation et export reproductibles | Scripts séparés de préparation, entraînement et évaluation |
| Documentation XGBoost | XGBoost est un ensemble d'arbres optimisé | Conservé comme comparatif, pas comme modèle final d'images |
| Guide Keras Transfer Learning | Le transfert est adapté aux petits datasets | Justifie l'utilisation de poids préentraînés |

## Décision issue de la veille

YOLOv8n-cls est retenu parce que le besoin est une **classification globale**.
YOLO Detect a été écarté car le dataset ne contient pas de boîtes englobantes.
Random Forest et XGBoost restent des baselines documentées, mais l'aplatissement
des pixels détruit une partie de l'information spatiale.

## Limites et poursuite

La veille devra suivre les nouvelles versions Ultralytics, les vulnérabilités des
dépendances et les modèles légers comme MobileNet/EfficientNet. Toute mise à jour
du modèle exige une nouvelle évaluation sur le même jeu de test.
