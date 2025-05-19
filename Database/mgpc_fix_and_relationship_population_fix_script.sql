-- 1. First, let's fix the calculate_mgpc function with correct syntax
CREATE OR REPLACE FUNCTION calculate_mgpc(genre1_id VARCHAR(27), genre2_id VARCHAR(27))
RETURNS DECIMAL(5,4) AS $$
DECLARE
    mode1 DECIMAL(3,2);
    mode2 DECIMAL(3,2);
    bpm1_low INTEGER;
    bpm1_high INTEGER;
    bpm2_low INTEGER;
    bpm2_high INTEGER;
    bpm1_avg DECIMAL;
    bpm2_avg DECIMAL;
    key1 TEXT;
    key2 TEXT;
    vol1 DECIMAL(5,2);
    vol2 DECIMAL(5,2);
    dur1 INTEGER;
    dur2 INTEGER;
    ts1 TEXT;
    ts2 TEXT;
    
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
    
    -- Get genre1 attributes (casting enum types to text)
    SELECT 
        average_mode, bpm_lower, bpm_upper, 
        dominant_key::text, typical_volume, average_duration, 
        time_signature::text
    INTO 
        mode1, bpm1_low, bpm1_high, key1, vol1, dur1, ts1
    FROM genres WHERE genre_id = genre1_id;
    
    -- Get genre2 attributes (casting enum types to text)
    SELECT 
        average_mode, bpm_lower, bpm_upper, 
        dominant_key::text, typical_volume, average_duration, 
        time_signature::text
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
    
    -- Key distance (handle text conversion)
    IF key1 = '-1' OR key2 = '-1' THEN
        d_key := 0;
    ELSE
        d_key := LEAST(ABS(key1::integer - key2::integer), 12 - ABS(key1::integer - key2::integer)) / 6.0;
    END IF;
    
    -- Volume distance
    d_vol := ABS(vol1 - vol2) / 60;
    
    -- Duration distance
    d_dur := ABS(dur1 - dur2) / 3600.0;
    
    -- Time signature distance (handle text conversion)
    IF ts1 = '0' OR ts2 = '0' THEN
        d_ts := 0;
    ELSE
        d_ts := ABS(ts1::integer - ts2::integer) / 6.0;
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

-- 2. Fix the add_genre_relationship function
CREATE OR REPLACE FUNCTION add_genre_relationship(
    p_source_genre_id VARCHAR(27),
    p_target_genre_id VARCHAR(27),
    p_influence_level INTEGER DEFAULT 5
) RETURNS INTEGER AS $$
DECLARE
    new_mgpc DECIMAL(5,4);
    new_relationship_id INTEGER;
BEGIN
    -- Validate influence level
    IF p_influence_level < 1 OR p_influence_level > 10 THEN
        RAISE EXCEPTION 'Influence level must be between 1 and 10';
    END IF;
    
    -- Check if relationship already exists
    PERFORM 1 FROM genre_relationships 
    WHERE (source_genre_id = p_source_genre_id AND target_genre_id = p_target_genre_id)
       OR (source_genre_id = p_target_genre_id AND target_genre_id = p_source_genre_id);
    
    IF FOUND THEN
        RAISE EXCEPTION 'A relationship between these genres already exists';
    END IF;
    
    -- Calculate MGPC score
    new_mgpc := calculate_mgpc(p_source_genre_id, p_target_genre_id);
    
    -- Insert new relationship
    INSERT INTO genre_relationships (
        source_genre_id, target_genre_id, influence_level, mgpc_score
    )
    VALUES (
        p_source_genre_id, p_target_genre_id, p_influence_level, new_mgpc
    )
    RETURNING relationship_id INTO new_relationship_id;
    
    RETURN new_relationship_id;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Error adding genre relationship: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- 3. Now run the relationship population
DO $$
DECLARE
    rock_id VARCHAR(27);
    jazz_id VARCHAR(27);
    classical_id VARCHAR(27);
    metal_id VARCHAR(27);
    bebop_id VARCHAR(27);
BEGIN
    -- Get genre IDs
    SELECT genre_id INTO rock_id FROM genres WHERE name = 'Rock';
    SELECT genre_id INTO jazz_id FROM genres WHERE name = 'Jazz';
    SELECT genre_id INTO classical_id FROM genres WHERE name = 'Classical';
    SELECT genre_id INTO metal_id FROM genres WHERE name = 'Heavy Metal';
    SELECT genre_id INTO bebop_id FROM genres WHERE name = 'Bebop';
    
    -- Create relationships
    PERFORM add_genre_relationship(jazz_id, rock_id, 7);
    PERFORM add_genre_relationship(classical_id, rock_id, 5);
    PERFORM add_genre_relationship(rock_id, metal_id, 9);
    PERFORM add_genre_relationship(jazz_id, bebop_id, 8);
END $$;