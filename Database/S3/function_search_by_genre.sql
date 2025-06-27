CREATE OR REPLACE FUNCTION search_artists_by_genre(
    p_genre_id VARCHAR(38),
    p_subgenre_id VARCHAR(38) DEFAULT NULL,
    p_name_filter VARCHAR(100) DEFAULT NULL,
    p_limit INT DEFAULT 100,
    p_offset INT DEFAULT 0
) RETURNS TABLE (
    artist_id VARCHAR(15),
    name VARCHAR(100),
    album_count BIGINT,
    genres TEXT,
    subgenres TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.artist_id,
        a.name,
        COUNT(DISTINCT al.album_id)::BIGINT AS album_count,
        string_agg(DISTINCT g.name, ', ') AS genres,
        string_agg(DISTINCT sg.name, ', ') AS subgenres
    FROM 
        artists a
    LEFT JOIN 
        artist_genres ag ON a.artist_id = ag.artist_id
    LEFT JOIN 
        genres g ON ag.genre_id = g.genre_id
    LEFT JOIN 
        artist_subgenres asg ON a.artist_id = asg.artist_id
    LEFT JOIN 
        genres sg ON asg.subgenre_id = sg.genre_id
    LEFT JOIN 
        albums al ON a.artist_id = al.artist_id
    WHERE 
        (ag.genre_id = p_genre_id OR (p_subgenre_id IS NOT NULL AND asg.subgenre_id = p_subgenre_id))
        AND (p_name_filter IS NULL OR a.name ILIKE '%' || p_name_filter || '%')
    GROUP BY 
        a.artist_id
    ORDER BY 
        a.name ASC
    LIMIT 
        p_limit
    OFFSET 
        p_offset;
END;
$$ LANGUAGE plpgsql;


