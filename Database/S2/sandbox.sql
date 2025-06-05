INSERT INTO artists (artist_id, name, biography, country_of_origin, cover_image_path, status, created_at)
VALUES
    ('The Midnight Echoes2', 'Alternative rock band formed in 2010 known for their atmospheric soundscapes.', 'United States', '/covers/midnight_echoes.jpg', 'active', '2020-05-15 14:30:00');

select * from genres where is_subgenre = true
select * from genres where is_subgenre = false
select * from genre_relationships

select * from artists
select * from artist_activity_years
select * from artist_photos
select * from band_members
select * from artist_genres

select * from genres

SELECT register_artist(
    'The Midnight Echoes', 
    'Alternative rock band formed in 2010 known for their atmospheric soundscapes.',
    'United States',
    'https://cdn.discordapp.com/attachments/964576637725315072/1379931432587231322/1900x1900-000000-80-0-0_1.jpg?ex=684208cb&is=6840b74b&hm=395ce8696675298481aba89cd72243ad69cf59244c8703030267f926dcc72122&',
	1980,
	2016,
	false,
    ARRAY['G-105AD5A53709000000000000', 'G-792432650DE6000000000000'],
	ARRAY['G-105AD5A53709000000000000', 'G-792432650DE6000000000000']
);

SELECT register_artist(
    'Electra Complex', 
    'Electronic music duo blending synthwave with modern EDM elements.',
    'Sweden',
    'https://cdn.discordapp.com/attachments/964576637725315072/1379931037701902406/a2326069825_16.jpg?ex=6842086d&is=6840b6ed&hm=23c4a80f75ef94af4123615709f980ee8451b6e9cc3acb4fb66353a69db5299f&',
    ARRAY['G-F53F82025731000000000000','G-8F00468E77B4S-DA24D98E74']
);

SELECT register_artist(
    'Mariana Trench', 
    'Experimental jazz collective pushing boundaries of improvisation.',
    'Japan',
    'https://cdn.discordapp.com/attachments/964576637725315072/1379931798330675290/Marianas_Trench_Phantoms.png?ex=68420922&is=6840b7a2&hm=8d780e1325ae0b1835fd9e7b26ed2a74c0a05459f6098e6d7de4e9351853640d&',
    ARRAY['G-792432650DE6000000000000','G-8F00468E77B4S-DA24D98E74']
);