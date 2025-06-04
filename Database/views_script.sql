CREATE OR REPLACE VIEW genre_hierarchy AS
WITH RECURSIVE genre_tree AS (
    -- Base case: main genres (no parent)
    SELECT 
        g.genre_id,
        g.name,
        g.parent_genre_id,
        g.is_subgenre,
        0 AS level,
        ARRAY[g.genre_id]::VARCHAR[] AS path,
        ARRAY[g.name]::VARCHAR[] AS name_path
    FROM genres g
    WHERE g.parent_genre_id IS NULL
    
    UNION ALL
    
    -- Recursive case: subgenres
    SELECT 
        g.genre_id,
        g.name,
        g.parent_genre_id,
        g.is_subgenre,
        gt.level + 1,
        gt.path || g.genre_id::VARCHAR,
        gt.name_path || g.name::VARCHAR
    FROM genres g
    JOIN genre_tree gt ON g.parent_genre_id = gt.genre_id
)
SELECT 
    genre_id,
    name,
    parent_genre_id,
    is_subgenre,
    level,
    path,
    name_path
FROM genre_tree
ORDER BY path;