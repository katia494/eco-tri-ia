# Benchmark des solutions IA — ECO-TRI

## Besoin

Classifier localement une photographie entière dans six catégories de déchets,
avec un modèle léger, intégrable à une API FastAPI et compatible avec une
utilisation respectueuse de la confidentialité.

## Comparaison décisionnelle

| Solution | Adaptation au besoin | Fonctionnement local | Coût | Sobriété / données | Décision |
|---|---|---:|---:|---|---|
| Random Forest sur pixels | Faible : structure spatiale perdue | Oui | Gratuit | Peu adapté : aplatissement coûteux et perte d'information | Baseline uniquement |
| XGBoost sur pixels | Faible à moyenne | Oui | Gratuit | Peu adapté : mêmes limites sur les pixels aplatis | Comparatif uniquement |
| YOLOv8 Detect | Nécessite des boîtes englobantes | Oui | Gratuit | Calcul local, mais architecture inutilement complexe pour le besoin | Écarté : dataset sans annotations de détection |
| MobileNetV3 | Très bonne | Oui | Gratuit | Modèle léger, adapté à une exécution locale sur CPU | Alternative pertinente |
| Google / AWS Vision | Bonne | Non | Payant | Transfert d'images vers le cloud et dépendance à un service externe | Écarté : coût et confidentialité |
| YOLOv8n-cls | Très bonne pour une classe par image | Oui | Gratuit | Modèle léger, local, sans transfert d'image utilisateur | **Retenu** |


## Choix retenu

YOLOv8n-cls est adapté au problème : chaque image possède une seule catégorie
globale et le dataset est organisé en dossiers de classes. Le modèle conserve
l’information spatiale de l’image, utilise des poids préentraînés et reste assez
léger pour une exécution locale avec FastAPI.

YOLO Detect a été écarté : aucune boîte englobante n’est disponible dans les
datasets. Les services cloud ont été écartés pour limiter le coût et éviter le
transfert des images utilisateur vers un service externe.

## Résultats mesurés

| Évaluation | Jeu évalué | Images | Accuracy | Macro F1 | Interprétation |
|---|---:|---:|---:|---:|---|
| V2 historique | Test Kaggle V2 indépendant | 383 | 91,64 % | 90,48 % | Référence historique |
| V3 interne | Test issu du dataset V3 | 793 | **93,69 %** | **92,87 %** | Très bon résultat dans un environnement proche de l’entraînement |
| V3 contrôlé | Ancien test Kaggle V2 verrouillé | 383 | 88,51 % | 87,00 % | Mesure comparable à V2, baisse à analyser honnêtement |
| V3 externe | RealWaste indépendant | 3 587 | 41,96 % | 40,98 % | Généralisation encore insuffisante sur des images plus réalistes |

Les métriques détaillées sont disponibles dans :

- `reports/model-v3-final/metrics.json` ;
- `reports/model-v3-on-v2-test/metrics.json` ;
- `reports/external-realwaste-v3/metrics.json`.

## Analyse critique

La V3 améliore les résultats sur son test interne, avec 93,69 % d’accuracy.
Cependant, son score sur le test V2 verrouillé est inférieur à la référence V2.
Elle ne doit donc pas être présentée comme une amélioration universelle sans
nuance.

Le test RealWaste est la preuve la plus importante de généralisation : avec
41,96 % d’accuracy et 40,98 % de macro F1, le modèle reste limité lorsque les
images sont plus variées, plus réalistes et prises dans d’autres contextes.

Le seuil d’incertitude de l’API est maintenu à 60 %. Sur RealWaste, 14,02 % des
prédictions sont signalées comme incertaines. Ce mécanisme réduit le risque de
donner une consigne catégorique lorsque le modèle hésite, mais il ne remplace
pas une amélioration du dataset.

## Décision

YOLOv8n-cls V3 est conservé pour la démonstration technique, car il permet un
service local, léger et documenté. Le projet ne revendique pas une robustesse
suffisante pour un usage municipal réel.

Avant un déploiement réel, il faudrait collecter davantage d’images proches des
conditions d’usage, enrichir les classes faibles et réévaluer le modèle sur un
jeu externe indépendant.
