# IPL Team & Player Performance Analysis

End-to-end analysis of IPL match and ball-by-ball data — Python for
cleaning/analysis, SQL for querying, and a 4-page Power BI dashboard.

## 📁 Folder Structure
```
IPL-Analysis/
│
├── dataset/
│   ├── matches.csv              # raw match-level data
│   ├── deliveries.csv           # raw ball-by-ball data
│   ├── matches_clean.csv        # output of data_cleaning.py
│   ├── deliveries_clean.csv     # output of data_cleaning.py
│   └── summary_*.csv            # aggregated outputs from analysis.py (for Power BI)
│
├── python/
│   ├── generate_sample_data.py  # creates the sample dataset (see note below)
│   ├── data_cleaning.py         # cleans & standardizes raw data
│   └── analysis.py              # runs analysis, saves charts to screenshots/
│
├── sql/
│   └── queries.sql              # 12 analysis queries (wins, orange/purple cap, etc.)
│
├── powerbi/
│   └── PowerBI_Setup_Guide.md   # step-by-step guide + DAX measures used to build the dashboard
│
├── screenshots/                 # Power BI dashboard screenshots (see below)
│
└── README.md
```

## 📊 Power BI Dashboard

4-page interactive dashboard built in Power BI Desktop on top of the cleaned CSVs.

### Page 1 — IPL Overview Dashboard
Total matches, total runs, matches won by team, top 10 batsmen by runs.

![IPL Overview Dashboard](screenshots/dashboard_1_overview.jpg)

### Page 2 — Player Performance Dashboard
Dismissal type breakdown, extras by team, top 10 batsmen, runs-by-over trend.

![Player Performance Dashboard](screenshots/dashboard_2_player_performance.jpg)

### Page 3 — Venue & Toss Insights
Match venues on map, toss decision split, matches by toss winner, runs by venue.

![Venue & Toss Insights](screenshots/dashboard_3_venue_toss.jpg)

### Page 4 — Team Winning Analysis Dashboard
Matches won by team, winning margin (runs vs wickets), average win margin, win share by team.

![Team Winning Analysis Dashboard](screenshots/dashboard_4_team_winning.jpg)

## ⚠️ About the dataset
This repo ships with a **synthetically generated** dataset (`generate_sample_data.py`)
so the full pipeline runs out of the box — real IPL data wasn't available in
this environment. It mimics the schema of the well-known Kaggle
"IPL Complete Dataset" (matches + ball-by-ball deliveries).

**To use real data instead:** download the actual dataset (e.g. from Kaggle)
and drop `matches.csv` + `deliveries.csv` into `dataset/` with the same
column names below — everything downstream (cleaning, analysis, SQL, Power BI)
works unchanged.

**matches.csv columns:** `id, season, city, date, team1, team2, toss_winner, toss_decision, result, dl_applied, winner, win_by_runs, win_by_wickets, player_of_match, venue, umpire1, umpire2`

**deliveries.csv columns:** `match_id, inning, batting_team, bowling_team, over, ball, batsman, non_striker, bowler, is_super_over, wide_runs, bye_runs, legbye_runs, noball_runs, penalty_runs, batsman_runs, extra_runs, total_runs, player_dismissed, dismissal_kind, fielder`

## 🚀 How to run
```bash
cd IPL-Analysis
pip install pandas numpy matplotlib

# 1. (optional) regenerate the sample dataset
python python/generate_sample_data.py

# 2. clean the raw data
python python/data_cleaning.py

# 3. run the analysis (prints insights, saves charts + summary CSVs)
python python/analysis.py
```

For SQL: load `matches_clean.csv` and `deliveries_clean.csv` into any
database (MySQL, PostgreSQL, SQLite) and run the queries in `sql/queries.sql`.

For Power BI: follow `powerbi/PowerBI_Setup_Guide.md` for the data model,
DAX measures, and page-by-page visual layout used to build the dashboard above.

## 📌 Key insights
- **Most wins:** Kolkata Knight Riders, Gujarat Titans lead the standings
- **Toss impact:** toss winner elects to field ~60% of the time
- **Win margins:** top teams win more often by wickets (chasing) than by defending
- **Venues:** M. Chinnaswamy Stadium and Sawai Mansingh Stadium are the highest-scoring grounds
- **Dismissals:** catches account for ~48% of all wickets, the most common mode

## 🛠 Tech stack
Python (pandas, numpy, matplotlib) · SQL · Power BI

## 📌 Possible extensions
- Add player career trajectories (runs/wickets per season)
- Predictive model for match win probability
- Death-overs vs powerplay economy comparison
- Head-to-head team rivalry dashboard page
