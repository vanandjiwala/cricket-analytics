---
title: IPL Analysis

queries:
  - total_seasons: total_seasons.sql
  - total_matches: matches_played.sql
  - seasons: seasons.sql
  - super_overs: super_overs.sql
  - no_results: no_results.sql
  - teams: teams.sql
  - chasing_stats: chasing_stats.sql
---

<Grid cols=1>
<Dropdown
title="Season" 
    data={seasons} 
    name=seasons 
    value=seasons 
/>
</Grid>

<Grid cols=5>
<BigValue 
  data={total_seasons} 
  value="Total Seasons"
/>

<BigValue 
  data={total_matches} 
  value="Matches Played"
/>

<BigValue 
  data={super_overs} 
  value="Super Overs"
/>

<BigValue 
  data={no_results} 
  value="No Results"
/>

<BigValue 
  data={teams} 
  value="Teams"
/>
</Grid>

<Grid cols=3>
<BigValue 
  data={chasing_stats} 
  value="Chasing"
/>

<BigValue 
  data={chasing_stats} 
  value="Defending"
/>
</Grid>
