INSERT INTO `SongListen` (`user_id`, `song_uri`, `timestamp`, `ms_played`, `conn_country`, `ip_addr`, `reason_start`, `reason_end`, `shuffle`, `skipped`, `offline`, `incognito_mode`)
VALUES (%(user_id)s, %(song_uri)s, %(timestamp)s, %(ms_played)s, %(conn_country)s, %(ip_addr)s, %(reason_start)s, %(reason_end)s, %(shuffle)s, %(skipped)s, %(offline)s, %(incognito_mode)s);
