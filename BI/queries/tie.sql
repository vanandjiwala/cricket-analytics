SELECT COUNT(*) as 'Tie'
FROM matches
WHERE result IN ('tie')
    AND season = '${ inputs.seasons.value }';