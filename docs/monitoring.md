# Monitoring du modèle et de l'application

## Différence entre les deux suivis

- Monitoring applicatif : disponibilité, codes HTTP, erreurs et latence.
- Monitoring modèle : confiance, distribution des classes et qualité sur un jeu annoté.

## Métriques et seuils

| Métrique | Seuil d'alerte | Action |
|---|---:|---|
| `/health` indisponible | 1 échec | Vérifier processus, modèle et logs |
| Taux d'erreurs 5xx | > 5 % sur 5 min | Examiner la trace et reproduire |
| Latence `/predict` | > 2 000 ms | Vérifier CPU, taille d'image et charge |
| Confiance faible | > 20 % sous 0,50 | Analyser images et dérive possible |
| Classe dominante | > 60 % sur une période | Vérifier biais d'usage ou du modèle |
| Accuracy test annoté | < 85 % | Bloquer la nouvelle version du modèle |

## Données disponibles

Le middleware journalise méthode, route, statut et durée. SQLite permet de calculer
le nombre de prédictions, la confiance moyenne et la répartition des classes.
L'image source n'est pas enregistrée.

La route `/stats/monitoring` agrège pour le processus courant : nombre de
requêtes, taux d'erreur, latence moyenne/maximale, statuts HTTP, endpoints
appelés, nombre de prédictions incertaines et seuils d'alerte. Les compteurs
applicatifs sont réinitialisés au redémarrage ; SQLite conserve les métadonnées
de prédiction.

## Procédure

1. Appeler `/health` régulièrement.
2. Consulter `/stats/`, `/stats/by-class` et `/stats/monitoring`.
3. Chercher les erreurs et latences anormales dans les logs.
4. Rejouer un test contrôlé.
5. Documenter tout incident et ajouter un test de non-régression.

## Évolution

Prometheus/Grafana ou un service équivalent pourra remplacer l'observation locale.
Le MVP documente les métriques et expose les données nécessaires sans prétendre
disposer déjà d'un système d'alertes en production.
