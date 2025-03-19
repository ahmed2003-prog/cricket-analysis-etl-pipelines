from fastapi import FastAPI, Query
import joblib
import pandas as pd

app = FastAPI()

# ✅ Load trained models
runs_model = joblib.load("runs_prediction_model.pkl")
wickets_model = joblib.load("wickets_prediction_model.pkl")
outcome_model = joblib.load("match_outcome_model.pkl")

# ✅ Load datasets
batting_df = pd.read_csv("batting_data.csv")
bowling_df = pd.read_csv("bowling_data.csv")
fantasy_scores_df = pd.read_csv("fantasy_scores.csv")

@app.get("/")
def home():
    return {"message": "🏏 Cricket Performance API is live!"}

# ✅ **Predict Match Outcome Based on Teams**
@app.post("/predict_match_outcome/")
def predict_match_outcome(team_1: str, team_2: str):
    # Filter team statistics
    team_1_stats = batting_df[batting_df["team"].str.lower() == team_1.lower()]
    team_2_stats = batting_df[batting_df["team"].str.lower() == team_2.lower()]

    if team_1_stats.empty or team_2_stats.empty:
        return {"error": "One or both teams not found in dataset"}

    # Compute averages
    team_1_avg_runs = team_1_stats["runs"].mean()
    team_2_avg_runs = team_2_stats["runs"].mean()
    team_1_avg_wickets = bowling_df[bowling_df["team"].str.lower() == team_1.lower()]["wickets"].mean()
    team_2_avg_wickets = bowling_df[bowling_df["team"].str.lower() == team_2.lower()]["wickets"].mean()

    # Prepare features for prediction
    features = [[team_1_avg_runs, team_1_avg_wickets, team_2_avg_runs, team_2_avg_wickets]]
    outcome = outcome_model.predict(features)[0]

    return {
        "team_1": team_1,
        "team_2": team_2,
        "predicted_winner": team_1 if outcome == 1 else team_2
    }

# ✅ **Predict Runs for a Team**
@app.post("/predict_team_runs/")
def predict_team_runs(team: str):
    team_stats = batting_df[batting_df["team"].str.lower() == team.lower()]
    if team_stats.empty:
        return {"error": "Team not found"}

    avg_runs = team_stats["runs"].mean()
    features = [[avg_runs, team_stats["innings"].mean(), team_stats["opponent_runs"].mean(), team_stats["opponent_wickets"].mean()]]
    predicted_runs = runs_model.predict(features)[0]

    return {"team": team, "predicted_runs": predicted_runs}

# ✅ **Predict Top Fantasy Players for a Match**
@app.get("/top_fantasy_players/")
def get_top_fantasy_players(match: str, top_n: int = 10):
    match_players = fantasy_scores_df[fantasy_scores_df["match"] == match]
    if match_players.empty:
        return {"error": "Match not found"}

    top_players = match_players.sort_values(by="fantasy_score", ascending=False).head(top_n).to_dict(orient="records")
    return {"match": match, "top_fantasy_players": top_players}
