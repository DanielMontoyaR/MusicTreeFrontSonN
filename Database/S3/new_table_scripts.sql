-- Tabla de fanáticos (usuarios)
CREATE TABLE fans (
    fan_id SERIAL PRIMARY KEY,
    username VARCHAR(30) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    avatar_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    CONSTRAINT username_length CHECK (LENGTH(username) BETWEEN 3 AND 30),
    CONSTRAINT full_name_length CHECK (LENGTH(full_name) BETWEEN 1 AND 100)
);

-- Relación fan-géneros favoritos
CREATE TABLE fan_favorite_genres (
    fan_id INT NOT NULL REFERENCES fans(fan_id) ON DELETE CASCADE,
    genre_id VARCHAR(38) NOT NULL REFERENCES genres(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (fan_id, genre_id)
);

-- Tabla de avatares predefinidos
CREATE TABLE avatars (
    avatar_id SERIAL PRIMARY KEY,
    image_path VARCHAR(255) NOT NULL,
    description VARCHAR(100)
);