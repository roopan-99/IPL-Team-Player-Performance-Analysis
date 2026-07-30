"""
generate_sample_data.py
------------------------
Generates a synthetic (but realistic-structured) IPL dataset:
    dataset/matches.csv
    dataset/deliveries.csv

NOTE: This is randomly-simulated data used as a stand-in so the rest of the
pipeline (cleaning, analysis, SQL, Power BI) has something to run against.
If you have the real Kaggle "IPL Complete Dataset" (matches.csv +
deliveries.csv), just drop those files into dataset/ with the same column
names and skip running this script — everything downstream will still work.
"""

import random
import pandas as pd
import numpy as np
from datetime import date, timedelta

random.seed(42)
np.random.seed(42)

TEAMS = [
    "Mumbai Indians", "Chennai Super Kings", "Royal Challengers Bengaluru",
    "Kolkata Knight Riders", "Delhi Capitals", "Rajasthan Royals",
    "Sunrisers Hyderabad", "Punjab Kings", "Gujarat Titans", "Lucknow Super Giants"
]

VENUES = [
    "Wankhede Stadium, Mumbai", "M. A. Chidambaram Stadium, Chennai",
    "M. Chinnaswamy Stadium, Bengaluru", "Eden Gardens, Kolkata",
    "Arun Jaitley Stadium, Delhi", "Sawai Mansingh Stadium, Jaipur",
    "Rajiv Gandhi International Stadium, Hyderabad", "Narendra Modi Stadium, Ahmedabad",
    "BRSABV Ekana Cricket Stadium, Lucknow", "Punjab Cricket Association Stadium, Mohali"
]

CITIES = {v: v.split(",")[-1].strip() for v in VENUES}

# Generate a pool of ~18 player names per team
FIRST_NAMES = ["Rohit","Virat","Suryakumar","Rishabh","Shubman","Jasprit","Ravindra",
               "Hardik","KL","Shreyas","Yuzvendra","Mohammed","Axar","Ishan","Prithvi",
               "Sanju","Devdutt","Ruturaj","Deepak","Kuldeep","Arshdeep","Umran","Tilak",
               "Rinku","Nitish","Yashasvi","Rahul","Avesh","Washington","Shardul"]
LAST_NAMES = ["Sharma","Kohli","Yadav","Pant","Gill","Bumrah","Jadeja","Pandya","Rahul",
              "Iyer","Chahal","Shami","Patel","Kishan","Shaw","Samson","Padikkal",
              "Gaikwad","Chahar","Kumar","Singh","Malik","Varma","Singh","Reddy","Jaiswal",
              "Tripathi","Khan","Sundar","Thakur"]

def build_squads():
    squads = {}
    pool = list({f"{f} {l}" for f in FIRST_NAMES for l in LAST_NAMES})
    random.shuffle(pool)
    idx = 0
    for t in TEAMS:
        squads[t] = pool[idx:idx+16]
        idx += 16
    return squads

SQUADS = build_squads()

def simulate_innings(match_id, inning_no, batting_team, bowling_team, target=None):
    rows = []
    batsmen = SQUADS[batting_team][:]
    random.shuffle(batsmen)
    bowlers = SQUADS[bowling_team][:6]
    striker_idx = 0
    non_striker_idx = 1
    wickets = 0
    total = 0
    for over in range(1, 21):
        bowler = bowlers[over % len(bowlers)]
        for ball in range(1, 7):
            if wickets >= 10:
                break
            if target is not None and total >= target:
                break
            striker = batsmen[striker_idx]
            non_striker = batsmen[non_striker_idx]

            extra_type = np.random.choice(
                ["none","wide","noball","bye","legbye"], p=[0.88,0.06,0.02,0.02,0.02]
            )
            wide_runs = noball_runs = bye_runs = legbye_runs = 0
            batsman_runs = 0
            player_dismissed, dismissal_kind, fielder = "", "", ""

            if extra_type == "wide":
                wide_runs = 1
            elif extra_type == "noball":
                noball_runs = 1
                batsman_runs = np.random.choice([0,1,2,4,6], p=[0.5,0.2,0.1,0.15,0.05])
            elif extra_type == "bye":
                bye_runs = np.random.choice([1,2,4], p=[0.7,0.2,0.1])
            elif extra_type == "legbye":
                legbye_runs = np.random.choice([1,2,4], p=[0.7,0.2,0.1])
            else:
                is_wicket = np.random.random() < 0.045
                if is_wicket and wickets < 9:
                    wickets += 1
                    player_dismissed = striker
                    dismissal_kind = np.random.choice(
                        ["caught","bowled","lbw","run out","stumped","caught and bowled"],
                        p=[0.45,0.2,0.12,0.13,0.05,0.05]
                    )
                    if dismissal_kind in ("caught","run out","stumped","caught and bowled"):
                        fielder = random.choice(bowlers)
                    batsman_runs = 0
                else:
                    batsman_runs = np.random.choice(
                        [0,1,2,3,4,6], p=[0.38,0.32,0.08,0.02,0.14,0.06]
                    )

            extra_runs = wide_runs + noball_runs + bye_runs + legbye_runs
            total_runs = batsman_runs + extra_runs
            total += total_runs

            rows.append({
                "match_id": match_id, "inning": inning_no,
                "batting_team": batting_team, "bowling_team": bowling_team,
                "over": over, "ball": ball,
                "batsman": striker, "non_striker": non_striker, "bowler": bowler,
                "is_super_over": 0,
                "wide_runs": wide_runs, "bye_runs": bye_runs, "legbye_runs": legbye_runs,
                "noball_runs": noball_runs, "penalty_runs": 0,
                "batsman_runs": batsman_runs, "extra_runs": extra_runs, "total_runs": total_runs,
                "player_dismissed": player_dismissed, "dismissal_kind": dismissal_kind,
                "fielder": fielder
            })

            if player_dismissed:
                next_batsman_pos = max(striker_idx, non_striker_idx) + 1
                if next_batsman_pos < len(batsmen):
                    striker_idx = next_batsman_pos
            elif extra_type != "wide" and batsman_runs % 2 == 1:
                striker_idx, non_striker_idx = non_striker_idx, striker_idx

        if wickets >= 10 or (target is not None and total >= target):
            break
    return rows, total, wickets

