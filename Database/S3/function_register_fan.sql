CREATE OR REPLACE FUNCTION register_fan(
    p_username VARCHAR(30),
    p_password VARCHAR(12),
    p_full_name VARCHAR(100),
    p_country VARCHAR(100),
    p_avatar_id INT,
    p_genre_ids VARCHAR(38)[]
) RETURNS INT AS $$
DECLARE
    v_fan_id INT;
    v_genre_id VARCHAR(38);
	v_genre_name VARCHAR(100);
    v_password_hash TEXT;
    v_avatar_path VARCHAR(255);
	
BEGIN
    -- Validar contraseña
    IF LENGTH(p_password) < 8 OR LENGTH(p_password) > 12 THEN
        RAISE EXCEPTION 'La contraseña debe tener entre 8 y 12 caracteres';
    END IF;
    
    IF p_password !~ '[A-Z]' OR p_password !~ '[a-z]' OR p_password !~ '[0-9]' THEN
        RAISE EXCEPTION 'La contraseña debe incluir mayúsculas, minúsculas y números';
    END IF;
    
    -- Obtener path del avatar
    SELECT image_path INTO v_avatar_path 
    FROM avatars 
    WHERE avatar_id = p_avatar_id;
    
    IF v_avatar_path IS NULL THEN
        RAISE EXCEPTION 'Avatar no válido';
    END IF;
    
    -- Hash de contraseña con SHA-256 (alternativa para Azure)
    v_password_hash := encode(sha256(p_password::bytea), 'hex');
    
    -- Insertar fan
    INSERT INTO fans (username, password_hash, full_name, country, avatar_path)
    VALUES (
        p_username,
        v_password_hash,
        p_full_name,
        p_country,
        v_avatar_path
    )
    RETURNING fan_id INTO v_fan_id;
    
    -- Añadir géneros favoritos
    FOREACH v_genre_id IN ARRAY p_genre_ids LOOP
        BEGIN
            -- Obtener el nombre del género
            SELECT name INTO v_genre_name FROM genres WHERE genre_id = v_genre_id;
            
            -- Insertar ambos valores
            INSERT INTO fan_favorite_genres (fan_id, genre_name) 
            VALUES (v_fan_id, v_genre_name);
        EXCEPTION WHEN OTHERS THEN
            RAISE NOTICE 'No se pudo agregar el género %: %', v_genre_id, SQLERRM;
        END;
    END LOOP;
    
    RETURN v_fan_id;
EXCEPTION
    WHEN unique_violation THEN
        RAISE EXCEPTION 'El nombre de usuario ya existe';
    WHEN foreign_key_violation THEN
        RAISE EXCEPTION 'Avatar o género no válido';
END;
$$ LANGUAGE plpgsql;