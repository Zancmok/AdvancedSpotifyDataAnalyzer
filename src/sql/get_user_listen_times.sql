SELECT 
    u.id AS user_id,
    u.username AS username,
    u.profile_picture AS profile_picture,
    SUM(sl.ms_played) AS liten_time
FROM 
    User u
JOIN 
    SongListen sl ON u.id = sl.user_id
WHERE 
    sl.timestamp >= :start_date
    AND sl.timestamp < :end_date
GROUP BY 
    u.id
ORDER BY 
    liten_time DESC;
