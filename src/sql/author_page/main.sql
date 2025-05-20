SELECT
    a.name,
    a.img_url as pfp
FROM Author a
WHERE id = :author_id;
