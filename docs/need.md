# Expression du besoin IA – ECO-TRI

> **Auteure** : Katia Boussad – Formation Dev IA, Simplon  
> **Date** : Août 2026

---

## 1. Contexte métier

Les déchets mal triés représentent un problème environnemental majeur.  
ECO-TRI est une application qui aide les citoyens à **trier correctement leurs déchets**  
en prenant une photo et en recevant instantanément la catégorie du déchet.

---

## 2. Entrées / sorties du service IA

| Élément | Détail |
|---|---|
| Entrée | Une image JPG ou PNG d'un déchet |
| Sortie | Catégorie prédite, confiance, version du modèle, consigne de tri |
| Exemple | Image de bouteille → `plastic`, confiance 0,94 |

## 3. Contraintes

| Contrainte | Détail |
|---|---|
| Coût | Modèle local, sans API d'IA payante |
| Vie privée | Aucune image envoyée n'est conservée |
| Latence | Objectif inférieur à 2 secondes après le chargement du modèle |
| Accessibilité | Interface web simple et responsive |
| Sécurité | Aucun secret dans le dépôt |

## 4. Critères de réussite mesurables

- accuracy sur le jeu de test supérieure à 80 % ;
- macro F1 supérieure à 80 % ;
- réponse API inférieure à 2 secondes à chaud ;
- fichiers non-images et fichiers trop volumineux refusés ;
- six catégories présentes dans l'évaluation ;
- parcours principal utilisable sur mobile.

Le test indépendant actuel atteint **91,15 % d'accuracy** et **90,47 % de
macro F1** sur 384 images. Le temps à froid mesuré localement est de 1,93 seconde ;
une mesure à chaud et une capture restent à joindre aux preuves de soutenance.
