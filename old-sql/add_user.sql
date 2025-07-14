INSERT INTO User (username, password, profile_picture, last_time_uploaded)
VALUES (:username, :password, :profile_picture, datetime('now'));