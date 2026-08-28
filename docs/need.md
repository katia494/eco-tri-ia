# Expression du besoin IA – ECO-TRI

> **Auteure** : Katia Boussad – Formation Dev IA, Simplon  
> **Date** : Août 2026

---

## 1. Contexte métier

Les déchets mal triés représentent un problème environnemental majeur.  
ECO-TRI est une application qui aide les citoyens à **trier correctement leurs déchets**  
en prenant une photo et en recevant instantanément la catégorie du déchet.

---

## 2. Entrées / Sorties du service IA
Élément	Détail
Entrée	Une image JPG/PNG d'un déchet
Sortie	Catégorie prédite + score de confiance (0 à 1)
Exemple	Image de bouteille → plastic – 94%

. Contraintes
Contrainte	Détail
Coût	Gratuit — modèle local, pas d'API payante
RGPD	Aucune image conservée sur le serveur
Latence	Réponse en moins de 2 secondes
Accessibilité	Interface web simple, utilisable sur mobile
Sécurité	Pas de clé API exposée dans le code

4. Critères de réussite
✅ Le modèle prédit la bonne catégorie dans plus de 80% des cas
✅ L'API répond en moins de 2 secondes
✅ L'interface est utilisable sans formation
✅ Les 6 catégories sont toutes reconnues

