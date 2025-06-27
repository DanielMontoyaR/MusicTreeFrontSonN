CREATE OR REPLACE FUNCTION authenticate_fan(
    p_username VARCHAR(30),
    p_password VARCHAR(12)
) RETURNS TABLE (
    fan_id INT,
    full_name VARCHAR(100),
    country VARCHAR(100),
    avatar_path VARCHAR(255),
    status_message VARCHAR(50)  -- Nueva columna para el mensaje
) AS $$
BEGIN
    -- Verificar primero si el usuario existe
    IF NOT EXISTS (SELECT 1 FROM fans WHERE username = p_username) THEN
        RETURN QUERY SELECT NULL::INT, NULL::VARCHAR, NULL::VARCHAR, NULL::VARCHAR, 'Usuario no encontrado'::VARCHAR;
        RETURN;
    END IF;
    
    -- Verificar si la contraseña coincide
    IF NOT EXISTS (
        SELECT 1 
        FROM fans 
        WHERE username = p_username 
        AND password_hash = encode(sha256(p_password::bytea), 'hex')
    ) THEN
        RETURN QUERY SELECT NULL::INT, NULL::VARCHAR, NULL::VARCHAR, NULL::VARCHAR, 'Contraseña incorrecta'::VARCHAR;
        RETURN;
    END IF;
    
    -- Si todo es correcto, devolver los datos del fan
    RETURN QUERY
    SELECT 
        f.fan_id,
        f.full_name,
        f.country,
        f.avatar_path,
        'Autenticación exitosa'::VARCHAR
    FROM 
        fans f
    WHERE 
        f.username = p_username
        AND f.password_hash = encode(sha256(p_password::bytea), 'hex');
    
    -- Actualizar last_login si la autenticación es exitosa
    IF FOUND THEN
        UPDATE fans 
        SET last_login = CURRENT_TIMESTAMP 
        WHERE username = p_username;
    END IF;
END;
$$ LANGUAGE plpgsql;