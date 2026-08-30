-- ============================================================
-- Requêtes SQL – ECO-TRI
-- Compétence C2 : Requêtes d'exploration et d'analyse
-- ============================================================

-- 1. Nombre d'images par catégorie
SELECT
    categorie,
    COUNT(*) AS nombre_images,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pourcentage
FROM dechets
GROUP BY categorie
ORDER BY nombre_images DESC;

-- 2. Statistiques globales du dataset
SELECT
    COUNT(*)                  AS total_images,
    COUNT(DISTINCT categorie) AS nombre_categories,
    MIN(date_ajout)           AS premiere_entree,
    MAX(date_ajout)           AS derniere_entree
FROM dechets;

-- 3. Recherche d'images par catégorie (exemple : plastic)
SELECT nom_fichier, categorie, date_ajout
FROM dechets
WHERE categorie = 'plastic'
ORDER BY date_ajout DESC
LIMIT 10;

-- 4. Précision moyenne des prédictions IA par catégorie
SELECT
    waste_class,
    COUNT(*) AS nombre_predictions,
    ROUND(AVG(confidence) * 100, 2) AS confiance_moyenne_pct,
    ROUND(MAX(confidence) * 100, 2) AS meilleure_confiance_pct,
    ROUND(MIN(confidence) * 100, 2) AS moins_bonne_confiance_pct
FROM predictions
GROUP BY waste_class
ORDER BY confiance_moyenne_pct DESC;

-- 5. Catégories sous-représentées (moins de 200 images)
SELECT categorie, COUNT(*) AS nombre
FROM dechets
GROUP BY categorie
HAVING COUNT(*) < 200
ORDER BY nombre ASC;

-- 6. Les 20 dernières prédictions
SELECT
    image_name,
    waste_class,
    ROUND(confidence * 100, 1) AS confiance_pct,
    created_at
FROM predictions
ORDER BY created_at DESC
LIMIT 20;

-- 7. Vue : distribution complète pour les graphiques
CREATE VIEW IF NOT EXISTS vue_distribution AS
SELECT
    categorie,
    COUNT(*) AS nombre,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pourcentage
FROM dechets
GROUP BY categorie
ORDER BY nombre DESC;

-- 8. Recherche par nom de fichier
SELECT id, nom_fichier, categorie, date_ajout
FROM dechets
WHERE nom_fichier LIKE 'glass%'
ORDER BY nom_fichier
LIMIT 5;
