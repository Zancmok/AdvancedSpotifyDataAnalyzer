DELETE FROM `Queue`
WHERE `owner` = %(user_id)s;
