
-- 3. Populate genre_clusters
INSERT INTO genre_clusters (name, description, is_active) VALUES
('Popular Music', 'Genres that are widely popular in mainstream culture', TRUE),
('Traditional', 'Roots and traditional music genres from around the world', TRUE),
('Electronic', 'Genres primarily created with electronic instruments and technology', TRUE),
('Regional', 'Genres strongly associated with specific regions or cultures', FALSE);

-- 4. Populate main genres (using DEFAULT for IDs)
INSERT INTO genres (
    name, description, color, creation_year, country_of_origin,
    average_mode, bpm_lower, bpm_upper, dominant_key, typical_volume,
    time_signature, average_duration, is_subgenre, cluster_id
) VALUES
('Rock', 'Genre of popular music that originated as "rock and roll"', '#FF0000', 1950, 'United States', 
 0.65, 100, 140, '0', -12.5, '4', 240, FALSE, (SELECT cluster_id FROM genre_clusters WHERE name = 'Popular Music')),

('Jazz', 'Music genre that originated in African-American communities', '#0000FF', 1900, 'United States', 
 0.55, 60, 200, '0', -15.0, '4', 300, FALSE, (SELECT cluster_id FROM genre_clusters WHERE name = 'Traditional')),

('Hip Hop', 'Style of popular music of US black and Hispanic origin', '#800080', 1970, 'United States', 
 0.85, 85, 115, '0', -8.0, '4', 180, FALSE, (SELECT cluster_id FROM genre_clusters WHERE name = 'Popular Music')),

('Classical', 'Art music produced or rooted in Western culture', '#FFFF00', 1750, 'Europe', 
 0.45, 40, 200, '0', -20.0, '4', 900, FALSE, (SELECT cluster_id FROM genre_clusters WHERE name = 'Traditional')),

('Electronic Dance', 'Electronic music produced for nightclubs and festivals', '#00FF00', 1980, 'United States', 
 0.75, 120, 140, '0', -5.0, '4', 360, FALSE, (SELECT cluster_id FROM genre_clusters WHERE name = 'Electronic'));

-- 5. Populate subgenres using a DO block
DO $$
DECLARE
    rock_id VARCHAR(27);
    jazz_id VARCHAR(27);
    classical_id VARCHAR(27);
    hiphop_id VARCHAR(27);
    electronic_id VARCHAR(27);
BEGIN
    -- Get parent genre IDs
    SELECT genre_id INTO rock_id FROM genres WHERE name = 'Rock';
    SELECT genre_id INTO jazz_id FROM genres WHERE name = 'Jazz';
    SELECT genre_id INTO classical_id FROM genres WHERE name = 'Classical';
    SELECT genre_id INTO hiphop_id FROM genres WHERE name = 'Hip Hop';
    SELECT genre_id INTO electronic_id FROM genres WHERE name = 'Electronic Dance';
    
    -- Insert subgenres with explicitly controlled ID lengths
    INSERT INTO genres (
        genre_id, name, description, creation_year, country_of_origin,
        average_mode, bpm_lower, bpm_upper, dominant_key, typical_volume,
        time_signature, average_duration, is_subgenre, parent_genre_id
    ) VALUES
    ('G-' || upper(substring(md5(random()::text), 1, 12)) || 'S-' || upper(substring(md5(random()::text), 1, 10)), 
    'Heavy Metal', 'Loud, aggressive rock music style', 1970, 'United Kingdom', 
     0.15, 100, 160, '0', -4.0, '4', 240, TRUE, rock_id),
    
    ('G-' || upper(substring(md5(random()::text), 1, 12)) || 'S-' || upper(substring(md5(random()::text), 1, 10)), 
    'Bebop', 'Complex jazz style with fast tempos', 1940, 'United States', 
     0.60, 180, 250, '0', -12.0, '4', 180, TRUE, jazz_id),
    
    ('G-' || upper(substring(md5(random()::text), 1, 12)) || 'S-' || upper(substring(md5(random()::text), 1, 10)), 
    'Trap', 'Subgenre of hip hop with synthesized drums', 1990, 'United States', 
     0.90, 70, 100, '0', -6.0, '4', 210, TRUE, hiphop_id),
    
    ('G-' || upper(substring(md5(random()::text), 1, 12)) || 'S-' || upper(substring(md5(random()::text), 1, 10)), 
    'Baroque', 'Western classical music from 1600-1750', 1600, 'Europe', 
     0.40, 60, 120, '0', -18.0, '4', 420, TRUE, classical_id),
    
    ('G-' || upper(substring(md5(random()::text), 1, 12)) || 'S-' || upper(substring(md5(random()::text), 1, 10)), 
    'Techno', 'Electronic dance music with repetitive beats', 1980, 'United States', 
     0.80, 120, 150, '0', -4.5, '4', 480, TRUE, electronic_id);
END $$;

-- 6. Populate genre relationships
DO $$
DECLARE
    rock_id VARCHAR(27);
    jazz_id VARCHAR(27);
    classical_id VARCHAR(27);
    metal_id VARCHAR(27);
    bebop_id VARCHAR(27);
BEGIN
    -- Get genre IDs
    SELECT genre_id INTO rock_id FROM genres WHERE name = 'Rock';
    SELECT genre_id INTO jazz_id FROM genres WHERE name = 'Jazz';
    SELECT genre_id INTO classical_id FROM genres WHERE name = 'Classical';
    SELECT genre_id INTO metal_id FROM genres WHERE name = 'Heavy Metal';
    SELECT genre_id INTO bebop_id FROM genres WHERE name = 'Bebop';
    
    -- Create relationships
    PERFORM add_genre_relationship(jazz_id, rock_id, 7);
    PERFORM add_genre_relationship(classical_id, rock_id, 5);
    PERFORM add_genre_relationship(rock_id, metal_id, 9);
    PERFORM add_genre_relationship(jazz_id, bebop_id, 8);
END $$;