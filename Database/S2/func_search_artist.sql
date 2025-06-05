CREATE OR REPLACE FUNCTION search_artist_json(
    p_search_term VARCHAR(100),
    p_limit INT DEFAULT 10
)
RETURNS JSONB AS $$
DECLARE
    result JSONB;
BEGIN
    WITH artist_data AS (
        SELECT 
            a.artist_id,
            a.name,
            a.biography,
            a.country_of_origin,
            a.cover_image_path
        FROM 
            artists a
        WHERE 
            a.name ILIKE '%' || p_search_term || '%'
            OR a.biography ILIKE '%' || p_search_term || '%'
        ORDER BY 
            CASE 
                WHEN a.name ILIKE p_search_term || '%' THEN 0
                WHEN a.name ILIKE '%' || p_search_term || '%' THEN 1
                ELSE 2
            END,
            a.name ASC
        LIMIT p_limit
    ),
    artist_genres_data AS (
        SELECT 
            ag.artist_id,
            json_agg(json_build_object('name', g.name)) AS genres
        FROM 
            artist_genres ag
            JOIN genres g ON ag.genre_id = g.genre_id
            JOIN artist_data ad ON ag.artist_id = ad.artist_id
        GROUP BY ag.artist_id
    ),
    artist_subgenres_data AS (
        SELECT 
            asg.artist_id,
            json_agg(json_build_object('name', sg.name)) AS subgenres
        FROM 
            artist_subgenres asg
            JOIN genres sg ON asg.subgenre_id = sg.genre_id
            JOIN artist_data ad ON asg.artist_id = ad.artist_id
        GROUP BY asg.artist_id
    ),
    artist_members_data AS (
        SELECT 
            bm.artist_id,
            json_agg(json_build_object(
                'full_name', bm.full_name,
                'instrument', bm.instrument,
                'is_current', bm.is_current
            )) AS members
        FROM 
            band_members bm
            JOIN artist_data ad ON bm.artist_id = ad.artist_id
        GROUP BY bm.artist_id
    ),
    artist_albums_data AS (
        SELECT 
            al.artist_id,
            json_agg(json_build_object(
                'title', al.title,
                'release_date', al.release_date,
                'cover_image_path', al.cover_image_path
            )) AS albums
        FROM 
            albums al
            JOIN artist_data ad ON al.artist_id = ad.artist_id
        GROUP BY al.artist_id
    ),
    artist_photos_data AS (
        SELECT 
            ap.artist_id,
            json_agg(json_build_object('image_path', ap.image_path)) AS photos
        FROM 
            artist_photos ap
            JOIN artist_data ad ON ap.artist_id = ad.artist_id
        GROUP BY ap.artist_id
    ),
    artist_comments_data AS (
        SELECT 
            ac.artist_id,
            json_agg(json_build_object('content', ac.content)) AS comments
        FROM 
            artist_comments ac
            JOIN artist_data ad ON ac.artist_id = ad.artist_id
        GROUP BY ac.artist_id
    ),
    artist_events_data AS (
        SELECT 
            ae.artist_id,
            json_agg(json_build_object(
                'description', ae.description,
                'event_date', ae.event_date,
                'location', ae.location
            )) AS events
        FROM 
            artist_events ae
            JOIN artist_data ad ON ae.artist_id = ad.artist_id
        GROUP BY ae.artist_id
    )
    SELECT json_agg(
        json_build_object(
            'name', ad.name,
            'biography', ad.biography,
            'country_of_origin', ad.country_of_origin,
            'cover_image_path', ad.cover_image_path,
            'genres', COALESCE(agd.genres, '[]'::jsonb),
            'subgenres', COALESCE(asd.subgenres, '[]'::jsonb),
            'members', COALESCE(amd.members, '[]'::jsonb),
            'albums', COALESCE(aad.albums, '[]'::jsonb),
            'photos', COALESCE(apd.photos, '[]'::jsonb),
            'comments', COALESCE(acd.comments, '[]'::jsonb),
            'events', COALESCE(aed.events, '[]'::jsonb)
        )
    ) INTO result
    FROM 
        artist_data ad
        LEFT JOIN artist_genres_data agd ON ad.artist_id = agd.artist_id
        LEFT JOIN artist_subgenres_data asd ON ad.artist_id = asd.artist_id
        LEFT JOIN artist_members_data amd ON ad.artist_id = amd.artist_id
        LEFT JOIN artist_albums_data aad ON ad.artist_id = aad.artist_id
        LEFT JOIN artist_photos_data apd ON ad.artist_id = apd.artist_id
        LEFT JOIN artist_comments_data acd ON ad.artist_id = acd.artist_id
        LEFT JOIN artist_events_data aed ON ad.artist_id = aed.artist_id;
    
    RETURN COALESCE(result, '[]'::JSONB);
END;
$$ LANGUAGE plpgsql;