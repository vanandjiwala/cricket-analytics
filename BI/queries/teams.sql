SELECT COUNT(DISTINCT team1) as 'Teams'
FROM matches
WHERE season = '${ inputs.seasons.value }';