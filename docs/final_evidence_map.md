# Carte finale des preuves C1-C21

| Compétence | Preuve principale | État après stabilisation |
|---|---|---|
| C1 | `scripts/download_dataset.py`, source documentée | Technique couverte ; capture d'exécution à faire à la fin |
| C2 | `sql/queries.sql`, `scripts/export_sql_evidence.py` | Technique couverte ; CSV/capture à générer à la fin |
| C3 | `scripts/audit_dataset.py`, `reports/data_quality.json`, exclusions | Couvert : 2 527 lisibles, 3 copies contradictoires exclues du pipeline v2 |
| C4 | schéma SQLite, import, dictionnaire, RGPD | Couvert : moteur, chemin et colonnes harmonisés |
| C5 | routes FastAPI, `/docs`, tests API | Couvert |
| C6 | `docs/veille.md` | Couvert : sources officielles, fiabilité, fréquence et décision |
| C7 | `docs/benchmark.md`, métriques réelles | Couvert |
| C8 | `.env.example`, scripts d'entraînement | Couvert |
| C9 | `/predict`, `/model/info`, validations | Couvert |
| C10 | `frontend/src/Scan/Scan.jsx`, build React | Couvert |
| C11 | rapports modèle, seuil d'incertitude, `/stats/monitoring` | Technique couverte ; jeu externe et capture à finaliser |
| C12 | 28 tests backend, 3 tests frontend | Couvert localement |
| C13 | `.github/workflows/ci.yml` | Première PR verte ; nouvelle branche à publier et revérifier |
| C14 | `docs/user_stories.md` | Couvert |
| C15 | `docs/technical_specifications.md` | Couvert |
| C16 | backlog, sprints, issues GitHub #2 à #5 | Presque couvert ; organiser la vue Kanban |
| C17 | application React/FastAPI et tests métier | Couvert |
| C18 | workflow backend/frontend/Docker | Couvert localement ; exécution GitHub de la branche requise |
| C19 | Dockerfile, `docs/release.md` | Partiel : créer tag et release |
| C20 | logs, `/stats/monitoring`, seuils | Technique couverte ; capture à faire à la fin |
| C21 | `docs/incident_report.md`, tests | Couvert après commit de correction |

Une compétence n'est déclarée validée à la soutenance que si la commande ou la
preuve visuelle correspondante est montrée. Les états « partiel » restent annoncés
honnêtement jusqu'à production de la dernière preuve.
