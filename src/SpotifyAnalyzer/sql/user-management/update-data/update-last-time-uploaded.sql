UPDATE `User`
SET `last_time_uploaded` = %(new_time)s
WHERE `id` = %(id)s;
