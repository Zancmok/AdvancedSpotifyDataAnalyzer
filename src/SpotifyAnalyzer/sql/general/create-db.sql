CREATE TABLE IF NOT EXISTS `Genre` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(128) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS `Artist` (
    `uri` VARCHAR(32) PRIMARY KEY,
    `image_url` VARCHAR(255),
    `image_height` INT,
    `image_width` INT,
    `name` VARCHAR(128) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS `GenreArtist` (
    `genre_id` INT,
    `artist_uri` VARCHAR(32),
    PRIMARY KEY (`genre_id`, `artist_uri`),
    FOREIGN KEY (`genre_id`) REFERENCES `Genre`(`id`),
    FOREIGN KEY (`artist_uri`) REFERENCES `Artist`(`uri`)
);

CREATE TABLE IF NOT EXISTS `Album` (
    `uri` VARCHAR(32) PRIMARY KEY,
    `album_type` VARCHAR(32) NOT NULL,
    `total_tracks` INT NOT NULL,
    `image_url` VARCHAR(255),
    `image_height` INT,
    `image_width` INT,
    `name` VARCHAR(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS `AlbumArtist` (
    `artist_uri` VARCHAR(32),
    `album_uri` VARCHAR(32),
    PRIMARY KEY (`artist_uri`, `album_uri`),
    FOREIGN KEY (`artist_uri`) REFERENCES `Artist`(`uri`),
    FOREIGN KEY (`album_uri`) REFERENCES `Album`(`uri`)
);

CREATE TABLE IF NOT EXISTS `Song` (
    `uri` VARCHAR(32) PRIMARY KEY,
    `album_uri` VARCHAR(32),
    `duration` INT NOT NULL,
    `explicit` TINYINT(1) NOT NULL,
    `name` VARCHAR(128) NOT NULL,
    `preview_url` VARCHAR(255),
    `is_local` TINYINT(1) NOT NULL,
    FOREIGN KEY (`album_uri`) REFERENCES `Album`(`uri`)
);

CREATE TABLE IF NOT EXISTS `SongArtist` (
    `song_uri` VARCHAR(32),
    `artist_uri` VARCHAR(32),
    PRIMARY KEY (`song_uri`, `artist_uri`),
    FOREIGN KEY (`song_uri`) REFERENCES `Song`(`uri`),
    FOREIGN KEY (`artist_uri`) REFERENCES `Artist`(`uri`)
);

CREATE TABLE IF NOT EXISTS `User` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(20) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `permission_level` INT NOT NULL DEFAULT 0,
    `profile_picture` LONGBLOB DEFAULT NULL,
    `last_time_uploaded` DATETIME DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS `Friendship` (
    `user1` INT,
    `user2` INT,
    PRIMARY KEY (`user1`, `user2`),
    FOREIGN KEY (`user1`) REFERENCES `User`(`id`),
    FOREIGN KEY (`user2`) REFERENCES `User`(`id`),
    CHECK (`user1` < `user2`)
);

CREATE TABLE IF NOT EXISTS `Group` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(20) NOT NULL,
    `owner_id` INT NOT NULL,
    `profile_picture` BLOB,
    FOREIGN KEY (owner_id) REFERENCES `User`(`id`)
);

CREATE TABLE IF NOT EXISTS `GroupUser` (
    `group_id` INT,
    `user_id` INT,
    `permission_level` INT NOT NULL DEFAULT 0,
    PRIMARY KEY (`group_id`, `user_id`),
    FOREIGN KEY (group_id) REFERENCES `Group`(`id`),
    FOREIGN KEY (user_id) REFERENCES `User`(`id`)
);

CREATE TABLE IF NOT EXISTS `SongListen` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT,
    `song_uri` VARCHAR(32),
    `timestamp` DATETIME NOT NULL,
    `ms_played` INT NOT NULL,
    `conn_country` VARCHAR(20) NOT NULL,
    `ip_addr` VARCHAR(32) NOT NULL,
    `reason_start` VARCHAR(20) NOT NULL,
    `reason_end` VARCHAR(20) NOT NULL,
    `shuffle` TINYINT(1) NOT NULL,
    `skipped` TINYINT(1) NOT NULL,
    `offline` TINYINT(1) NOT NULL,
    `incognito_mode` TINYINT(1) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES `User`(`id`),
    FOREIGN KEY (song_uri) REFERENCES `Song`(`uri`)
);

CREATE TABLE IF NOT EXISTS `Queue` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `owner` INT,
    `song_uri` VARCHAR(32),
    `timestamp` DATETIME NOT NULL,
    `ms_played` INT NOT NULL,
    `conn_country` VARCHAR(20) NOT NULL,
    `ip_addr` VARCHAR(32) NOT NULL,
    `reason_start` VARCHAR(20) NOT NULL,
    `reason_end` VARCHAR(20) NOT NULL,
    `shuffle` TINYINT(1) NOT NULL,
    `skipped` TINYINT(1) NOT NULL,
    `offline` TINYINT(1) NOT NULL,
    `incognito_mode` TINYINT(1) NOT NULL,
    FOREIGN KEY (owner) REFERENCES `User`(`id`)
);
