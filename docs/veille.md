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

Consultation vérifiée le **30 août 2026**.

| Source | Auteur | Fiabilité | Information utile | Impact sur ECO-TRI |
|---|---|---|---|---|
| [Classification Ultralytics](https://docs.ultralytics.com/tasks/classify/) | Ultralytics | Source primaire, documentation officielle | La classification attribue une classe à l'image entière | Choix de YOLOv8n-cls |
| [Configuration Ultralytics](https://docs.ultralytics.com/usage/cfg/) | Ultralytics | Source primaire, paramètres maintenus | Les tâches `classify` et `detect` répondent à des contrats différents | YOLO Detect écarté faute de bounding boxes |
| [MobileNetV3](https://docs.pytorch.org/vision/stable/models/mobilenetv3.html) | PyTorch/Torchvision | Source primaire, documentation officielle | Architecture légère avec poids préentraînés | Alternative locale retenue pour une future comparaison |
| [Recommandations IA et RGPD](https://www.cnil.fr/fr/developpement-des-systemes-dia-les-recommandations-de-la-cnil-pour-respecter-le-rgpd) | CNIL | Autorité publique française | Minimisation et maîtrise des données traitées | Les images envoyées ne sont pas conservées |

## Décision issue de la veille

YOLOv8n-cls est retenu parce que le besoin est une **classification globale**.
YOLO Detect a été écarté car le dataset ne contient pas de boîtes englobantes.
Random Forest et XGBoost restent des baselines documentées, mais l'aplatissement
des pixels détruit une partie de l'information spatiale.

## Limites et poursuite

La veille est revue avant chaque changement du modèle et au minimum une fois par
mois. Elle suit les versions Ultralytics, les vulnérabilités des dépendances et
les modèles légers comme MobileNet. Toute mise à jour exige une nouvelle
évaluation sur le même protocole de test.
