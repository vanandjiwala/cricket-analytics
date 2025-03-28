SELECT SUM(
        CASE
            WHEN result = 'wickets' THEN 1
            ELSE 0
        END
    ) as 'Chasing',
    SUM(
        CASE
            WHEN result = 'runs' THEN 1
            ELSE 0
        END
    ) as 'Defending'
FROM matches
WHERE result NOT IN ('no result', 'tie')
    AND season = '${ inputs.seasons.value }';