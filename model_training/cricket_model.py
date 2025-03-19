import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, accuracy_score
from sklearn.model_selection import RandomizedSearchCV

# Load dataset
df = pd.read_csv("cleaned_cricket_performance.csv")

# Ensure match_date is in datetime format
df["match_date"] = pd.to_datetime(df["match_date"])

# ✅ Fantasy Player Ranking
df["fantasy_score"] = (
    df["total_runs"] * 1.2 +
    df["total_wickets"] * 25 +
    df["batting_avg"] * 5 +
    df["bowling_avg"] * -3 +
    df["avg_opponent_runs"] * -0.5 +
    df["avg_opponent_wickets"] * 0.5
)

fantasy_players = df.groupby("player")["fantasy_score"].sum().reset_index()
fantasy_players = fantasy_players.sort_values(by="fantasy_score", ascending=False)

# Save fantasy scores
fantasy_players.to_csv("fantasy_scores.csv", index=False)

# ✅ Runs & Wickets Prediction
features = ["batting_innings", "bowling_innings", "avg_opponent_runs", "avg_opponent_wickets"]
X_runs = df[features]
y_runs = df["total_runs"]
X_wickets = df[features]
y_wickets = df["total_wickets"]

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_runs, y_runs, test_size=0.2, random_state=42)
X_train_w, X_test_w, y_train_w, y_test_w = train_test_split(X_wickets, y_wickets, test_size=0.2, random_state=42)

# Hyperparameter tuning
rf_params = {
    "n_estimators": [50, 100, 200],
    "max_depth": [10, 20, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4]
}

rf_model_r = RandomizedSearchCV(RandomForestRegressor(random_state=42), rf_params, n_iter=10, cv=3, n_jobs=-1)
rf_model_w = RandomizedSearchCV(RandomForestRegressor(random_state=42), rf_params, n_iter=10, cv=3, n_jobs=-1)

rf_model_r.fit(X_train_r, y_train_r)
rf_model_w.fit(X_train_w, y_train_w)

# Store MAE
runs_mae = mean_absolute_error(y_test_r, rf_model_r.best_estimator_.predict(X_test_r))
wickets_mae = mean_absolute_error(y_test_w, rf_model_w.best_estimator_.predict(X_test_w))

# ✅ Match Outcome Prediction
df["win"] = np.where(df["batting_avg"] > df["avg_opponent_runs"], 1, 0)
X_outcome = df[["batting_avg", "bowling_avg", "avg_opponent_runs", "avg_opponent_wickets"]]
y_outcome = df["win"]

X_train_o, X_test_o, y_train_o, y_test_o = train_test_split(X_outcome, y_outcome, test_size=0.2, random_state=42)
rf_model_o = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model_o.fit(X_train_o, y_train_o)

# Store Accuracy
outcome_accuracy = accuracy_score(y_test_o, rf_model_o.predict(X_test_o))

# ✅ Save models
joblib.dump(rf_model_r.best_estimator_, "runs_prediction_model.pkl")
joblib.dump(rf_model_w.best_estimator_, "wickets_prediction_model.pkl")
joblib.dump(rf_model_o, "match_outcome_model.pkl")

print(f"🏏 Runs Prediction MAE: {runs_mae}")
print(f"🎯 Wickets Prediction MAE: {wickets_mae}")
print(f"⚡ Match Outcome Accuracy: {outcome_accuracy}")
print("✅ Models & Fantasy Scores saved successfully!")
