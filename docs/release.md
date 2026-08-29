# Procédure de livraison

## Préconditions

- tests backend verts ;
- couverture publiée comme artefact CI ;
- lint et build React verts ;
- modèle et métriques présents ;
- README et notes de version à jour ;
- aucun secret ou fichier `.env` versionné.

## Livraison locale

```bash
docker compose build
docker compose up -d
curl http://localhost:8000/health
```

Vérifier ensuite `/docs`, une prédiction JPG, un rejet de fichier texte et `/stats/`.

## Version GitHub

```bash
git tag -a v1.0.0 -m "ECO-TRI IA - MVP soutenance"
git push origin v1.0.0
```

Créer une release GitHub avec :

- résumé des fonctions ;
- métriques du modèle ;
- procédure de lancement ;
- limites connues ;
- lien vers la CI verte.

## Retour arrière

Conserver la release précédente et son modèle. En cas d'échec, redéployer le tag
précédent puis ouvrir un incident avec les logs et la commande de reproduction.
