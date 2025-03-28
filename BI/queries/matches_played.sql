SELECT COUNT(*) as 'Matches Played'
FROM ipl_data.matches
WHERE season = '${ inputs.seasons.value }';