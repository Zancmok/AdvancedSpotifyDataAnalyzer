SELECT
    au.id AS author_id,
    au.name AS author_name,
    au.spotify_uri,
    au.img_url,
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
    AND au.id != 0
    AND sl.user_id = :user_id
GROUP BY
    au.id
ORDER BY
    total_listen_time DESC