def generate(num_seasons=5, matches_per_season=14, out_dir="dataset"):
    match_rows = []
    delivery_rows = []
    match_id = 1
    start_year = 2020

    for s in range(num_seasons):
        season = start_year + s
        season_start = date(season, 3, 25)
        team_pool = TEAMS[:]
        for m in range(matches_per_season):
            t1, t2 = random.sample(team_pool, 2)
            venue = random.choice(VENUES)
            city = CITIES[venue]
            match_date = season_start + timedelta(days=m * 2)
            toss_winner = random.choice([t1, t2])
            toss_decision = random.choice(["bat", "field"])

            bat_first = toss_winner if toss_decision == "bat" else (t2 if toss_winner == t1 else t1)
            bowl_first = t2 if bat_first == t1 else t1

            rows1, total1, wkts1 = simulate_innings(match_id, 1, bat_first, bowl_first)
            rows2, total2, wkts2 = simulate_innings(match_id, 2, bowl_first, bat_first, target=total1 + 1)

            delivery_rows.extend(rows1)
            delivery_rows.extend(rows2)

            if total2 > total1:
                winner = bowl_first
                win_by_runs = 0
                win_by_wickets = 10 - wkts2
            elif total1 > total2:
                winner = bat_first
                win_by_runs = total1 - total2
                win_by_wickets = 0
            else:
                winner = "Tie"
                win_by_runs = 0
                win_by_wickets = 0

            all_players = SQUADS[t1] + SQUADS[t2]
            player_of_match = random.choice(all_players)

            match_rows.append({
                "id": match_id, "season": season, "city": city,
                "date": match_date.isoformat(), "team1": t1, "team2": t2,
                "toss_winner": toss_winner, "toss_decision": toss_decision,
                "result": "normal" if winner != "Tie" else "tie",
                "dl_applied": 0,
                "winner": winner, "win_by_runs": win_by_runs, "win_by_wickets": win_by_wickets,
                "player_of_match": player_of_match, "venue": venue,
                "umpire1": "Umpire " + str(random.randint(1, 12)),
                "umpire2": "Umpire " + str(random.randint(1, 12)),
            })
            match_id += 1

    matches_df = pd.DataFrame(match_rows)
    deliveries_df = pd.DataFrame(delivery_rows)

    # sprinkle a few realistic messy issues for the cleaning script to fix
    matches_df.loc[matches_df.sample(frac=0.03, random_state=1).index, "city"] = None
    matches_df["team1"] = matches_df["team1"].replace(
        {"Royal Challengers Bengaluru": "Royal Challengers Bangalore"}, regex=False
    ) if False else matches_df["team1"]  # placeholder to keep structure obvious/simple

    import os
    os.makedirs(out_dir, exist_ok=True)
    matches_df.to_csv(f"{out_dir}/matches.csv", index=False)
    deliveries_df.to_csv(f"{out_dir}/deliveries.csv", index=False)
    print(f"Generated {len(matches_df)} matches and {len(deliveries_df)} deliveries.")
    print(f"Saved to {out_dir}/matches.csv and {out_dir}/deliveries.csv")

if __name__ == "__main__":
    generate()
