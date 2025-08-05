INSERT INTO `Queue` (`owner`, `song_uri`, `timestamp`, `ms_played`, `conn_country`, `ip_addr`, `incognito_mode`, `offline`, `skipped`, `shuffle`, `reason_end`, `reason_start`)
VALUES (%(owner)s, %(song_uri)s, %(timestamp)s, %(ms_played)s, %(conn_country)s, %(ip_addr)s, %(incognito_mode)s, %(offline)s, %(skipped)s, %(shuffle)s, %(reason_end)s, %(reason_start)s);
