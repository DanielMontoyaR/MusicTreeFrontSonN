-- Create enum types first
CREATE TYPE activity_status AS ENUM ('active', 'inactive');
CREATE TYPE musical_mode AS ENUM ('C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'none');

-- Artists table
CREATE TABLE artists (
    artist_id VARCHAR(15) PRIMARY KEY, -- Format: A-<12 alphanum chars>
    name VARCHAR(100) NOT NULL,
    biography TEXT,
    country_of_origin VARCHAR(100),
    status activity_status NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cover_image_path TEXT,
    CONSTRAINT name_length CHECK (LENGTH(name) BETWEEN 3 AND 100)
);

-- Artist activity years (handles ranges and single years)
CREATE TABLE artist_activity_years (
    id SERIAL PRIMARY KEY,
    artist_id VARCHAR(15) NOT NULL REFERENCES artists(artist_id) ON DELETE CASCADE,
    start_year INTEGER NOT NULL,
    end_year INTEGER,
    is_present BOOLEAN DEFAULT FALSE,
    CONSTRAINT valid_years CHECK (
        (end_year IS NULL AND is_present = FALSE) OR
        (end_year IS NOT NULL AND end_year >= start_year) OR
        (is_present = TRUE)
    )
);

-- Band members
CREATE TABLE band_members (
    id SERIAL PRIMARY KEY,
    artist_id VARCHAR(15) NOT NULL REFERENCES artists(artist_id) ON DELETE CASCADE,
    full_name VARCHAR(100) NOT NULL,
    instrument VARCHAR(100),
    start_period VARCHAR(50),
    end_period VARCHAR(50),
    is_current BOOLEAN DEFAULT TRUE
);

-- Albums
CREATE TABLE albums (
    album_id VARCHAR(30) PRIMARY KEY, -- Format: A-<artist_id>-D-<12 alphanum chars>
    artist_id VARCHAR(15) NOT NULL REFERENCES artists(artist_id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    release_date DATE,
    cover_image_path TEXT,
    duration_seconds INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Artist-genre relationships
CREATE TABLE artist_genres (
    artist_id VARCHAR(15) NOT NULL REFERENCES artists(artist_id) ON DELETE CASCADE,
    genre_id VARCHAR(38) NOT NULL REFERENCES genres(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (artist_id, genre_id)
);

-- Artist-subgenre relationships
CREATE TABLE artist_subgenres (
    artist_id VARCHAR(15) NOT NULL REFERENCES artists(artist_id) ON DELETE CASCADE,
    subgenre_id VARCHAR(38) NOT NULL REFERENCES genres(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (artist_id, subgenre_id)
);

-- Comments thread for artists
CREATE TABLE artist_comments (
    id SERIAL PRIMARY KEY,
    artist_id VARCHAR(15) NOT NULL REFERENCES artists(artist_id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    author VARCHAR(100) NOT NULL
);

-- Photo album for artists
CREATE TABLE artist_photos (
    id SERIAL PRIMARY KEY,
    artist_id VARCHAR(15) NOT NULL REFERENCES artists(artist_id) ON DELETE CASCADE,
    image_path TEXT NOT NULL,
    upload_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

-- Event calendar for artists
CREATE TABLE artist_events (
    id SERIAL PRIMARY KEY,
    artist_id VARCHAR(15) NOT NULL REFERENCES artists(artist_id) ON DELETE CASCADE,
    event_date TIMESTAMP NOT NULL,
    location VARCHAR(200) NOT NULL,
    description TEXT
);


