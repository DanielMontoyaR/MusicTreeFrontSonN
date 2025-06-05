-- Function to calculate MGPC score between two genres
CREATE OR REPLACE FUNCTION calculate_mgpc(
    genre1_id VARCHAR(27),
    genre2_id VARCHAR(27)
) RETURNS DECIMAL(5,4) AS $$
DECLARE
    mode1 DECIMAL(3,2);
    mode2 DECIMAL(3,2);
    bpm1_low INTEGER;
    bpm1_high INTEGER;
    bpm2_low INTEGER;
    bpm2_high INTEGER;
    bpm1_avg DECIMAL;
    bpm2_avg DECIMAL;
    key1 INTEGER;
    key2 INTEGER;
    vol1 DECIMAL(5,2);
    vol2 DECIMAL(5,2);
    dur1 INTEGER;
    dur2 INTEGER;
    ts1 INTEGER;
    ts2 INTEGER;
    
    d_mode DECIMAL(10,8);
    d_bpm DECIMAL(10,8);
    d_key DECIMAL(10,8);
    d_vol DECIMAL(10,8);
    d_dur DECIMAL(10,8);
    d_ts DECIMAL(10,8);
    
    w_mode DECIMAL(3,2);
    w_bpm DECIMAL(3,2);
    w_key DECIMAL(3,2);
    w_vol DECIMAL(3,2);
    w_dur DECIMAL(3,2);
    w_ts DECIMAL(3,2);
    
    mgpc_score DECIMAL(5,4);
BEGIN
    -- Get weights
    SELECT weight_value INTO w_mode FROM mgpc_weights WHERE feature_name = 'mode';
    SELECT weight_value INTO w_bpm FROM mgpc_weights WHERE feature_name = 'bpm';
    SELECT weight_value INTO w_key FROM mgpc_weights WHERE feature_name = 'key';
    SELECT weight_value INTO w_vol FROM mgpc_weights WHERE feature_name = 'volume';
    SELECT weight_value INTO w_dur FROM mgpc_weights WHERE feature_name = 'duration';
    SELECT weight_value INTO w_ts FROM mgpc_weights WHERE feature_name = 'time_signature';
    
    -- Get genre1 attributes
    SELECT 
        average_mode, bpm_lower, bpm_upper, 
        dominant_key::integer, typical_volume, average_duration, 
        time_signature::integer
    INTO 
        mode1, bpm1_low, bpm1_high, key1, vol1, dur1, ts1
    FROM genres WHERE genre_id = genre1_id;
    
    -- Get genre2 attributes
    SELECT 
        average_mode, bpm_lower, bpm_upper, 
        dominant_key::integer, typical_volume, average_duration, 
        time_signature::integer
    INTO 
        mode2, bpm2_low, bpm2_high, key2, vol2, dur2, ts2
    FROM genres WHERE genre_id = genre2_id;
    
    -- Calculate distances
    -- Mode distance
    d_mode := ABS(mode1 - mode2);
    
    -- BPM distance (using average of the range)
    bpm1_avg := (bpm1_low + bpm1_high) / 2.0;
    bpm2_avg := (bpm2_low + bpm2_high) / 2.0;
    d_bpm := ABS(bpm1_avg - bpm2_avg) / 250;
    
    -- Key distance
    IF key1 = -1 OR key2 = -1 THEN
        d_key := 0;
    ELSE
        d_key := LEAST(ABS(key1 - key2), 12 - ABS(key1 - key2)) / 6.0;
    END IF;
    
    -- Volume distance
    d_vol := ABS(vol1 - vol2) / 60;
    
    -- Duration distance
    d_dur := ABS(dur1 - dur2) / 3600.0;
    
    -- Time signature distance
    IF ts1 = 0 OR ts2 = 0 THEN
        d_ts := 0;
    ELSE
        d_ts := ABS(ts1 - ts2) / 6.0;
    END IF;
    
    -- Calculate MGPC score
    mgpc_score := 1 - SQRT(
        w_mode * POWER(d_mode, 2) + 
        w_bpm * POWER(d_bpm, 2) + 
        w_key * POWER(d_key, 2) + 
        w_vol * POWER(d_vol, 2) + 
        w_dur * POWER(d_dur, 2) + 
        w_ts * POWER(d_ts, 2)
    );
    
    -- Ensure score is between 0 and 1
    IF mgpc_score < 0 THEN
        mgpc_score := 0;
    ELSIF mgpc_score > 1 THEN
        mgpc_score := 1;
    END IF;
    
    RETURN mgpc_score;
