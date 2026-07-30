"""
data_cleaning.py
-----------------
Cleans dataset/matches.csv and dataset/deliveries.csv and writes cleaned
versions to dataset/matches_clean.csv and dataset/deliveries_clean.csv.

Run:
    python python/data_cleaning.py
"""

import pandas as pd
import numpy as np
import os

DATASET_DIR = "dataset"

# Old franchise names -> current names (handles years where teams rebranded)
TEAM_NAME_MAP = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Rising Pune Supergiant": "Rising Pune Supergiants",
}


def load_data():
    matches = pd.read_csv(f"{DATASET_DIR}/matches.csv")
    deliveries = pd.read_csv(f"{DATASET_DIR}/deliveries.csv")
    return matches, deliveries


def clean_matches(matches: pd.DataFrame) -> pd.DataFrame:
    df = matches.copy()

    # Standardize team name spelling/rebrands across both team columns + winner/toss
    for col in ["team1", "team2", "toss_winner", "winner"]:
        df[col] = df[col].replace(TEAM_NAME_MAP)

    # Parse dates properly
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Fill missing city using the venue name (venue string usually contains the city)
    df["city"] = df.apply(
        lambda r: r["city"] if pd.notna(r["city"])
        else (r["venue"].split(",")[-1].strip() if pd.notna(r["venue"]) else "Unknown"),
        axis=1
    )

    # Drop exact duplicate match rows, if any
    df = df.drop_duplicates(subset=["id"])

    # Ensure numeric columns are numeric
    for col in ["win_by_runs", "win_by_wickets", "dl_applied"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # Flag ties / no-result matches so analysis can exclude them from "winner" stats
    df["is_decisive"] = ~df["winner"].isin(["Tie", "No Result", np.nan])

    df = df.sort_values("id").reset_index(drop=True)
    return df


def clean_deliveries(deliveries: pd.DataFrame, valid_match_ids) -> pd.DataFrame:
    df = deliveries.copy()

    # Keep only deliveries linked to a real match (referential integrity)
    df = df[df["match_id"].isin(valid_match_ids)]

    # Standardize team names here too
    for col in ["batting_team", "bowling_team"]:
        df[col] = df[col].replace(TEAM_NAME_MAP)

    # Fill numeric run columns with 0 where missing
    run_cols = ["wide_runs", "bye_runs", "legbye_runs", "noball_runs",
                "penalty_runs", "batsman_runs", "extra_runs", "total_runs"]
    for col in run_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # Text columns: keep genuine NaN (not empty string) so re-reading the CSV
    # doesn't silently turn "no dismissal" into an ambiguous value later.
    text_cols = ["player_dismissed", "dismissal_kind", "fielder"]
    for col in text_cols:
        df[col] = df[col].where(df[col].notna(), pd.NA)

    # Sanity check: total_runs should equal batsman_runs + extra_runs
    mismatch = df[df["total_runs"] != (df["batsman_runs"] + df["extra_runs"])]
    if len(mismatch) > 0:
        df.loc[mismatch.index, "total_runs"] = (
            mismatch["batsman_runs"] + mismatch["extra_runs"]
        )

    df = df.drop_duplicates(subset=["match_id", "inning", "over", "ball", "batsman", "bowler"])
    df = df.reset_index(drop=True)
    return df


def main():
    matches, deliveries = load_data()

    print(f"Raw matches: {len(matches)} rows | Raw deliveries: {len(deliveries)} rows")

    matches_clean = clean_matches(matches)
    deliveries_clean = clean_deliveries(deliveries, valid_match_ids=matches_clean["id"])

    print(f"Cleaned matches: {len(matches_clean)} rows | Cleaned deliveries: {len(deliveries_clean)} rows")
    print(f"Missing values in matches after cleaning:\n{matches_clean.isna().sum().sum()} total nulls")
    print(f"Missing values in deliveries after cleaning:\n{deliveries_clean.isna().sum().sum()} total nulls")

    matches_clean.to_csv(f"{DATASET_DIR}/matches_clean.csv", index=False)
    deliveries_clean.to_csv(f"{DATASET_DIR}/deliveries_clean.csv", index=False)
    print(f"\nSaved: {DATASET_DIR}/matches_clean.csv")
    print(f"Saved: {DATASET_DIR}/deliveries_clean.csv")


if __name__ == "__main__":
    main()
