# Carte finale des preuves C1-C21

| Compétence | Preuve principale | État après stabilisation |
|---|---|---|
| C1 | `scripts/download_dataset.py`, source et licence documentées | Couvert ; conserver une capture d'exécution sur un environnement Kaggle configuré |
| C2 | `sql/queries.sql` | Couvert |
| C3 | notebook de nettoyage, dataset traité | Couvert |
| C4 | `sql/schema.sql`, `src/import_data.py`, `docs/rgpd.md` | Couvert, schéma à illustrer en slide |
| C5 | routes FastAPI, `/docs`, tests API | Couvert |
| C6 | `docs/veille.md` | Couvert documentaire |
| C7 | `docs/benchmark.md`, métriques réelles | Couvert |
| C8 | `.env.example`, scripts d'entraînement | Couvert |
| C9 | `/predict`, `/model/info`, validations | Couvert |
| C10 | `frontend/src/Scan/Scan.jsx`, build React | Couvert |
| C11 | `reports/model`, `docs/monitoring.md` | Partiel : suivi continu à démontrer |
| C12 | `tests/`, commande pytest | Couvert |
| C13 | `.github/workflows/ci.yml` | À confirmer par une exécution verte |
| C14 | `docs/user_stories.md` | Couvert |
| C15 | `docs/technical_specifications.md` | Couvert |
| C16 | `docs/project_management.md`, historique Git | Partiel : ajouter issues/Kanban |
| C17 | application React/FastAPI et tests | Couvert |
| C18 | workflow tests/lint/build | À confirmer par une exécution verte |
| C19 | Dockerfile, `docs/release.md` | Partiel : créer tag et release |
| C20 | logs, stats et `docs/monitoring.md` | Partiel : capture et seuils à démontrer |
| C21 | `docs/incident_report.md`, tests | Couvert après commit de correction |

Une compétence n'est déclarée validée à la soutenance que si la commande ou la
preuve visuelle correspondante est montrée. Les états « partiel » restent annoncés
honnêtement jusqu'à production de la dernière preuve.
