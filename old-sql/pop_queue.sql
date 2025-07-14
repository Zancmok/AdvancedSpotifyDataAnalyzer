DELETE FROM APIQueueElement
WHERE id = (
    SELECT id FROM APIQueueElement
    ORDER BY id ASC
    LIMIT 1
);
