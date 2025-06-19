-- Function to add a band member
CREATE OR REPLACE FUNCTION add_band_member(
    p_artist_id VARCHAR(15),
    p_full_name VARCHAR(100),
    p_instrument VARCHAR(100),
    p_start_period VARCHAR(50),
    p_end_period VARCHAR(50),
    p_is_current BOOLEAN
)
RETURNS INTEGER AS $$
DECLARE
    member_id INTEGER;
BEGIN
    INSERT INTO band_members (artist_id, full_name, instrument, start_period, end_period, is_current)
    VALUES (p_artist_id, p_full_name, p_instrument, p_start_period, p_end_period, p_is_current)
    RETURNING id INTO member_id;
    
    RETURN member_id;
END;
$$ LANGUAGE plpgsql;