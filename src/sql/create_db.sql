CREATE TABLE User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
);

CREATE TABLE Genre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE Author (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_id INTEGER,
    name TEXT,
    spotify_uri TEXT,
    img_url TEXT,
    FOREIGN KEY (genre_id) REFERENCES Genre(id)
);

CREATE TABLE AuthorGenre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER,
    genre_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES Author(id),
    FOREIGN KEY (genre_id) REFERENCES Genre(id)
);

CREATE TABLE Album (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER,
    spotify_uri TEXT,
    name TEXT,
    album_type TEXT,
    img_url TEXT,
    FOREIGN KEY (author_id) REFERENCES Author(id)
);

CREATE TABLE Song (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER,
    name TEXT,
    spotify_uri TEXT,
    FOREIGN KEY (album_id) REFERENCES Album(id)
);

CREATE TABLE SongListen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    song_id INTEGER,
    timestamp TEXT,
    conn_country TEXT,
    ip_address TEXT,
    platform TEXT,
    reason_start TEXT,
    reason_end TEXT,
    shuffle INTEGER,
    skipped INTEGER,
    offline INTEGER,
    incognito_mode INTEGER,
    offline_timestamp TEXT,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (song_id) REFERENCES Song(id)
);
