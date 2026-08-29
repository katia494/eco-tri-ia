# Benchmark des modèles - ECO-TRI

## Besoin

Classifier une photographie entière dans six catégories, localement, avec un
modèle léger et une réponse adaptée à une application web.

## Comparaison

| Solution | Adaptation aux images | Coût | Complexité | Décision |
|---|---|---|---|---|
| Random Forest sur pixels | Faible : structure spatiale perdue | Gratuit | Faible | Baseline uniquement |
| XGBoost sur pixels | Faible à moyenne | Gratuit | Moyenne | Comparatif uniquement |
| YOLOv8 Detect | Bonne avec bounding boxes | Gratuit | Élevée | Écarté : aucune bounding box |
| MobileNetV3 | Très bonne | Gratuit | Moyenne | Alternative pertinente |
| YOLOv8n-cls | Très bonne pour une classe par image | Gratuit | Moyenne | **Retenu** |
| Google/AWS Vision | Bonne | Payant/cloud | Faible | Écarté : coût et transfert d'images |

## Résultat du modèle retenu

- entraînement : 1 766 images ;
- validation : 377 images ;
- test indépendant : 384 images ;
- accuracy test : **91,15 %** ;
- macro F1 test : **90,47 %** ;
- meilleur entraînement : époque 12 avec arrêt anticipé ;
- taille du modèle : environ 2,9 Mo.

Les métriques par classe et la matrice de confusion se trouvent dans
`reports/model`. Le score de validation n'est pas présenté comme score final :
seul le jeu de test indépendant sert à annoncer la performance finale.

## Justification

YOLOv8n-cls conserve l'information spatiale de l'image, utilise des poids
préentraînés et reste suffisamment léger pour une API CPU. Ce choix correspond au
dataset par dossiers et ne nécessite pas d'inventer des annotations de détection.
