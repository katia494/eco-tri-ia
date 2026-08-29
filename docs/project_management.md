# Organisation agile de la reprise individuelle

## Contexte

Le projet a commencé en groupe puis a été repris individuellement par Katia
Boussad. La reprise a nécessité un audit, une réduction du périmètre et une
harmonisation du modèle, du code et de la documentation.

## Rôle

Katia assure les rôles de product owner, développeuse IA, développeuse API,
intégratrice frontend et responsable qualité. Cette organisation individuelle est
rendue visible par le backlog et les commits ; elle ne prétend pas simuler une équipe.

## Backlog priorisé

| Priorité | Élément | Définition de fini |
|---|---|---|
| P0 | Unifier le modèle | Un modèle réel, métriques et code cohérents |
| P0 | Rétablir l'API | `/health`, `/predict` et erreurs testés |
| P0 | Rétablir le frontend | lint et build verts |
| P0 | Rétablir la CI | tests, couverture et build automatiques |
| P1 | Livrer | Dockerfile, procédure, tag et release |
| P1 | Prouver C1-C21 | documents et liens vers les fichiers |
| P2 | Fonctions secondaires | profil, chatbot et gamification réels |

## Sprints de stabilisation

### Sprint 1 - Produit fonctionnel

- dataset reproductible ;
- entraînement YOLOv8n-cls ;
- intégration FastAPI ;
- réparation React ;
- tests automatisés.

### Sprint 2 - Livraison et soutenance

- CI/CD ;
- Docker et release ;
- monitoring ;
- incident et non-régression ;
- carte finale des preuves.

## Rituels adaptés au travail individuel

- début de session : objectif et priorité ;
- fin de session : tests, commit et mise à jour du backlog ;
- revue : démonstration du parcours complet ;
- rétrospective : ce qui a fonctionné, blocages et décision suivante.
