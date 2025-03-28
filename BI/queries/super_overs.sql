SELECT SUM(
        CASE
            WHEN super_over = 'Y' THEN 1
            ELSE 0
        END
    ) as 'Super Overs'
FROM matches
WHERE season = '${ inputs.seasons.value }';