-- Indexes for better performance on common queries
CREATE INDEX idx_artists_created_at ON artists(created_at);
CREATE INDEX idx_artist_genres_artist_id ON artist_genres(artist_id);
CREATE INDEX idx_albums_artist_id ON albums(artist_id);
CREATE INDEX idx_artist_activity_years_artist_id ON artist_activity_years(artist_id);
CREATE INDEX idx_band_members_artist_id ON band_members(artist_id);