UPDATE Album
SET author_id = (
    SELECT id FROM Author WHERE spotify_uri = :author_uri
)
WHERE spotify_uri = :album_uri;
