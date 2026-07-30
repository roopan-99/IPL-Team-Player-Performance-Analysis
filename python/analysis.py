"""
analysis.py
-----------
Performs team & player performance analysis on the cleaned IPL data and
saves chart images to screenshots/ plus summary CSVs to dataset/ (handy
for building the Power BI dashboard on top of).

Run:
    python python/analysis.py
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

DATASET_DIR = "dataset"
SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

plt.rcParams["figure.figsize"] = (9, 5)
plt.rcParams["axes.titleweight"] = "bold"


def load_clean():
    matches = pd.read_csv(f"{DATASET_DIR}/matches_clean.csv", parse_dates=["date"])
    deliveries = pd.read_csv(f"{DATASET_DIR}/deliveries_clean.csv")
    # empty strings written to CSV come back as NaN on re-read; restore them
    # so text-based filters (e.g. player_dismissed != "") work correctly
    for col in ["player_dismissed", "dismissal_kind", "fielder"]:
        deliveries[col] = deliveries[col].fillna("")
    return matches, deliveries


def team_wins(matches: pd.DataFrame):
    wins = matches[matches["is_decisive"]]["winner"].value_counts()
    ax = wins.plot(kind="bar", color="#1f77b4")
    ax.set_title("Total Wins by Team")
    ax.set_ylabel("Wins")
    ax.set_xlabel("")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{SCREENSHOTS_DIR}/team_wins.png", dpi=150)
    plt.close()
    wins.to_csv(f"{DATASET_DIR}/summary_team_wins.csv", header=["wins"])
    return wins


def toss_impact(matches: pd.DataFrame):
    decisive = matches[matches["is_decisive"]].copy()
    decisive["toss_win_and_match_win"] = decisive["toss_winner"] == decisive["winner"]
    pct = decisive["toss_win_and_match_win"].mean() * 100

    decision_split = decisive["toss_decision"].value_counts()
    ax = decision_split.plot(kind="pie", autopct="%1.1f%%", ylabel="")
    ax.set_title(f"Toss Decision Split (Toss winner also won match: {pct:.1f}%)")
    plt.tight_layout()
    plt.savefig(f"{SCREENSHOTS_DIR}/toss_impact.png", dpi=150)
    plt.close()
    return pct, decision_split


def orange_cap(deliveries: pd.DataFrame, top_n=10):
    runs = deliveries.groupby("batsman")["batsman_runs"].sum().sort_values(ascending=False).head(top_n)
    ax = runs.plot(kind="barh", color="#ff7f0e")
    ax.invert_yaxis()
    ax.set_title(f"Top {top_n} Run Scorers (Orange Cap Race)")
    ax.set_xlabel("Runs")
    plt.tight_layout()
    plt.savefig(f"{SCREENSHOTS_DIR}/orange_cap_top10.png", dpi=150)
    plt.close()
    runs.to_csv(f"{DATASET_DIR}/summary_top_batsmen.csv", header=["runs"])
    return runs


def purple_cap(deliveries: pd.DataFrame, top_n=10):
    wickets_df = deliveries[
        (deliveries["player_dismissed"] != "") &
        (~deliveries["dismissal_kind"].isin(["run out"]))  # run outs aren't credited to bowler
    ]
    wkts = wickets_df.groupby("bowler").size().sort_values(ascending=False).head(top_n)
    ax = wkts.plot(kind="barh", color="#2ca02c")
    ax.invert_yaxis()
    ax.set_title(f"Top {top_n} Wicket Takers (Purple Cap Race)")
    ax.set_xlabel("Wickets")
    plt.tight_layout()
    plt.savefig(f"{SCREENSHOTS_DIR}/purple_cap_top10.png", dpi=150)
    plt.close()
    wkts.to_csv(f"{DATASET_DIR}/summary_top_bowlers.csv", header=["wickets"])
    return wkts


def venue_scoring(matches: pd.DataFrame, deliveries: pd.DataFrame, top_n=10):
    team_totals = deliveries.groupby(["match_id", "inning"])["total_runs"].sum().reset_index()
    match_venue = matches[["id", "venue"]].rename(columns={"id": "match_id"})
    merged = team_totals.merge(match_venue, on="match_id")
    avg_by_venue = merged.groupby("venue")["total_runs"].mean().sort_values(ascending=False).head(top_n)
    ax = avg_by_venue.plot(kind="barh", color="#9467bd")
    ax.invert_yaxis()
    ax.set_title("Average Innings Score by Venue")
    ax.set_xlabel("Avg runs per innings")
    plt.tight_layout()
    plt.savefig(f"{SCREENSHOTS_DIR}/venue_avg_scores.png", dpi=150)
    plt.close()
    return avg_by_venue


def season_run_trend(matches: pd.DataFrame, deliveries: pd.DataFrame):
    match_season = matches[["id", "season"]].rename(columns={"id": "match_id"})
    per_match_runs = deliveries.groupby("match_id")["total_runs"].sum().reset_index()
    merged = per_match_runs.merge(match_season, on="match_id")
    trend = merged.groupby("season")["total_runs"].mean()
    ax = trend.plot(kind="line", marker="o", color="#d62728")
    ax.set_title("Average Total Match Runs by Season")
    ax.set_ylabel("Avg runs per match")
    ax.set_xlabel("Season")
    plt.tight_layout()
    plt.savefig(f"{SCREENSHOTS_DIR}/season_run_trend.png", dpi=150)
    plt.close()
    return trend


def main():
    matches, deliveries = load_clean()

    wins = team_wins(matches)
    print("=== Team Wins ===")
    print(wins.to_string())

    pct, decision_split = toss_impact(matches)
    print(f"\n=== Toss Impact ===\nToss winner also won match: {pct:.1f}%")
    print(decision_split.to_string())

    top_bat = orange_cap(deliveries)
    print("\n=== Orange Cap (Top Run Scorers) ===")
    print(top_bat.to_string())

    top_bowl = purple_cap(deliveries)
    print("\n=== Purple Cap (Top Wicket Takers) ===")
    print(top_bowl.to_string())

    venues = venue_scoring(matches, deliveries)
    print("\n=== Avg Score by Venue ===")
    print(venues.to_string())

    trend = season_run_trend(matches, deliveries)
    print("\n=== Season Scoring Trend ===")
    print(trend.to_string())

    print(f"\nAll charts saved to {SCREENSHOTS_DIR}/")
    print(f"Summary CSVs (for Power BI) saved to {DATASET_DIR}/summary_*.csv")


if __name__ == "__main__":
    main()
