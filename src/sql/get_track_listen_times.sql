SELECT
    s.id AS song_id,
    s.name AS song_name,
    s.spotify_uri AS spotify_uri,
    SUM(sl.ms_played) AS total_listen_time
FROM
    SongListen sl
JOIN
    Song s ON sl.song_id = s.id
WHERE
    sl.timestamp >= :start_date
    AND sl.timestamp < :end_date
GROUP BY
    s.id
ORDER BY
    total_listen_time DESC
LIMIT 100;
