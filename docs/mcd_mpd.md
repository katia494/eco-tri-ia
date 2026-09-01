# Conformité RGPD et gestion des données — ECO-TRI

> **Projet** : ECO-TRI — classification de déchets par IA
> **Auteure** : Katia Boussad
> **Cadre** : prototype pédagogique et démonstration technique
> **Dernière mise à jour** : 1er septembre 2026

## 1. Périmètre du traitement

ECO-TRI traite des images de déchets pour :

- construire un catalogue de données traçable ;
- entraîner et évaluer un modèle de classification ;
- répondre à une demande de prédiction dans l’application.

Le projet ne vise pas à collecter des données personnelles. Une image de déchet
peut toutefois contenir accidentellement une personne, un visage, une plaque ou
un texte identifiable. Ce risque résiduel est pris en compte par la minimisation
des données et l’absence de conservation des images envoyées par l’utilisateur.

## 2. Registre simplifié des traitements

| Élément | Description |
|---|---|
| Responsable du prototype | Katia Boussad |
| Finalité | Classification pédagogique de six catégories de déchets |
| Personnes concernées | Utilisateurs de démonstration ; personnes éventuellement visibles par erreur dans une image |
| Données traitées | Images de datasets, nom de fichier, catégorie, empreinte SHA-256, chemin local, source, prédiction, confiance, date |
| Données volontairement non conservées | Image envoyée par l’utilisateur lors de la prédiction |
| Destinataires | Environnement local du projet et jury pédagogique |
| Hébergement actuel | Machine locale et volume Docker local |
| Transfert hors UE | Aucun transfert volontaire de données utilisateur |

## 3. Sources et licences

| Source | Rôle | Données personnelles déclarées | Licence / précaution |
|---|---|---:|---|
| Garbage Classification V1 | Données historiques | Non | Respecter la licence affichée sur Kaggle |
| Garbage Classification V2 | Extension d’entraînement V3 | Non | Respecter la licence affichée sur Kaggle |
| RealWaste | Évaluation externe uniquement | Non | CC BY-NC-SA 4.0 : attribution et usage non commercial |

RealWaste n’est pas intégré au catalogue d’entraînement. Il est utilisé
séparément pour mesurer la généralisation externe du modèle.

## 4. Minimisation et séparation des données

- Les fichiers bruts restent dans `data/raw/` et ne sont pas commités dans Git.
- La base SQLite conserve des métadonnées et des chemins, pas une copie binaire
  supplémentaire des images.
- L’empreinte SHA-256 sert uniquement au dédoublonnage et à la traçabilité.
- L’endpoint `/predict` lit l’image en mémoire pour l’inférence ; il ne
  sauvegarde pas le fichier envoyé.
- L’historique de prédiction conserve seulement le nom du fichier, la classe,
  la confiance et la date.

## 5. Durée de conservation

| Donnée | Durée dans le prototype | Règle |
|---|---|---|
| Datasets bruts | Durée du projet pédagogique | Suppression à la fin du projet ou selon la licence |
| Catalogue SQLite | Durée du projet pédagogique | Recréable par script depuis les sources |
| Prédictions locales | Durée de la démonstration | À purger avant diffusion publique |
| Images utilisateur | Non conservées | Traitement en mémoire uniquement |

Il n’existe pas encore de purge automatique, car le projet est local et
pédagogique. Une mise en production nécessiterait une durée paramétrable et
une tâche de suppression planifiée.

## 6. Mesures de sécurité

- la clé d’accès aux endpoints de données est stockée dans `.env` ;
- `.env` n’est pas versionné ;
- les endpoints `/records`, `/records/{id}` et `/search` exigent `x-api-key` ;
- `/health` reste public pour le contrôle technique ;
- les accès sans clé ou avec une clé incorrecte reçoivent `401 Unauthorized` ;
- SQLite est stocké localement et exclu de Git ;
- HTTPS devra être activé avant toute mise en production.

## 7. Droits et demandes

Dans un contexte de production, une personne pourrait demander :

- l’accès aux données la concernant ;
- la rectification ou l’effacement ;
- la limitation du traitement ;
- une information sur la finalité et la conservation.

Pour le prototype, toute image utilisateur n’étant pas conservée, il n’existe
pas de fichier image à restituer après la réponse de prédiction. Les éventuels
historiques locaux doivent être supprimés sur demande.

## 8. Procédure en cas d’incident

En cas d’exposition accidentelle d’une image ou d’une clé :

1. arrêter le service concerné ;
2. révoquer et régénérer la clé `DATA_API_KEY` ;
3. supprimer les données exposées si elles existent ;
4. documenter l’incident et ajouter un test de non-régression ;
5. vérifier que les secrets et bases locales ne sont pas dans Git.

## 9. Preuves dans le dépôt


- `config/dataset_sources.json` : sources, rôles et licences ;
- `data/catalog_exclusions.json` : exclusions qualité documentées ;
- `sql/schema.sql` : contraintes et traçabilité des sources ;
- `src/import_data.py` : import reproductible ;
- `docs/mcd_mpd.md` : modèle de données ;
- `docs/api_data.md` : protection des endpoints de données ;
- `reports/c4_multisource_preflight.json` et
  `reports/c4_multisource_import.json` : preuves d’exécution.