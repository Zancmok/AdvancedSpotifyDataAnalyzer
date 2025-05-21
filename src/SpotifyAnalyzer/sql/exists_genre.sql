SELECT EXISTS(
    SELECT 1 FROM Genre WHERE name = :name
);
