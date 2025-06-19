-- 1. First, recreate the ID generation functions with proper length control

-- Function to generate valid cluster IDs (15 chars: C- + 12 alnum)
CREATE OR REPLACE FUNCTION generate_valid_cluster_id() 
RETURNS VARCHAR(15) AS $$
BEGIN
    RETURN 'C-' || upper(substring(replace(md5(random()::text), '[^a-zA-Z0-9]', '') from 1 for 12));
END;
$$ LANGUAGE plpgsql;

-- Function to generate valid genre IDs (27 chars: G-12 + S-12 + null byte)
CREATE OR REPLACE FUNCTION generate_valid_genre_id(is_subgenre BOOLEAN DEFAULT FALSE) 
RETURNS VARCHAR(27) AS $$
DECLARE
    base_part VARCHAR(15);
    sub_part VARCHAR(12) := '000000000000';
BEGIN
    base_part := 'G-' || upper(substring(replace(md5(random()::text), '[^a-zA-Z0-9]', '') from 1 for 12));
    
    IF is_subgenre THEN
        sub_part := 'S-' || upper(substring(replace(md5(random()::text), '[^a-zA-Z0-9]', '') from 1 for 10));
    END IF;
    
    RETURN base_part || sub_part;
END;
$$ LANGUAGE plpgsql;

-- 2. Update table defaults
ALTER TABLE genre_clusters 
ALTER COLUMN cluster_id SET DEFAULT generate_valid_cluster_id();

ALTER TABLE genres
ALTER COLUMN genre_id SET DEFAULT generate_valid_genre_id(FALSE);
