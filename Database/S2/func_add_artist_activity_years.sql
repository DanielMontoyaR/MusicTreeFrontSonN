-- Function to add activity years for an artist
CREATE OR REPLACE FUNCTION add_artist_activity_years(
    p_artist_id VARCHAR(15),
    p_start_year INTEGER,
    p_end_year INTEGER DEFAULT NULL,
    p_is_present BOOLEAN DEFAULT FALSE
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO artist_activity_years (artist_id, start_year, end_year, is_present)
    VALUES (p_artist_id, p_start_year, p_end_year, p_is_present);
END;
$$ LANGUAGE plpgsql;