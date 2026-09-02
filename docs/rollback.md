# Procédure de retour arrière — ECO-TRI IA

## Objectif

Revenir rapidement à une version stable si une version plus récente présente un
incident après livraison.

## Version stable de référence

La version stable actuelle est le tag `v1.0.1`.

## Procédure

Depuis la racine du projet :

```powershell
git fetch --tags
git switch --detach v1.0.1
docker compose down
docker compose build
docker compose up -d
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" | ConvertTo-Json
```

La réponse attendue contient `status: "ok"`.

`docker compose down` ne supprime pas le volume SQLite : ne jamais ajouter
l’option `-v` lors d’un retour arrière normal.

## Retour au développement

Après vérification :

```powershell
git switch feat/model-robustness
```

## Preuves

- tag `v1.0.1` publié ;
- CI GitHub Actions verte ;
- build Docker et route `/health` validés.