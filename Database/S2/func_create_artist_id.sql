-- Function to generate artist ID
CREATE OR REPLACE FUNCTION generate_artist_id()
RETURNS VARCHAR(15) AS $$
DECLARE
    random_part TEXT;
BEGIN
    random_part := substring(md5(random()::text) from 1 for 12);
    RETURN 'A-' || random_part;
END;
$$ LANGUAGE plpgsql;

-- Function to generate album ID
CREATE OR REPLACE FUNCTION generate_album_id(artist_id VARCHAR)
RETURNS VARCHAR(30) AS $$
DECLARE
    random_part TEXT;
BEGIN
    random_part := substring(md5(random()::text) from 1 for 12);
    RETURN artist_id || '-D-' || random_part;
END;
$$ LANGUAGE plpgsql;

