SELECT EXISTS(
    SELECT 1 FROM Author WHERE spotify_uri = :spotify_uri
);
