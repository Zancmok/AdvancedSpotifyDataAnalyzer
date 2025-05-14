SELECT EXISTS(
    SELECT 1 FROM Album WHERE spotify_uri = :spotify_uri
);
