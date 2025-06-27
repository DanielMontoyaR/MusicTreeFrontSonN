CREATE TABLE artist_ratings (
    rating_id SERIAL PRIMARY KEY,
    fan_id INT NOT NULL REFERENCES fans(fan_id) ON DELETE CASCADE,
    artist_id VARCHAR(15) NOT NULL REFERENCES artists(artist_id) ON DELETE CASCADE,
    rating SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_fan_artist_rating UNIQUE (fan_id, artist_id)
);

ALTER TABLE artists ADD COLUMN average_rating DECIMAL(3,2) DEFAULT 0;
ALTER TABLE artists ADD COLUMN rating_count INT DEFAULT 0;

