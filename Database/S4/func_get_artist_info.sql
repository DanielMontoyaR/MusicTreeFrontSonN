CREATE OR REPLACE FUNCTION get_artist_profile(
    p_artist_id VARCHAR(15)
) RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'artist', (
            SELECT json_build_object(
                'artist_id', a.artist_id,
                'name', a.name,
                'biography', a.biography,
                'country_of_origin', a.country_of_origin,
                'created_at', a.created_at,
                'cover_image_path', a.cover_image_path,
                'average_rating', COALESCE(a.average_rating, 0),
                'rating_count', COALESCE(a.rating_count, 0),
                'activity_years', (
                    SELECT json_agg(json_build_object(
                        'start_year', y.start_year,
                        'end_year', y.end_year,
                        'is_present', y.is_present
                    ))
                    FROM artist_activity_years y
                    WHERE y.artist_id = a.artist_id
                ),
                'genres', (
                    SELECT json_agg(json_build_object(
                        'genre_id', g.genre_id,
                        'name', g.name
                    ))
                    FROM artist_genres ag
                    JOIN genres g ON ag.genre_id = g.genre_id
                    WHERE ag.artist_id = a.artist_id
                ),
                'subgenres', (
                    SELECT json_agg(json_build_object(
                        'subgenre_id', sg.genre_id,
                        'name', sg.name
                    ))
                    FROM artist_subgenres asg
                    JOIN genres sg ON asg.subgenre_id = sg.genre_id
                    WHERE asg.artist_id = a.artist_id
                ),
                'members', (
                    SELECT json_agg(json_build_object(
                        'full_name', m.full_name,
                        'instrument', m.instrument,
                        'start_period', m.start_period,
                        'end_period', m.end_period,
                        'is_current', m.is_current
                    ))
                    FROM band_members m
                    WHERE m.artist_id = a.artist_id
                ),
                'albums', (
                    SELECT json_agg(json_build_object(
                        'album_id', al.album_id,
                        'title', al.title,
                        'release_date', al.release_date,
                        'cover_image_path', al.cover_image_path,
                        'duration_seconds', al.duration_seconds
                    ))
                    FROM albums al
                    WHERE al.artist_id = a.artist_id
                ),
                'photos', (
                    SELECT COALESCE(
                        json_agg(json_build_object(
                            'photo_id', p.id,
                            'image_path', p.image_path,
                            'description', p.description,
                            'upload_date', p.upload_date
                        )),
                        '[{"message": "No hay fotos disponibles"}]'::json
                    )
                    FROM artist_photos p
                    WHERE p.artist_id = a.artist_id
                ),
                'comments', (
                    SELECT COALESCE(
                        json_agg(json_build_object(
                            'comment_id', c.id,
                            'content', c.content,
                            'author', c.author,
                            'created_at', c.created_at
                        )),
                        '[{"message": "No hay comentarios disponibles"}]'::json
                    )
                    FROM artist_comments c
                    WHERE c.artist_id = a.artist_id
                ),
                'events', (
                    SELECT COALESCE(
                        json_agg(json_build_object(
                            'event_id', e.id,
                            'description', e.description,
                            'event_date', e.event_date,
                            'location', e.location
                        )),
                        '[{"message": "No hay eventos disponibles"}]'::json
                    )
                    FROM artist_events e
                    WHERE e.artist_id = a.artist_id
                )
            )
            FROM artists a
            WHERE a.artist_id = p_artist_id
        )
    ) INTO result;
    
    RETURN result;
EXCEPTION WHEN OTHERS THEN
    RETURN json_build_object(
        'error', TRUE,
        'message', 'No se pudo cargar el perfil del artista. Intente más tarde.'
    );
END;
$$ LANGUAGE plpgsql;

CREATE INDEX idx_artist_ratings_artist ON artist_ratings(artist_id);
CREATE INDEX idx_artist_ratings_fan ON artist_ratings(fan_id);

