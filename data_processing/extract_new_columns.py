import pandas as pd

# Load dataset
df = pd.read_csv("cricket_data.csv")

df.rename(columns={"start_date": "match_date"}, inplace=True)
# Ensure match_date is in datetime format
df["match_date"] = pd.to_datetime(df["match_date"])

# Group by match date and get opponent teams
team_groups = df.groupby("match_date")["team"].unique()

# Rebuild opponent dictionary
opponent_dict = {}
for teams in team_groups:
    if len(teams) == 2:  # Ensure exactly 2 teams in a match
        opponent_dict[teams[0]] = teams[1]
        opponent_dict[teams[1]] = teams[0]

# Assign opponent team
df["opponent_team"] = df["team"].map(opponent_dict)

# Compute average opponent performance in last 5 matches
opponent_performance = df.groupby("opponent_team").agg(
    avg_opponent_runs=("total_runs", "mean"),
    avg_opponent_wickets=("total_wickets", "mean")
).reset_index()

# Merge back
df = df.merge(opponent_performance, on="opponent_team", how="left")

# Fill missing values
df["opponent_team"].fillna("Unknown", inplace=True)
df["avg_opponent_runs"].fillna(0, inplace=True)
df["avg_opponent_wickets"].fillna(0, inplace=True)

# Save cleaned dataset
df.to_csv("cleaned_cricket_performance.csv", index=False)

# Display preview
print(df[["player", "team", "opponent_team", "avg_opponent_runs", "avg_opponent_wickets"]].head())
print("\n✅ Data Processing Complete! Missing values handled successfully.")
