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
├── screenshots/                 # Power BI dashboard screenshots (embedded below)
│
└── README.md
```

## 📊 Power BI Dashboard

A 4-page interactive dashboard built in Power BI Desktop on top of the cleaned CSVs.

### Page 1 — IPL Overview Dashboard
The landing page. Three summary cards at the top (Total Matches, Total Runs,
Total Batsman Runs) give a quick pulse of the tournament, followed by two
charts: **Matches won by Team** (who's dominating overall) and
**Top 10 Batsman by Runs** (leading run-scorers across all seasons).

![IPL Overview Dashboard](https://github.com/roopan-99/IPL-Team-Player-Performance-Analysis/blob/3a613741dff0d19c61fe34af7a6538fd6dd19f4e/screenshorts/Screenshot%202026-08-02%20202452.png)

### Page 2 — Player Performance Dashboard
Digs deeper into how players get out and score. **Dismissal Types** (donut)
shows catches are the most common dismissal (~48.5%), followed by bowled
and run out. **Extras by Team** compares wides vs no-balls conceded per
team. **Top 10 Batsmen** ranks scorers, and **Runs by Over** shows scoring
trend across the 20 overs of an innings — typically higher in the first
over (powerplay) and dipping mid-innings.

![Player Performance Dashboard](https://github.com/roopan-99/IPL-Team-Player-Performance-Analysis/blob/9d66eaa89ec6c90b34d50d551b84e54228de4460/screenshorts/Screenshot%202026-08-02%20202638.png)

### Page 3 — Venue & Toss Insights
**IPL Match Venues** map plots every stadium used, with mini pie charts per
city. **Toss Decision** shows teams choose to field first (~59.6%) more
often than bat first (~40.4%) — chasing is generally favored in T20.
**Matches by Toss Winner** and **Runs by Venue** round out venue-level
scoring patterns (e.g. M. Chinnaswamy Stadium trends highest-scoring).

![Venue & Toss Insights](https://github.com/roopan-99/IPL-Team-Player-Performance-Analysis/blob/2843500dc62297125f006f997c5addfd6154ebed/screenshorts/Screenshot%202026-08-02%20202729.png)

### Page 4 — Team Winning Analysis Dashboard
The team-performance summary. **Matches won by Team** and **Win Share by
Team** (donut) show Kolkata Knight Riders and Gujarat Titans leading
(17.2% and 15.9% of all wins respectively). **Winning Margin by Team**
splits wins by runs (defending) vs wickets (chasing), and **Average Win by
Team** shows the typical victory margin for each side.

![Team Winning Analysis Dashboard](https://github.com/roopan-99/IPL-Team-Player-Performance-Analysis/blob/833ac0a375875d7ac20d8babb105fa750eaf8f7f/screenshorts/Screenshot%202026-08-02%20202800.png)

> **Note:** the "Total Runes" / "Total Batsman Runes" card titles on Page 1
> are a small typo (should read "Runs") — cosmetic only, doesn't affect the
> underlying data or calculations.

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
- **Most wins:** Kolkata Knight Riders (17.2% win share), Gujarat Titans (15.9%) lead the standings
- **Toss impact:** teams elect to field first ~60% of the time after winning the toss
- **Win margins:** top teams win more often by wickets (chasing) than by defending totals
- **Venues:** M. Chinnaswamy Stadium and Sawai Mansingh Stadium are the highest-scoring grounds
- **Dismissals:** catches account for ~48.5% of all wickets, by far the most common mode
- **Scoring trend:** runs per over generally decline across the innings after an early peak

## 🛠 Tech stack
Python (pandas, numpy, matplotlib) · SQL · Power BI

## 📌 Possible extensions
- Add player career trajectories (runs/wickets per season)
- Predictive model for match win probability
- Death-overs vs powerplay economy comparison
- Head-to-head team rivalry dashboard page
