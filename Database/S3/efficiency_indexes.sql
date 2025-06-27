-- Índices para búsquedas rápidas
CREATE INDEX idx_fans_username ON fans(username);
CREATE INDEX idx_fan_genres ON fan_favorite_genres(fan_id);
CREATE INDEX idx_artist_genres ON artist_genres(genre_id);
CREATE INDEX idx_artist_subgenres ON artist_subgenres(subgenre_id);
CREATE INDEX idx_artists_name ON artists(name);