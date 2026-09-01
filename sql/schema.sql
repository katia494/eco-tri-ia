-- ============================================================
-- Schéma SQLite versionné — ECO-TRI
-- C4 : catalogue multi-source, dédoublonnage et traçabilité
-- ============================================================

PRAGMA foreign_keys = ON;

-- Référentiel des sources collectées dans C1.
CREATE TABLE IF NOT EXISTS sources_donnees (
    id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    code                   TEXT NOT NULL UNIQUE,
    nom                    TEXT NOT NULL,
    fournisseur            TEXT NOT NULL,
    url                    TEXT NOT NULL,
    licence                TEXT NOT NULL,
    role_dans_projet       TEXT NOT NULL,
    contient_donnees_perso INTEGER NOT NULL DEFAULT 0
        CHECK (contient_donnees_perso IN (0, 1)),
    cree_le                TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO sources_donnees
    (code, nom, fournisseur, url, licence, role_dans_projet, contient_donnees_perso)
VALUES
    (
        'garbage_classification_v1',
        'Garbage Classification',
        'Kaggle',
        'https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification',
        'Licence à consulter et respecter sur Kaggle',
        'training_historical_v2',
        0
    ),
    (
        'garbage_classification_v2',
        'Garbage Classification V2',
        'Kaggle',
        'https://www.kaggle.com/datasets/sumn2u/garbage-classification-v2',
        'Licence à consulter et respecter sur Kaggle',
        'training_extension_v3',
        0
    ),
    (
        'realwaste',
        'RealWaste',
        'GitHub - dataset scientifique',
        'https://github.com/sam-single/realwaste',
        'CC BY-NC-SA 4.0',
        'external_evaluation_only',
        0
    );

-- Une ligne par image physiquement unique.
CREATE TABLE IF NOT EXISTS dechets (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    contenu_sha256  TEXT NOT NULL UNIQUE CHECK(length(contenu_sha256) = 64),
    nom_fichier     TEXT NOT NULL,
    categorie       TEXT NOT NULL
        CHECK(categorie IN ('cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash')),
    chemin_image    TEXT NOT NULL,
    source_id       INTEGER NOT NULL,
    source          TEXT NOT NULL,
    date_ajout      TEXT NOT NULL,
    FOREIGN KEY (source_id) REFERENCES sources_donnees(id)
);

-- Une image peut provenir de plusieurs sources.
-- Les doublons exacts sont donc tracés sans créer une seconde image canonique.
CREATE TABLE IF NOT EXISTS dechet_sources (
    dechet_id            INTEGER NOT NULL,
    source_id            INTEGER NOT NULL,
    chemin_source        TEXT NOT NULL,
    nom_fichier_source   TEXT NOT NULL,
    categorie_source     TEXT NOT NULL
        CHECK(categorie_source IN ('cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash')),
    date_import          TEXT NOT NULL,
    PRIMARY KEY (dechet_id, source_id, chemin_source),
    FOREIGN KEY (dechet_id) REFERENCES dechets(id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES sources_donnees(id)
);

-- Historique minimal des prédictions utilisateur.
CREATE TABLE IF NOT EXISTS predictions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    image_name  TEXT NOT NULL,
    waste_class TEXT NOT NULL
        CHECK(waste_class IN ('cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash')),
    confidence  REAL NOT NULL CHECK(confidence BETWEEN 0 AND 1),
    created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Agrégats par catégorie pour le suivi.
CREATE TABLE IF NOT EXISTS statistiques_categories (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    categorie            TEXT NOT NULL UNIQUE
        CHECK(categorie IN ('cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash')),
    nombre_images        INTEGER NOT NULL DEFAULT 0 CHECK(nombre_images >= 0),
    pourcentage          REAL CHECK(pourcentage BETWEEN 0 AND 100),
    derniere_mise_a_jour TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index de recherche et de jointure.
CREATE INDEX IF NOT EXISTS idx_dechets_categorie
    ON dechets (categorie);

CREATE INDEX IF NOT EXISTS idx_dechets_source_id
    ON dechets (source_id);

CREATE INDEX IF NOT EXISTS idx_dechet_sources_source_id
    ON dechet_sources (source_id);

CREATE INDEX IF NOT EXISTS idx_predictions_categorie
    ON predictions (waste_class);

CREATE INDEX IF NOT EXISTS idx_predictions_date
    ON predictions (created_at);