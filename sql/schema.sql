-- ============================================================
-- Schéma de la base de données ECO-TRI
-- Compétence C4 : Conception et création de la base de données
-- Moteur retenu : SQLite
-- Dataset source : Kaggle – Garbage Classification (asdasdasasdas)
-- ============================================================

-- Table 1 : Catalogue de toutes les images du dataset
CREATE TABLE IF NOT EXISTS dechets (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_fichier  TEXT NOT NULL,
    categorie    TEXT NOT NULL,
    chemin_image TEXT,
    source       TEXT DEFAULT 'Kaggle-GarbageClassification',
    date_ajout   TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(nom_fichier, categorie)
);

-- Table 2 : Prédictions faites par le modèle IA
CREATE TABLE IF NOT EXISTS predictions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    image_name  TEXT NOT NULL,
    waste_class TEXT NOT NULL,
    confidence  REAL NOT NULL CHECK(confidence BETWEEN 0 AND 1),
    created_at  TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Table 3 : Statistiques par catégorie
CREATE TABLE IF NOT EXISTS statistiques_categories (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    categorie             TEXT UNIQUE NOT NULL,
    nombre_images         INTEGER DEFAULT 0,
    pourcentage           REAL,
    derniere_mise_a_jour  TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ── Index pour accélérer les recherches ────────────────────
CREATE INDEX IF NOT EXISTS idx_dechets_categorie
    ON dechets (categorie);

CREATE INDEX IF NOT EXISTS idx_predictions_categorie
    ON predictions (waste_class);

CREATE INDEX IF NOT EXISTS idx_predictions_date
    ON predictions (created_at);

-- ── Données initiales : statistiques du dataset Kaggle ─────
INSERT INTO statistiques_categories (categorie, nombre_images, pourcentage)
VALUES
    ('paper',     594, 23.51),
    ('glass',     501, 19.83),
    ('plastic',   482, 19.07),
    ('metal',     410, 16.22),
    ('cardboard', 403, 15.95),
    ('trash',     137,  5.42)
ON CONFLICT (categorie) DO NOTHING;
