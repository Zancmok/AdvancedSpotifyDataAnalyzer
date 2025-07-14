SELECT
    a.name,
    a.img_url as pfp
FROM Album a
WHERE id = :album_id;
