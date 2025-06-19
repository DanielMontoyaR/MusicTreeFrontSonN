-- Function to get artist catalog
CREATE OR REPLACE FUNCTION get_artist_catalog(
    p_limit INTEGER DEFAULT NULL,
    p_offset INTEGER DEFAULT 0
)
RETURNS TABLE (
    artist_id VARCHAR(15),
    name VARCHAR(100),
    country_of_origin VARCHAR(100),
    album_count BIGINT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.artist_id,
        a.name,
        a.country_of_origin,
        COUNT(al.album_id)::BIGINT AS album_count,
        a.created_at
    FROM 
        artists a
    LEFT JOIN 
        albums al ON a.artist_id = al.artist_id
    GROUP BY 
        a.artist_id
    ORDER BY 
        a.created_at DESC
    LIMIT 
        p_limit
    OFFSET 
        p_offset;
END;
$$ LANGUAGE plpgsql;