CREATE OR REPLACE FUNCTION rate_artist(
    p_fan_id INT,
    p_artist_id VARCHAR,  -- Cambiado de VARCHAR(15) a VARCHAR
    p_rating INT
) RETURNS JSON AS $$
DECLARE
    existing_rating INT;
    result JSON;
BEGIN
    -- Verificar si ya existe una calificación
    SELECT rating INTO existing_rating
    FROM artist_ratings
    WHERE fan_id = p_fan_id AND artist_id = p_artist_id;
    
    IF existing_rating IS NOT NULL THEN
        RETURN json_build_object(
            'status', 'error',
            'message', 'Ya has calificado a este artista',
            'your_rating', existing_rating
        );
    END IF;
    
    -- Insertar nueva calificación
    INSERT INTO artist_ratings (fan_id, artist_id, rating)
    VALUES (p_fan_id, p_artist_id, p_rating);
    
    -- Actualizar métricas del artista
    UPDATE artists
    SET 
        average_rating = (
            SELECT AVG(rating)::DECIMAL(3,2)
            FROM artist_ratings
            WHERE artist_id = p_artist_id
        ),
        rating_count = (
            SELECT COUNT(*)
            FROM artist_ratings
            WHERE artist_id = p_artist_id
        )
    WHERE artist_id = p_artist_id;
    
    RETURN json_build_object(
        'status', 'success',
        'message', 'Calificación registrada',
        'new_average', (
            SELECT average_rating
            FROM artists
            WHERE artist_id = p_artist_id
        ),
        'total_ratings', (
            SELECT rating_count
            FROM artists
            WHERE artist_id = p_artist_id
        )
    );
EXCEPTION WHEN OTHERS THEN
    RETURN json_build_object(
        'status', 'error',
        'message', 'No se pudo registrar la calificación. Intente más tarde.'
    );
END;
$$ LANGUAGE plpgsql;

