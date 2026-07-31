-- ============================================================
-- IPL Team & Player Performance Analysis — SQL Queries
-- ============================================================
-- Assumes two tables loaded from dataset/matches_clean.csv and
-- dataset/deliveries_clean.csv, e.g.:
--
--   CREATE TABLE matches (
--       id INT PRIMARY KEY, season INT, city TEXT, date DATE,
--       team1 TEXT, team2 TEXT, toss_winner TEXT, toss_decision TEXT,
--       result TEXT, dl_applied INT, winner TEXT,
--       win_by_runs INT, win_by_wickets INT, player_of_match TEXT,
--       venue TEXT, umpire1 TEXT, umpire2 TEXT, is_decisive BOOLEAN
--   );
--
--   CREATE TABLE deliveries (
--       match_id INT, inning INT, batting_team TEXT, bowling_team TEXT,
--       over INT, ball INT, batsman TEXT, non_striker TEXT, bowler TEXT,
--       is_super_over INT, wide_runs INT, bye_runs INT, legbye_runs INT,
--       noball_runs INT, penalty_runs INT, batsman_runs INT,
--       extra_runs INT, total_runs INT, player_dismissed TEXT,
--       dismissal_kind TEXT, fielder TEXT
--   );
--
-- Syntax targets standard ANSI SQL / MySQL / PostgreSQL (works with minor
-- tweaks in SQLite too, which is what Power BI's "Import from CSV" ends
-- up querying under the hood).
-- ============================================================


-- 1. Total matches won per team (excludes ties)
SELECT winner AS team, COUNT(*) AS total_wins
FROM matches
WHERE is_decisive = 1
GROUP BY winner
ORDER BY total_wins DESC;


-- 2. Orange Cap — Top 10 run scorers overall
SELECT batsman, SUM(batsman_runs) AS total_runs
FROM deliveries
GROUP BY batsman
ORDER BY total_runs DESC
LIMIT 10;


-- 3. Purple Cap — Top 10 wicket takers (run outs excluded, not credited to bowler)
SELECT bowler, COUNT(*) AS total_wickets
FROM deliveries
WHERE player_dismissed IS NOT NULL
  AND dismissal_kind <> 'run out'
GROUP BY bowler
ORDER BY total_wickets DESC
LIMIT 10;


-- 4. Team win percentage (wins / total matches played)
WITH team_matches AS (
    SELECT team1 AS team, id FROM matches
    UNION ALL
    SELECT team2 AS team, id FROM matches
),
played AS (
    SELECT team, COUNT(*) AS matches_played
    FROM team_matches
    GROUP BY team
),
won AS (
    SELECT winner AS team, COUNT(*) AS matches_won
    FROM matches
    WHERE is_decisive = 1
    GROUP BY winner
)
SELECT p.team,
       p.matches_played,
       COALESCE(w.matches_won, 0) AS matches_won,
       ROUND(100.0 * COALESCE(w.matches_won, 0) / p.matches_played, 2) AS win_pct
FROM played p
LEFT JOIN won w ON p.team = w.team
ORDER BY win_pct DESC;


-- 5. Toss decision impact — how often the toss winner also won the match
SELECT
    ROUND(100.0 * SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) / COUNT(*), 2)
        AS toss_winner_match_win_pct
FROM matches
WHERE is_decisive = 1;


-- 6. Average first-innings score by venue (highest scoring grounds)
SELECT m.venue,
       ROUND(AVG(d.total_runs), 2) AS avg_first_innings_score
FROM (
    SELECT match_id, SUM(total_runs) AS total_runs
    FROM deliveries
    WHERE inning = 1
    GROUP BY match_id
) d
JOIN matches m ON m.id = d.match_id
GROUP BY m.venue
ORDER BY avg_first_innings_score DESC;


-- 7. Best strike rate among batters with 100+ runs scored
SELECT batsman,
       SUM(batsman_runs) AS total_runs,
       COUNT(*) AS balls_faced,
       ROUND(100.0 * SUM(batsman_runs) / COUNT(*), 2) AS strike_rate
FROM deliveries
WHERE wide_runs = 0  -- wides aren't faced balls
GROUP BY batsman
HAVING SUM(batsman_runs) >= 100
ORDER BY strike_rate DESC
LIMIT 10;


-- 8. Best bowling economy among bowlers with 10+ overs bowled
SELECT bowler,
       ROUND(SUM(total_runs) * 1.0 / (COUNT(*) / 6.0), 2) AS economy_rate,
       COUNT(*) / 6 AS overs_bowled
FROM deliveries
WHERE wide_runs = 0 AND noball_runs = 0  -- illegal deliveries don't count toward overs
GROUP BY bowler
HAVING COUNT(*) / 6 >= 10
ORDER BY economy_rate ASC
LIMIT 10;


-- 9. Head-to-head record between two teams (edit team names as needed)
SELECT winner, COUNT(*) AS wins
FROM matches
WHERE (team1 = 'Mumbai Indians' AND team2 = 'Chennai Super Kings')
   OR (team1 = 'Chennai Super Kings' AND team2 = 'Mumbai Indians')
GROUP BY winner;


-- 10. Most Player-of-the-Match awards
SELECT player_of_match, COUNT(*) AS awards
FROM matches
GROUP BY player_of_match
ORDER BY awards DESC
LIMIT 10;


-- 11. Season-wise average total runs per match (scoring trend over time)
SELECT m.season, ROUND(AVG(t.match_total), 2) AS avg_runs_per_match
FROM (
    SELECT match_id, SUM(total_runs) AS match_total
    FROM deliveries
    GROUP BY match_id
) t
JOIN matches m ON m.id = t.match_id
GROUP BY m.season
ORDER BY m.season;


-- 12. Highest individual innings score (batsman runs in a single match)
SELECT batsman, match_id, SUM(batsman_runs) AS runs_in_match
FROM deliveries
GROUP BY batsman, match_id
ORDER BY runs_in_match DESC
LIMIT 10;
