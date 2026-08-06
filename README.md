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

A 4-page interactive dashboard built in Power BI Desktop.

---

## 📄 Page 1 — IPL Overview Dashboard

Displays Total Matches, Total Runs, Total Batsman Runs, Matches Won by Team, and Top 10 Batsmen.

<img src="screenshots/Screenshot%202026-08-02%20202452.png" alt="IPL Overview Dashboard" width="100%">

---

## 📄 Page 2 — Player Performance Dashboard

Shows Dismissal Types, Extras by Team, Top 10 Batsmen, and Runs by Over.

<img src="screenshots/Screenshot%202026-08-02%20202638.png" alt="Player Performance Dashboard" width="100%">

---

## 📄 Page 3 — Venue & Toss Insights

Analyzes IPL Match Venues, Toss Decisions, Matches by Toss Winner, and Runs by Venue.

<img src="screenshots/Screenshot%202026-08-02%20272729.png" alt="Venue & Toss Dashboard" width="100%">

---

## 📄 Page 4 — Team Winning Analysis Dashboard

Shows Matches Won by Team, Winning Margin by Team, Average Win by Team, and Win Share by Team.

<img src="screenshots/Screenshot%202026-08-02%20202800.png" alt="Team Winning Dashboard" width="100%">
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
