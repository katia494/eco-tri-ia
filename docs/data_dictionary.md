# Dictionnaire de données SQLite

## Table `dechets`

| Colonne | Type | Rôle |
|---|---|---|
| `id` | INTEGER | Identifiant technique |
| `nom_fichier` | TEXT | Nom du fichier du dataset |
| `categorie` | TEXT | Classe réelle du déchet |
| `chemin_image` | TEXT | Chemin local de la donnée brute |
| `source` | TEXT | Origine du dataset |
| `date_ajout` | TEXT | Date d'import |

## Table `predictions`

| Colonne | Type | Rôle |
|---|---|---|
| `id` | INTEGER | Identifiant de la prédiction |
| `image_name` | TEXT | Nom du fichier envoyé, sans conserver l'image |
| `waste_class` | TEXT | Classe prédite par YOLOv8n-cls |
| `confidence` | REAL | Confiance comprise entre 0 et 1 |
| `created_at` | TEXT | Horodatage de la prédiction |

## Table `statistiques_categories`

Elle contient les effectifs et pourcentages du dataset par catégorie. Ces valeurs
sont recalculées par `src/import_data.py` et ne doivent pas être saisies manuellement.
