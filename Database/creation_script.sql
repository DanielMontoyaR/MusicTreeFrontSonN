Vivi_sr2010CREATE TYPE key_type AS ENUM ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '-1');
CREATE TYPE time_signature_type AS ENUM ('0', '2', '3', '4', '5', '6', '7', '8');

-- Genre clusters table
CREATE TABLE genre_clusters (
    cluster_id VARCHAR(15) PRIMARY KEY DEFAULT 'C-' || substr(md5(random()::text), 0, 12),
    name VARCHAR(30) NOT NULL,
    description VARCHAR(300),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT cluster_name_unique UNIQUE (name),
    CONSTRAINT cluster_id_format CHECK (cluster_id ~ '^C-[A-Za-z0-9]{12}$')
);

-- Main genres table
CREATE TABLE genres (
    genre_id VARCHAR(27) PRIMARY KEY DEFAULT 'G-' || substr(md5(random()::text), 0, 12) || 'S-000000000000',
    name VARCHAR(30) NOT NULL,
    description VARCHAR(1000),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    color VARCHAR(7) CHECK (color ~ '^#[A-Fa-f0-9]{6}$'),
    creation_year INTEGER,
    country_of_origin VARCHAR(100),
    average_mode DECIMAL(3,2) CHECK (average_mode BETWEEN 0 AND 1),
    bpm_lower INTEGER CHECK (bpm_lower BETWEEN 0 AND 250),
    bpm_upper INTEGER CHECK (bpm_upper BETWEEN 0 AND 250),
    dominant_key key_type,
    typical_volume DECIMAL(5,2) CHECK (typical_volume BETWEEN -60 AND 0),
    time_signature time_signature_type,
    average_duration INTEGER CHECK (average_duration BETWEEN 0 AND 3600),
    is_subgenre BOOLEAN NOT NULL DEFAULT FALSE,
    parent_genre_id VARCHAR(27) REFERENCES genres(genre_id),
    cluster_id VARCHAR(15) REFERENCES genre_clusters(cluster_id),
    CONSTRAINT bpm_range CHECK (bpm_lower <= bpm_upper),
    CONSTRAINT subgenre_color CHECK (
        (is_subgenre = TRUE AND color IS NULL) OR 
        (is_subgenre = FALSE)
    ),
    CONSTRAINT subgenre_parent CHECK (
        (is_subgenre = TRUE AND parent_genre_id IS NOT NULL) OR
        (is_subgenre = FALSE AND parent_genre_id IS NULL)
    ),
    CONSTRAINT genre_name_unique UNIQUE (name, parent_genre_id)
);

-- Genre relationships table
CREATE TABLE genre_relationships (
    relationship_id SERIAL PRIMARY KEY,
    source_genre_id VARCHAR(27) NOT NULL REFERENCES genres(genre_id),
    target_genre_id VARCHAR(27) NOT NULL REFERENCES genres(genre_id),
    influence_level INTEGER NOT NULL DEFAULT 5 CHECK (influence_level BETWEEN 1 AND 10),
    mgpc_score DECIMAL(5,4),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT no_self_relationship CHECK (source_genre_id != target_genre_id),
    CONSTRAINT unique_relationship UNIQUE (source_genre_id, target_genre_id)
);

-- Configuration for MGPC weights
CREATE TABLE mgpc_weights (
    weight_id SERIAL PRIMARY KEY,
    feature_name VARCHAR(20) NOT NULL,
    weight_value DECIMAL(3,2) NOT NULL CHECK (weight_value BETWEEN 0 AND 1),
    last_updated TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_feature UNIQUE (feature_name)
);

-- Initial weights insertion
INSERT INTO mgpc_weights (feature_name, weight_value) VALUES
    ('mode', 0.18),
    ('bpm', 0.20),
    ('key', 0.18),
    ('volume', 0.14),
    ('duration', 0.14),
    ('time_signature', 0.16);


