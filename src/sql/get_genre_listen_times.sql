SELECT
    g.id AS genre_id,
    g.name AS genre_name,
    SUM(sl.ms_played) AS total_listen_time
FROM
    SongListen sl
JOIN
    Song s ON sl.song_id = s.id
JOIN
    Album a ON s.album_id = a.id
JOIN
    Author au ON a.author_id = au.id
LEFT JOIN
    AuthorGenre ag ON au.id = ag.author_id
LEFT JOIN
    Genre g ON ag.genre_id = g.id
WHERE
    sl.timestamp >= :start_date
    AND sl.timestamp < :end_date
    AND g.id IS NOT NULL
    AND g.name != 'Pending'
GROUP BY
    g.id, g.name
ORDER BY
    total_listen_time DESC
LIMIT 100;
