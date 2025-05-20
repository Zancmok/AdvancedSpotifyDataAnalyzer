SELECT
    u.id AS user_id,
    u.username AS username,
    SUM(sl.ms_played) AS listen_time
FROM
    User u
JOIN
    SongListen sl ON u.id = sl.user_id
JOIN
    Song s ON sl.song_id = s.id
JOIN
    Album a ON s.album_id = a.id
JOIN
    Author au ON a.author_id = au.id
JOIN
    AuthorGenre ag ON au.id = ag.author_id
WHERE
    sl.timestamp >= :start_date
    AND sl.timestamp < :end_date
    AND s.id = :song_id
GROUP BY
    u.id
ORDER BY
    listen_time DESC;
