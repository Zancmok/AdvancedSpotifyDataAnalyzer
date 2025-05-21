SELECT
    a.id AS album_id,
    a.name AS album_name,
    a.spotify_uri,
    a.img_url,
    au.name AS author_name,
    SUM(sl.ms_played) AS total_listen_time
FROM
    SongListen sl
JOIN
    Song s ON sl.song_id = s.id
JOIN
    Album a ON s.album_id = a.id
JOIN
    Author au ON a.author_id = au.id
WHERE
    sl.timestamp >= :start_date
    AND sl.timestamp < :end_date
    AND a.id != 0
GROUP BY
    a.id
ORDER BY
    total_listen_time DESC
