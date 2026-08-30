# Benchmark des modèles - ECO-TRI

## Besoin

Classifier une photographie entière dans six catégories, localement, avec un
modèle léger et une réponse adaptée à une application web.

## Comparaison décisionnelle

| Solution | Adaptation aux images | Coût | Complexité | Décision |
|---|---|---|---|---|
| Random Forest sur pixels | Faible : structure spatiale perdue | Gratuit | Faible | Baseline uniquement |
| XGBoost sur pixels | Faible à moyenne | Gratuit | Moyenne | Comparatif uniquement |
| YOLOv8 Detect | Bonne avec bounding boxes | Gratuit | Élevée | Écarté : aucune bounding box |
| MobileNetV3 | Très bonne | Gratuit | Moyenne | Alternative pertinente |
| YOLOv8n-cls | Très bonne pour une classe par image | Gratuit | Moyenne | **Retenu** |
| Google/AWS Vision | Bonne | Payant/cloud | Faible | Écarté : coût et transfert d'images |

Cette première table est une analyse de décision, pas une mesure expérimentale
des performances de toutes les solutions.

## Matrice de décision pondérée

Notes sur 5. Pondération : qualité image 35 %, fonctionnement local/RGPD 25 %,
facilité d'intégration 20 %, coût 10 %, légèreté 10 %.

| Solution | Qualité image | Local/RGPD | Intégration | Coût | Légèreté | Score /5 |
|---|---:|---:|---:|---:|---:|---:|
| Random Forest pixels | 2 | 5 | 4 | 5 | 4 | 3,55 |
| XGBoost pixels | 2 | 5 | 3 | 5 | 3 | 3,25 |
| MobileNetV3 | 5 | 5 | 3 | 5 | 5 | 4,60 |
| YOLOv8n-cls | 5 | 5 | 5 | 5 | 4 | **4,90** |
| Google/AWS Vision | 4 | 1 | 4 | 2 | 5 | 3,15 |

Les notes sont des appréciations techniques justifiées par les contraintes du
MVP. Seul YOLOv8n-cls a été entraîné et mesuré dans ce projet.

## Résultat du modèle retenu

- entraînement : 1 764 images ;
- validation : 377 images ;
- test indépendant : 383 images ;
- accuracy test : **91,64 %** ;
- macro F1 test : **90,48 %** ;
- meilleur entraînement : époque 8 ; arrêt anticipé après 15 époques ;
- taille du modèle : environ 3 Mo.

Les métriques v2 par classe, la matrice de confusion et le manifeste du split se
trouvent dans `reports/model`. Les résultats v1 sont archivés dans
`reports/model-v1`. Le score de validation n'est pas présenté comme score final :
seul le jeu de test indépendant sert à annoncer la performance finale.

## Justification

YOLOv8n-cls conserve l'information spatiale de l'image, utilise des poids
préentraînés et reste suffisamment léger pour une API CPU. Ce choix correspond au
dataset par dossiers et ne nécessite pas d'inventer des annotations de détection.

## Limite observée hors dataset

Une photo externe de métal trouvée sur le Web a été prédite `paper` avec 52 % de
confiance. Ce test isolé ne remplace pas un benchmark, mais révèle un possible
décalage entre le dataset Kaggle et les images réelles. La version corrigée de
l'application signale désormais toute confiance inférieure à 60 % et demande une
nouvelle photo. Un jeu externe équilibré reste à constituer pour mesurer la
généralisation avant une utilisation réelle.
