SELECT EXISTS(
    SELECT 1 FROM Song WHERE spotify_uri = :spotify_uri
);
