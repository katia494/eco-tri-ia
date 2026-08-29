# Besoin applicatif et user stories

## Acteurs

- Utilisateur : souhaite identifier rapidement une catégorie de déchet.
- Administratrice/développeuse : surveille l'API, les erreurs et la qualité du modèle.

## Parcours principal

1. L'utilisateur ouvre l'écran de scan.
2. Il choisit ou capture une image.
3. L'application contrôle le fichier et l'envoie à l'API.
4. Le modèle retourne une classe et une confiance.
5. L'application présente une consigne de tri compréhensible.

## User stories et critères d'acceptation

### US1 - Classifier une image

En tant qu'utilisateur, je veux envoyer une photo d'un déchet afin d'obtenir sa catégorie.

- JPG et PNG sont acceptés.
- Un fichier vide, invalide ou supérieur à 10 Mo est refusé clairement.
- La réponse contient classe, confiance, version du modèle et consigne.
- La classe appartient aux six catégories documentées.

### US2 - Comprendre le résultat

En tant qu'utilisateur, je veux voir le niveau de confiance et une consigne afin de décider correctement.

- La confiance est comprise entre 0 et 1.
- Une confiance faible est présentée comme une incertitude et non comme une certitude.
- Le texte reste lisible sur mobile et utilisable au clavier.

### US3 - Consulter l'historique

En tant qu'administratrice, je veux consulter les prédictions afin d'observer l'usage.

- L'image n'est jamais conservée.
- Seules les métadonnées utiles sont enregistrées.
- Les statistiques par classe sont accessibles par l'API.

### US4 - Diagnostiquer l'application

En tant qu'administratrice, je veux un healthcheck et des logs afin de détecter une anomalie.

- `/health` répond sans lancer une inférence.
- Chaque requête produit un statut et une durée dans les logs.
- Les seuils sont définis dans `monitoring.md`.
