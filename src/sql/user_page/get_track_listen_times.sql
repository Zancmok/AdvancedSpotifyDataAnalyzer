SELECT
    s.id AS song_id,
    s.name AS song_name,
    s.spotify_uri AS spotify_uri,
    a.img_url AS img_url,
    SUM(sl.ms_played) AS total_listen_time
FROM
    SongListen sl
JOIN
    Song s ON sl.song_id = s.id
JOIN
    Album a ON a.id = s.album_id
WHERE
    sl.timestamp >= :start_date
    AND sl.timestamp < :end_date
    AND sl.user_id = :user_id
GROUP BY
    s.id
ORDER BY
    total_listen_time DESC
