
# Prise en compte du RGPD — ECO-TRI

## 1. Périmètre du traitement

ECO-TRI est un prototype de classification d’images de déchets. Le catalogue
SQLite sert à tracer les images utilisées pour entraîner ou évaluer le modèle.

Les sources utilisées sont :

- **Garbage Classification V1** : jeu historique utilisé pour l’entraînement ;
- **Garbage Classification V2** : extension utilisée pour l’entraînement ;
- **RealWaste** : jeu réservé à l’évaluation externe, non importé dans le
  catalogue d’entraînement.

Les jeux de données sont composés d’images de déchets. Aucune donnée
personnelle n’est intentionnellement collectée. Toutefois, une image publique
peut exceptionnellement contenir un élément contextuel identifiable. Cette
possibilité est prise en compte dans les mesures de minimisation ci-dessous.

## 2. Registre simplifié des données

| Élément | Finalité | Données conservées | Données personnelles attendues |
|---|---|---|---|
| `sources_donnees` | Identifier l’origine et la licence des datasets | nom, fournisseur, URL, licence, rôle | Non |
| `dechets` | Constituer le catalogue canonique | nom, catégorie, chemin, SHA-256, date, source | Non |
| `dechet_sources` | Assurer la traçabilité multi-source | source, chemin, catégorie d’origine | Non |
| `predictions` | Journaliser une prédiction de démonstration | nom de fichier, classe, score, date | Non intentionnellement |

La colonne `contient_donnees_perso` de `sources_donnees` permet de documenter
explicitement l’analyse de chaque source.

## 3. Minimisation des données

La base SQLite ne copie pas les fichiers image. Elle stocke uniquement :

- le chemin local de l’image ;
- sa catégorie ;
- son empreinte SHA-256 ;
- sa source et sa date d’import ;
- les liens de provenance nécessaires à l’audit.

L’empreinte SHA-256 permet de dédoublonner les fichiers sans multiplier les
copies. Les 9 985 occurrences admissibles sont ainsi représentées par 7 769
images canoniques.

Les données brutes, les bases SQLite locales et les sauvegardes sont exclues
du dépôt Git grâce au fichier `.gitignore`.

## 4. Base légale et licences

Le projet poursuit une finalité pédagogique et de recherche appliquée :
entraîner, évaluer et démontrer un classifieur de déchets.

Avant toute réutilisation hors cadre pédagogique, il faut vérifier la licence
de chaque source et respecter ses conditions :

- les deux datasets Kaggle doivent être utilisés selon leur licence publiée ;
- RealWaste est documenté avec sa licence `CC BY-NC-SA 4.0` et reste réservé à
  l’évaluation externe.

## 5. Conservation et suppression

Les données sont conservées pendant la durée du projet et de son évaluation
pédagogique. Elles doivent être supprimées lorsque cette finalité cesse, sauf
obligation légale ou accord explicite pour une conservation plus longue.

En cas de présence accidentelle d’une donnée personnelle identifiable dans une
image, le fichier concerné doit être ajouté à `data/catalog_exclusions.json`,
exclu du prochain import, puis supprimé de l’espace de travail local.

## 6. Sécurité

Les mesures mises en place sont les suivantes :

- accès aux routes de consultation des données protégé par l’en-tête
  `x-api-key` ;
- clé conservée dans le fichier local `.env`, jamais dans Git ;
- bases et sauvegardes SQLite ignorées par Git ;
- intégrité référentielle vérifiée avec `PRAGMA foreign_key_check` ;
- import reproductible, traçable et contrôlé par tests ;
- en production, l’API devra être servie exclusivement via HTTPS.

## 7. Droits et gestion d’incident

Toute demande relative à une image ou à une donnée potentiellement personnelle
doit être analysée rapidement. Si elle est fondée, la procédure est :

1. identifier l’image et sa source ;
2. l’ajouter aux exclusions ;
3. reconstruire le catalogue avec l’import reproductible ;
4. vérifier l’absence de l’image dans la base ;
5. consigner l’action dans le rapport de projet.

## 8. Preuves associées

Les preuves techniques C4 sont versionnées dans le dépôt :

- `sql/schema.sql` : schéma relationnel versionné ;
- `src/import_data.py` : import reproductible multi-source ;
- `docs/mcd_mpd.md` : modèle conceptuel et physique ;
- `reports/c4_multisource_preflight.json` : audit avant import ;
- `reports/c4_multisource_import.json` : résultat de l’import ;
- `reports/c4_database_checks.json` : contrôle d’intégrité ;
- `tests/test_import_multisource.py` : test automatisé du dédoublonnage et de
  la provenance.