# Conformité RGPD – ECO-TRI

> **Projet** : ECO-TRI — Application de classification de déchets par IA  
> **Auteure** : Katia Boussad – Formation Dev IA, Simplon  
> **Date** : Août 2026

---

## 1. Nature des données traitées

ECO-TRI traite **uniquement des images de déchets** (carton, verre, métal, papier, plastique, ordures).

Type de donnée	Exemple	Données personnelles ?
Images de déchets	paper013.jpg	❌ Non
Catégorie du déchet	paper, glass	❌ Non
Résultat de prédiction	plastic – 94 %	❌ Non
Date de prédiction	2026-08-28 10:42	❌ Non
✅ ECO-TRI ne collecte aucune donnée personnelle.

2. Source des données
Élément	Détail
Nom du dataset	Garbage Classification
Auteur Kaggle	cchangcs
Licence	CC0 – Domaine public
Lien	https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification
Nombre d'images	2 467 images réelles
Catégories	6 : cardboard, glass, metal, paper, plastic, trash

3. Finalité du traitement
Les données sont utilisées uniquement pour :

Entraîner un modèle de classification de déchets
Valider les performances du modèle
Démontrer le fonctionnement de l'application ECO-TRI

4. Données générées par l'application
Action	Ce qui est stocké
Analyse l'image	❌ L'image n'est PAS sauvegardée
Retourne la catégorie	✅ Catégorie + confiance retournées
Log de la prédiction	✅ Catégorie + confiance + date
💡 Aucune image envoyée par un utilisateur n'est conservée sur le serveur.

5. Droits des utilisateurs
Minimisation : seules les données nécessaires sont traitées
Finalité : uniquement pour la classification de déchets
Transparence : ce document explique clairement le traitement
Sécurité : API accessible uniquement via HTTPS en production 