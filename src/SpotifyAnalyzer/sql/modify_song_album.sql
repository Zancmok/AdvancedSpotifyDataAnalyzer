UPDATE Song
SET album_id = (
    SELECT id FROM Album WHERE spotify_uri = :album_uri
)
WHERE spotify_uri = :song_uri;
