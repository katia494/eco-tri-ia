-- ============================================================
-- Requêtes SQL vérifiées — ECO-TRI
-- C2 : exploration, agrégation et contrôle du catalogue C4
-- ============================================================

-- 1. Sources collectées et nombre de liens de provenance.
SELECT
    s.code,
    s.nom,
    s.role_dans_projet,
    COUNT(ds.dechet_id) AS liens_provenance
FROM sources_donnees AS s
LEFT JOIN dechet_sources AS ds
    ON ds.source_id = s.id
GROUP BY s.id, s.code, s.nom, s.role_dans_projet
ORDER BY s.code;

-- 2. Répartition des images canoniques par catégorie.
SELECT
    categorie,
    COUNT(*) AS images_canoniques,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pourcentage
FROM dechets
GROUP BY categorie
ORDER BY images_canoniques DESC;

-- 3. Nombre d'images uniques et de liens de provenance.
SELECT
    (SELECT COUNT(*) FROM dechets) AS images_canoniques,
    (SELECT COUNT(*) FROM dechet_sources) AS liens_provenance,
    (
        (SELECT COUNT(*) FROM dechet_sources)
        - (SELECT COUNT(*) FROM dechets)
    ) AS doublons_traces_sans_duplication;

-- 4. Images observées dans plusieurs sources.
SELECT
    d.id,
    d.nom_fichier,
    d.categorie,
    COUNT(DISTINCT ds.source_id) AS nombre_sources
FROM dechets AS d
JOIN dechet_sources AS ds
    ON ds.dechet_id = d.id
GROUP BY d.id, d.nom_fichier, d.categorie
HAVING COUNT(DISTINCT ds.source_id) > 1
ORDER BY nombre_sources DESC, d.id
LIMIT 20;

-- 5. Vérification de l'intégrité : aucun lien orphelin attendu.
SELECT
    COUNT(*) AS liens_orphelins
FROM dechet_sources AS ds
LEFT JOIN dechets AS d
    ON d.id = ds.dechet_id
LEFT JOIN sources_donnees AS s
    ON s.id = ds.source_id
WHERE d.id IS NULL OR s.id IS NULL;

-- 6. Vérification de complétude des métadonnées du catalogue.
SELECT
    COUNT(*) AS total_images,
    SUM(CASE WHEN contenu_sha256 IS NOT NULL THEN 1 ELSE 0 END) AS avec_sha256,
    SUM(CASE WHEN source_id IS NOT NULL THEN 1 ELSE 0 END) AS avec_source,
    SUM(CASE WHEN date_ajout IS NOT NULL THEN 1 ELSE 0 END) AS avec_date_import
FROM dechets;

-- 7. Détail des six catégories et de leur source canonique.
SELECT
    s.code AS source_canonique,
    d.categorie,
    COUNT(*) AS nombre_images
FROM dechets AS d
JOIN sources_donnees AS s
    ON s.id = d.source_id
GROUP BY s.code, d.categorie
ORDER BY s.code, d.categorie;

-- 8. Historique des prédictions, si l'application en contient.
SELECT
    image_name,
    waste_class,
    ROUND(confidence * 100, 1) AS confiance_pct,
    created_at
FROM predictions
ORDER BY created_at DESC
LIMIT 20;

-- 9. Vue réutilisable pour le suivi de la distribution.
CREATE VIEW IF NOT EXISTS vue_distribution_catalogue AS
SELECT
    categorie,
    COUNT(*) AS nombre_images,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pourcentage
FROM dechets
GROUP BY categorie;