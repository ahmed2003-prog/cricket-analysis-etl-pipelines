import pandas as pd
import numpy as np

# Load cricket dataset
df = pd.read_csv("cricket_data.csv")

df.rename(columns={"start_date": "match_date"}, inplace=True)
# Ensure date is in datetime format
df["match_date"] = pd.to_datetime(df["match_date"])

# Sort by player and match date for rolling calculations
df = df.sort_values(["player", "match_date"])

# 1️⃣ Player Form - Rolling Average of Last 5 Matches
df["rolling_runs"] = df.groupby("player")["total_runs"].rolling(window=5, min_periods=1).mean().reset_index(drop=True)
df["rolling_wickets"] = df.groupby("player")["total_wickets"].rolling(window=5, min_periods=1).mean().reset_index(drop=True)

# 2️⃣ Opponent Strength - Average opponent performance in last 5 matches
opponent_performance = df.groupby("opponent_team").agg(
    avg_opponent_runs=("total_runs", "mean"),
    avg_opponent_wickets=("total_wickets", "mean")
).reset_index()

df = df.merge(opponent_performance, on="opponent_team", how="left")

# Save processed data
df.to_csv("processed_cricket_performance.csv", index=False)

# Display preview
print(df.head())

print("\n✅ Data Processing Complete! Ready for Machine Learning.")