END;
$$ LANGUAGE plpgsql;

-- Function to create a new genre cluster
CREATE OR REPLACE FUNCTION create_genre_cluster(
    cluster_name VARCHAR(30),
    cluster_description VARCHAR(300) DEFAULT NULL,
    is_active_flag BOOLEAN DEFAULT TRUE
) RETURNS VARCHAR(15) AS $$
DECLARE
    new_cluster_id VARCHAR(15);
BEGIN
    -- Validate input
    IF cluster_name IS NULL OR LENGTH(cluster_name) < 3 OR LENGTH(cluster_name) > 30 THEN
        RAISE EXCEPTION 'Cluster name must be between 3 and 30 characters';
    END IF;
    
    IF cluster_description IS NOT NULL AND LENGTH(cluster_description) > 300 THEN
        RAISE EXCEPTION 'Cluster description must be 300 characters or less';
    END IF;
    
    -- Check for duplicate name
    PERFORM 1 FROM genre_clusters WHERE name = cluster_name;
    IF FOUND THEN
        RAISE EXCEPTION 'A cluster with this name already exists';
    END IF;
    
    -- Insert new cluster
    INSERT INTO genre_clusters (name, description, is_active)
    VALUES (cluster_name, cluster_description, is_active_flag)
    RETURNING cluster_id INTO new_cluster_id;
    
    RETURN new_cluster_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error creating genre cluster: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Function to create a new genre
CREATE OR REPLACE FUNCTION create_genre(
    genre_name VARCHAR(30),
    genre_description VARCHAR(1000) DEFAULT NULL,
    genre_color VARCHAR(7) DEFAULT NULL,
    creation_year INTEGER DEFAULT NULL,
    country_of_origin VARCHAR(100) DEFAULT NULL,
    average_mode DECIMAL(3,2) DEFAULT NULL,
    bpm_lower INTEGER DEFAULT NULL,
    bpm_upper INTEGER DEFAULT NULL,
    dominant_key key_type DEFAULT NULL,
    typical_volume DECIMAL(5,2) DEFAULT NULL,
    time_signature time_signature_type DEFAULT NULL,
    average_duration INTEGER DEFAULT NULL,
    is_subgenre_flag BOOLEAN DEFAULT FALSE,
    parent_genre_id VARCHAR(27) DEFAULT NULL,
    cluster_id VARCHAR(15) DEFAULT NULL
) RETURNS VARCHAR(27) AS $$
DECLARE
    new_genre_id VARCHAR(27);
BEGIN
    -- Validate input
    IF genre_name IS NULL OR LENGTH(genre_name) < 3 OR LENGTH(genre_name) > 30 THEN
        RAISE EXCEPTION 'Genre name must be between 3 and 30 characters';
    END IF;
    
    IF genre_description IS NOT NULL AND LENGTH(genre_description) > 1000 THEN
        RAISE EXCEPTION 'Genre description must be 1000 characters or less';
    END IF;
    
    IF is_subgenre_flag = TRUE AND parent_genre_id IS NULL THEN
        RAISE EXCEPTION 'Parent genre is required for subgenres';
    END IF;
    
    IF is_subgenre_flag = TRUE AND genre_color IS NOT NULL THEN
        RAISE EXCEPTION 'Subgenres cannot have a color';
    END IF;
    
    -- Check for duplicate name with same parent
    PERFORM 1 FROM genres 
    WHERE name = genre_name 
    AND ((parent_genre_id IS NULL AND parent_genre_id IS NULL) OR parent_genre_id = parent_genre_id);
    
    IF FOUND THEN
        RAISE EXCEPTION 'A genre with this name (and parent) already exists';
    END IF;
    
    -- Validate parent genre if this is a subgenre
    IF is_subgenre_flag = TRUE THEN
        PERFORM 1 FROM genres WHERE genre_id = parent_genre_id AND is_subgenre = FALSE;
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Parent genre must be a main genre (not a subgenre)';
        END IF;
    END IF;
    
    -- Validate cluster exists if provided
    IF cluster_id IS NOT NULL THEN
        PERFORM 1 FROM genre_clusters WHERE cluster_id = cluster_id;
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Specified cluster does not exist';
        END IF;
    END IF;
    
    -- Insert new genre
    INSERT INTO genres (
        name, description, color, creation_year, country_of_origin,
        average_mode, bpm_lower, bpm_upper, dominant_key, typical_volume,
        time_signature, average_duration, is_subgenre, parent_genre_id, cluster_id
    )
    VALUES (
        genre_name, genre_description, genre_color, creation_year, country_of_origin,
        average_mode, bpm_lower, bpm_upper, dominant_key, typical_volume,
        time_signature, average_duration, is_subgenre_flag, parent_genre_id, cluster_id
    )
    RETURNING genre_id INTO new_genre_id;
    
    -- If this is a subgenre, calculate MGPC with parent
    IF is_subgenre_flag = TRUE THEN
        PERFORM add_genre_relationship(parent_genre_id, new_genre_id, 5);
    END IF;
    
    RETURN new_genre_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error creating genre: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Function to add a genre relationship
