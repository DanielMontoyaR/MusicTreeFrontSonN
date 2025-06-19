-- Function to add an album to an artist
CREATE OR REPLACE FUNCTION add_album(
    p_artist_id VARCHAR(15),
    p_title VARCHAR(100),
    p_release_date DATE,
    p_cover_image_path TEXT,
    p_duration_seconds INTEGER
)
RETURNS VARCHAR(30)
AS $$
DECLARE
    album_id VARCHAR(30);
BEGIN
    -- Generate album ID
    album_id := generate_album_id(p_artist_id);
    
    -- Insert album record
    INSERT INTO albums (album_id, artist_id, title, release_date, cover_image_path, duration_seconds)
    VALUES (album_id, p_artist_id, p_title, p_release_date, p_cover_image_path, p_duration_seconds);
    
    RETURN album_id;
END;
$$ LANGUAGE plpgsql;