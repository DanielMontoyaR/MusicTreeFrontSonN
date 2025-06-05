CREATE OR REPLACE FUNCTION register_artist(
    p_name VARCHAR(100),
    p_biography TEXT,
    p_country VARCHAR(100),
    p_cover_image_path TEXT,
    p_date_start INTEGER,
    p_date_end INTEGER,
    p_is_present BOOLEAN DEFAULT FALSE,
    p_genre_ids VARCHAR(38)[] DEFAULT '{}',
    p_subgenre_ids VARCHAR(38)[] DEFAULT '{}'
)
RETURNS VARCHAR(15)
AS $$
DECLARE
    artist_id VARCHAR(15);
    genre_id VARCHAR(38);
    subgenre_id VARCHAR(38);
BEGIN
    -- Validate parameters
    IF p_name IS NULL OR LENGTH(TRIM(p_name)) < 3 THEN
        RAISE EXCEPTION 'Artist name must be at least 3 characters';
    END IF;
    
    IF p_date_start IS NULL THEN
        RAISE EXCEPTION 'Start year is required';
    END IF;
    
    -- Generate artist ID
    artist_id := generate_artist_id();
    
    -- Insert artist record
    INSERT INTO artists (artist_id, name, biography, country_of_origin, cover_image_path)
    VALUES (artist_id, p_name, p_biography, p_country, p_cover_image_path);
    
    -- Add activity years
    INSERT INTO artist_activity_years (
        artist_id, 
        start_year, 
        end_year, 
        is_present
    ) VALUES (
        artist_id,
        p_date_start,
        CASE WHEN p_is_present THEN NULL ELSE p_date_end END,
        p_is_present
    );
    
    -- Add cover photo to artist photos
    IF p_cover_image_path IS NOT NULL THEN
        INSERT INTO artist_photos (
            artist_id, 
            image_path, 
            description
        ) VALUES (
            artist_id,
            p_cover_image_path,
            'Official artist photo'
        );
    END IF;
    
    -- Add genres
    FOREACH genre_id IN ARRAY p_genre_ids LOOP
        BEGIN
            INSERT INTO artist_genres (artist_id, genre_id) 
            VALUES (artist_id, genre_id);
        EXCEPTION WHEN OTHERS THEN
            RAISE NOTICE 'Failed to add genre %: %', genre_id, SQLERRM;
        END;
    END LOOP;
    
    -- Add subgenres
    FOREACH subgenre_id IN ARRAY p_subgenre_ids LOOP
        BEGIN
            INSERT INTO artist_subgenres (artist_id, subgenre_id) 
            VALUES (artist_id, subgenre_id);
        EXCEPTION WHEN OTHERS THEN
            RAISE NOTICE 'Failed to add subgenre %: %', subgenre_id, SQLERRM;
        END;
    END LOOP;
    
    RETURN artist_id;
END;
$$ LANGUAGE plpgsql;