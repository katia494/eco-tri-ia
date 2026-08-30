# Rapport technique - ECO-TRI IA

## Objectif

ECO-TRI aide un utilisateur à identifier une catégorie de déchet depuis une
photographie. L'application retourne une classe, un niveau de confiance et une
consigne, sans conserver l'image.

## Données

Le dataset Garbage Classification contient 2 527 images brutes réparties entre carton,
verre, métal, papier, plastique et déchet non recyclable. Un script déterministe
réalise un split 70/15/15 avec la graine 42.

## Modèle

Le modèle final est YOLOv8n-cls préentraîné puis adapté aux six classes. La
classification a été choisie car une seule étiquette est attendue par image et le
dataset ne possède pas de bounding boxes.

Le modèle v1 atteint sur 384 images de test **91,15 % d'accuracy** et
**90,47 % de macro F1**. Un audit SHA-256 ultérieur a détecté trois copies
mal étiquetées entre classes. Le pipeline v2 les exclut et retient 2 524 images ;
le modèle devra être réentraîné avant d'attribuer ces métriques à la v2. Les résultats v1 sont versionnés dans
`reports/model`.

## Application

- FastAPI expose le modèle et documente le contrat OpenAPI ;
- React/Vite fournit l'interface de scan ;
- SQLAlchemy/SQLite stocke uniquement les métadonnées ;
- les fichiers sont validés par MIME, contenu et taille ;
- un middleware journalise statut et durée ;
- 28 tests backend passent avec 86 % de couverture ;
- 3 tests métier frontend, le lint et le build passent ;
- ESLint et le build Vite passent localement.

## Livraison

GitHub Actions vérifie backend et frontend. Le Dockerfile utilise une image Python
non privilégiée, PyTorch CPU et un healthcheck. La procédure complète est décrite
dans `guide_deploiement.md` et `release.md`.

## Limites

Le modèle ne connaît que six classes, le jeu `trash` est plus petit et une image
hors distribution peut être mal classée. Le monitoring continu et un jeu de photos
prises par smartphone constituent les principales évolutions.
