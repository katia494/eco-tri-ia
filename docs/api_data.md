# API de données sécurisée — C5

## Objectif

L’API ECO-TRI expose des données importées dans SQLite tout en protégeant
les endpoints concernés par une clé envoyée dans l’en-tête HTTP `x-api-key`.

L’état de santé de l’application reste volontairement public afin de permettre
la supervision technique.

## Endpoints

| Méthode | Route | Authentification | Rôle |
|---|---|---:|---|
| GET | `/health` | Non | Vérifie que l’API est disponible |
| GET | `/records` | Oui | Liste paginée des enregistrements |
| GET | `/records/{record_id}` | Oui | Retourne un enregistrement précis |
| GET | `/search` | Oui | Recherche par nom de fichier ou catégorie |
| GET | `/docs` | Non | Documentation OpenAPI / Swagger |

## Configuration

La clé privée est stockée uniquement dans le fichier local `.env` :

```env
DATA_API_KEY=valeur_privee_non_versionnee
```

Le fichier `.env.example` ne contient qu’un exemple. Aucune clé réelle ne doit
être ajoutée à Git ou affichée dans les captures d’écran.

## Démarrer l’API

```powershell
python -m uvicorn backend.api.main:app --reload
```

La documentation interactive est disponible sur :

```text
http://127.0.0.1:8000/docs
```

## Vérification manuelle de la sécurité

### Accès refusé sans clé

```powershell
try {
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/records"
} catch {
    $_.Exception.Response.StatusCode.value__
    $_.ErrorDetails.Message
}
```

Résultat vérifié : `401` et le message `Clé API absente ou invalide.`

### Accès autorisé avec clé

La clé est récupérée localement sans être affichée :

```powershell
$key = python -c "from backend.api.config import settings; print(settings.data_api_key)"

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/records?limit=2" `
  -Headers @{"x-api-key" = $key} | ConvertTo-Json -Depth 5
```

Résultat vérifié : l’API retourne les enregistrements SQLite, avec `total: 2527`
et une liste `items` paginée.

## Tests automatisés

Les tests `tests/test_data_api.py` vérifient :

- `/health` reste accessible sans clé ;
- `/records` refuse l’absence ou une mauvaise clé avec `401` ;
- `/records` accepte une clé valide et applique la pagination ;
- `/records/{id}` retourne l’enregistrement demandé ou `404` ;
- `/search` filtre les enregistrements.

Commande exécutée :

```powershell
python -m pytest -q
```

Résultat vérifié le 1er septembre 2026 : **45 tests passés**, 1 warning non bloquant,
avec **89 %** de couverture backend.