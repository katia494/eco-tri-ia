\# Guide de contribution - ECO-TRI



\## Convention des commits



feat() - nouvelle fonctionnalite

fix() - correction de bug

docs() - documentation

test() - tests unitaires

refactor() - refactorisation



\## Exemples de commits



feat(api): ajouter endpoint de prediction

fix(database): corriger la connexion PostgreSQL

docs(readme): mettre a jour le README

test(api): ajouter tests pour /predict



\## Workflow Git



1\. Creer une branche pour chaque fonctionnalite

2\. Ecrire les tests avant le code

3\. Faire un commit par fonctionnalite

4\. Pusher et verifier que le CI est vert



\## Structure du projet



backend/api/     - Code de l'API FastAPI

backend/models/  - Modeles IA et preprocessing

tests/           - Tests unitaires

docs/            - Documentation

notebooks/       - Analyse des donnees