CREATE OR REPLACE FUNCTION add_genre_relationship(
    source_genre_id VARCHAR(27),
    target_genre_id VARCHAR(27),
    influence_level INTEGER DEFAULT 5
) RETURNS INTEGER AS $$
DECLARE
    relationship_exists BOOLEAN;
    new_mgpc DECIMAL(5,4);
    new_relationship_id INTEGER;
BEGIN
    -- Validate influence level
    IF influence_level < 1 OR influence_level > 10 THEN
        RAISE EXCEPTION 'Influence level must be between 1 and 10';
    END IF;
    
    -- Check if relationship already exists
    PERFORM 1 FROM genre_relationships 
    WHERE (source_genre_id = source_genre_id AND target_genre_id = target_genre_id)
    OR (source_genre_id = target_genre_id AND target_genre_id = source_genre_id);
    
    IF FOUND THEN
        RAISE EXCEPTION 'A relationship between these genres already exists';
    END IF;
    
    -- Calculate MGPC score
    new_mgpc := calculate_mgpc(source_genre_id, target_genre_id);
    
    -- Insert new relationship
    INSERT INTO genre_relationships (
        source_genre_id, target_genre_id, influence_level, mgpc_score
    )
    VALUES (
        source_genre_id, target_genre_id, influence_level, new_mgpc
    )
    RETURNING relationship_id INTO new_relationship_id;
    
    RETURN new_relationship_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error adding genre relationship: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Function to get all active genre clusters
CREATE OR REPLACE FUNCTION get_genre_clusters(
    include_inactive BOOLEAN DEFAULT FALSE
) RETURNS TABLE (
    cluster_id VARCHAR(15),
    name VARCHAR(30),
    is_active BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    IF include_inactive THEN
        RETURN QUERY
        SELECT gc.cluster_id, gc.name, gc.is_active, gc.created_at
        FROM genre_clusters gc
        ORDER BY gc.name DESC;
    ELSE
        RETURN QUERY
        SELECT gc.cluster_id, gc.name, gc.is_active, gc.created_at
        FROM genre_clusters gc
        WHERE gc.is_active = TRUE
        ORDER BY gc.name DESC;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to update MGPC weights
CREATE OR REPLACE FUNCTION update_mgpc_weights(
    mode_weight DECIMAL(3,2),
    bpm_weight DECIMAL(3,2),
    key_weight DECIMAL(3,2),
    volume_weight DECIMAL(3,2),
    duration_weight DECIMAL(3,2),
    time_signature_weight DECIMAL(3,2)
) RETURNS VOID AS $$
DECLARE
    total_weight DECIMAL(5,2);
BEGIN
    -- Validate weights sum to 1
    total_weight := mode_weight + bpm_weight + key_weight + volume_weight + duration_weight + time_signature_weight;
    
    IF total_weight != 1.0 THEN
        RAISE EXCEPTION 'Weights must sum to 1.0 (current sum: %)', total_weight;
    END IF;
    
    -- Update weights
    UPDATE mgpc_weights SET weight_value = mode_weight WHERE feature_name = 'mode';
    UPDATE mgpc_weights SET weight_value = bpm_weight WHERE feature_name = 'bpm';
    UPDATE mgpc_weights SET weight_value = key_weight WHERE feature_name = 'key';
    UPDATE mgpc_weights SET weight_value = volume_weight WHERE feature_name = 'volume';
    UPDATE mgpc_weights SET weight_value = duration_weight WHERE feature_name = 'duration';
    UPDATE mgpc_weights SET weight_value = time_signature_weight WHERE feature_name = 'time_signature';
END;
$$ LANGUAGE plpgsql;


