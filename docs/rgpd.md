# Conformité RGPD – ECO-TRI

> **Projet** : ECO-TRI — Application de classification de déchets par IA  
> **Auteure** : Katia Boussad – Formation Dev IA, Simplon  
> **Date** : Août 2026

---

## 1. Nature des données traitées

ECO-TRI traite **uniquement des images de déchets** (carton, verre, métal, papier, plastique, ordures).

| Type de donnée | Exemple | Donnée personnelle ? |
|---|---|---|
| Image du dataset | `paper013.jpg` | Non |
| Catégorie | `paper`, `glass` | Non |
| Résultat de prédiction | `plastic`, confiance 0,94 | Non |
| Date de prédiction | `2026-08-28 10:42` | Non |

Les images envoyées peuvent toutefois contenir accidentellement une personne ou
un élément identifiable. Elles sont traitées en mémoire puis supprimées : elles ne
sont pas écrites sur disque.

## 2. Source des données

| Élément | Détail |
|---|---|
| Nom | Garbage Classification |
| Auteur Kaggle | `asdasdasasdas` |
| Licence annoncée sur la fiche | CC0 – Domaine public |
| Lien | <https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification> |
| Nombre vérifié | 2 527 images |
| Catégories | cardboard, glass, metal, paper, plastic, trash |

## 3. Finalité du traitement
Les données sont utilisées uniquement pour :

- entraîner un modèle de classification de déchets ;
- valider ses performances ;
- démontrer l'application ECO-TRI.

## 4. Données générées par l'application

| Action | Traitement |
|---|---|
| Analyse | l'image est lue en mémoire, sans sauvegarde |
| Réponse | catégorie, confiance, version du modèle et consigne de tri |
| Historique | catégorie, confiance et date uniquement |

## 5. Mesures et limites

- **Minimisation** : aucune image utilisateur n'est conservée.
- **Transparence** : l'interface doit informer l'utilisateur du traitement.
- **Sécurité** : une terminaison HTTPS devra être configurée sur l'hébergeur ; le
  conteneur local expose actuellement HTTP.
- **Conservation** : l'historique SQLite doit disposer d'une durée de conservation
  avant une mise en production réelle.
