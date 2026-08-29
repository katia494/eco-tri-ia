-- ============================================================
-- Schéma de la base de données ECO-TRI
-- Compétence C4 : Conception et création de la base de données
-- Dataset source : Kaggle – Garbage Classification (asdasdasasdas)
-- ============================================================

-- Table 1 : Catalogue de toutes les images du dataset
CREATE TABLE IF NOT EXISTS dechets (
    id           SERIAL PRIMARY KEY,
    nom_fichier  VARCHAR(255) NOT NULL,
    categorie    VARCHAR(50)  NOT NULL,
    chemin_image TEXT,
    source       VARCHAR(100) DEFAULT 'Kaggle-GarbageClassification',
    date_ajout   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- Table 2 : Prédictions faites par le modèle IA
CREATE TABLE IF NOT EXISTS predictions (
    id                SERIAL PRIMARY KEY,
    image_path        TEXT,
    categorie_predite VARCHAR(50) NOT NULL,
    confiance         DECIMAL(5, 4),
    date_prediction   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 3 : Statistiques par catégorie
CREATE TABLE IF NOT EXISTS statistiques_categories (
    id                    SERIAL PRIMARY KEY,
    categorie             VARCHAR(50) UNIQUE NOT NULL,
    nombre_images         INTEGER    DEFAULT 0,
    pourcentage           DECIMAL(5, 2),
    derniere_mise_a_jour  TIMESTAMP  DEFAULT CURRENT_TIMESTAMP
);

-- ── Index pour accélérer les recherches ────────────────────
CREATE INDEX IF NOT EXISTS idx_dechets_categorie
    ON dechets (categorie);

CREATE INDEX IF NOT EXISTS idx_predictions_categorie
    ON predictions (categorie_predite);

CREATE INDEX IF NOT EXISTS idx_predictions_date
    ON predictions (date_prediction);

-- ── Données initiales : statistiques du dataset Kaggle ─────
INSERT INTO statistiques_categories (categorie, nombre_images, pourcentage)
VALUES
    ('paper',     584, 24.96),
    ('glass',     501, 21.43),
    ('plastic',   472, 20.19),
    ('metal',     410, 17.54),
    ('cardboard', 403, 17.23),
    ('trash',     137,  5.86)
ON CONFLICT (categorie) DO NOTHING;
