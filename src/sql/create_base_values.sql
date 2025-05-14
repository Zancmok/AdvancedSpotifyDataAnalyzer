INSERT OR IGNORE  INTO Genre (id, name)
VALUES (0, 'Pending');

INSERT OR IGNORE  INTO Author (id, name, spotify_uri, img_url)
VALUES (0, 'Pending Artist', 'spotify:artist:pending', 'https://icons.veryicon.com/png/o/miscellaneous/hfy/temporary-1.png');

INSERT OR IGNORE  INTO AuthorGenre (id, author_id, genre_id)
VALUES (0, 0, 0);

INSERT OR IGNORE  INTO Album (id, author_id, spotify_uri, name, album_type, img_url)
VALUES (0, 0, 'spotify:album:pending', 'Pending Album', 'Pending Album Type', 'https://icons.veryicon.com/png/o/miscellaneous/hfy/temporary-1.png')
