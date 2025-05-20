SELECT
    s.name,
    a.img_url AS pfp
FROM
    Song s
JOIN
    Album a ON s.album_id = a.id
WHERE
    s.id = :song_id;
