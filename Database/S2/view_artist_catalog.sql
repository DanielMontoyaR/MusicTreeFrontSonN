CREATE OR REPLACE VIEW artist_catalog_view AS
SELECT 
    a.artist_id AS "ID Artista",
    a.name AS "Nombre",
    a.country_of_origin AS "País de Origen",
    COUNT(al.album_id) AS "Álbumes Asociados",
    a.created_at AS "Fecha y Hora de Registro",
    -- Información adicional útil para el curador
    a.status AS "Estado",
    (
        SELECT string_agg(
            CASE 
                WHEN y.is_present THEN y.start_year::text || '-Presente'
                WHEN y.end_year IS NULL THEN y.start_year::text
                ELSE y.start_year::text || '-' || y.end_year::text
            END, 
            ', ' ORDER BY y.start_year
        )
        FROM artist_activity_years y
        WHERE y.artist_id = a.artist_id
    ) AS "Años de Actividad"
FROM 
    artists a
LEFT JOIN 
    albums al ON a.artist_id = al.artist_id
GROUP BY 
    a.artist_id
ORDER BY 
    a.created_at DESC;