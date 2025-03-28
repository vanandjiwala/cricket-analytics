SELECT COUNT(*) as 'No Results'
FROM matches
WHERE result IN ('no result')
    AND season = '${ inputs.seasons.value }';