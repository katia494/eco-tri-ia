# Compétences couvertes — ECO-TRI

**Auteur :** Katia Boussad
**Formation :** Dev IA — Simplon ECE 2024

---

## Bloc 1 — Développement IA
#	Compétence	Fichier(s)	Preuve
C1	Concevoir une architecture logicielle	backend/api/main.py	Structure FastAPI complète
C2	Développer une API REST	backend/api/routes.py	Endpoints /predict, /predictions
C3	Gérer un environnement de développement	requirements.txt, venv	Environnement virtuel Python
C4	Conteneuriser une application	Dockerfile, docker-compose.yml	Docker complet
C5	Documenter une API	backend/api/main.py	Swagger auto-généré /docs
C6	Connecter une base de données	backend/api/database.py	SQLAlchemy + PostgreSQL/SQLite
C7	Analyser des données	notebooks/analyse_dechets.ipynb	Analyse exploratoire complète
C8	Prétraiter des données	backend/models/preprocess.py	Normalisation et validation images

Bloc 2 — IA et Machine Learning
#	Compétence	Fichier(s)	Preuve
C9	Implémenter un modèle IA	backend/api/predict.py	YOLOv8 classification déchets
C10	Évaluer un modèle IA	notebooks/analyse_dechets.ipynb	Métriques : précision 87%, mAP 89%
C11	Gérer les données d'entraînement	notebooks/analyse_dechets.ipynb	Distribution des 6 classes
C12	Optimiser un modèle	backend/api/predict.py	Mode simulation + mode réel
C13	Déployer un modèle IA	backend/api/routes.py	Endpoint /predict en production
Bloc 3 — Qualité et DevOps
#	Compétence	Fichier(s)	Preuve
C14	Écrire des tests unitaires	tests/test_api.py	5 tests endpoints FastAPI
C15	Mesurer la couverture de code	pytest.ini	pytest-cov configuré
C16	Mettre en place un CI/CD	.github/workflows/ci.yml	GitHub Actions vert ✅
C17	Logger une application	backend/api/logger.py	Logs avec timestamp
C18	Gérer les erreurs	backend/api/exceptions.py	Exceptions personnalisées
C19	Sécuriser une API	backend/api/security.py	Authentification par clé API
C20	Optimiser les performances	backend/api/cache.py	Cache en mémoire
C21	Rédiger la documentation technique	docs/rapport_technique.md	Rapport complet + guide déploiement
Résumé
Bloc	Compétences	Statut
Développement IA	C1 à C8	✅ 8/8
IA et Machine Learning	C9 à C13	✅ 5/5
Qualité et DevOps	C14 à C21	✅ 8/8
TOTAL	21 compétences	✅ 21/21