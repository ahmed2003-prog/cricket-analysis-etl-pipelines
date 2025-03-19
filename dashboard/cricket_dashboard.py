import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy.engine import create_engine

athena_engine = create_engine(
    "awsathena+rest://:@athena.eu-north-1.amazonaws.com:443/cricket-db",
    connect_args={"s3_staging_dir": "s3://cricket-athena-results/"}
)

query = """
    SELECT player, team, SUM(total_runs) AS total_runs, 
           AVG(batting_avg) AS batting_avg, AVG(batting_sr) AS batting_sr,
           SUM(total_wickets) AS total_wickets, AVG(bowling_avg) AS bowling_avg,
           AVG(bowling_economy) AS bowling_economy, SUM(catches) AS catches, 
           SUM(stumpings) AS stumpings 
    FROM cricket_performance_partitioned
    GROUP BY player, team;
"""

try:
    df = pd.read_sql(query, athena_engine)
except Exception as e:
    st.error(f"Error: {e}")
    df = pd.DataFrame()

st.title("🏏 Cricket Performance Dashboard")
st.write("Analyze top cricket performers with interactive insights.")

if not df.empty:
    team_list = df["team"].unique().tolist()
    selected_team = st.selectbox("Select a Team:", ["All"] + team_list)
    if selected_team != "All":
        df = df[df["team"] == selected_team]

if not df.empty:
    st.subheader("🏆 Top Performers Leaderboard")
    col1, col2 = st.columns(2)
    with col1:
        st.write("🏏 **Top Batters**")
        top_batsmen = df.sort_values(by="total_runs", ascending=False).head(10)
        st.dataframe(top_batsmen[["player", "team", "total_runs", "batting_avg"]])
    with col2:
        st.write("🎯 **Top Bowlers**")
        top_bowlers = df.sort_values(by="total_wickets", ascending=False).head(10)
        st.dataframe(top_bowlers[["player", "team", "total_wickets", "bowling_avg"]])

if not df.empty:
    st.subheader("⚔️ Player Comparison Tool")
    players = df["player"].unique().tolist()
    player1 = st.selectbox("Select Player 1:", players)
    player2 = st.selectbox("Select Player 2:", players)
    player1_stats = df[df["player"] == player1].iloc[0]
    player2_stats = df[df["player"] == player2].iloc[0]
    comparison_data = {
        "Metric": ["Total Runs", "Batting Avg", "Strike Rate", "Total Wickets", "Economy Rate"],
        player1: [player1_stats["total_runs"], player1_stats["batting_avg"], player1_stats["batting_sr"], player1_stats["total_wickets"], player1_stats["bowling_economy"]],
        player2: [player2_stats["total_runs"], player2_stats["batting_avg"], player2_stats["batting_sr"], player2_stats["total_wickets"], player2_stats["bowling_economy"]]
    }
    st.table(pd.DataFrame(comparison_data))

if not df.empty:
    st.subheader("📊 Batting Performance")
    fig1 = px.scatter(df, x="batting_sr", y="total_runs", size="batting_avg", color="player", hover_name="player", title="Strike Rate vs Total Runs")
    st.plotly_chart(fig1)

    st.subheader("🎯 Bowling Performance")
    fig2 = px.scatter(df, x="bowling_economy", y="total_wickets", size="bowling_avg", color="player", hover_name="player", title="Economy Rate vs Total Wickets")
    st.plotly_chart(fig2)

    st.subheader("🔄 Dismissals - Catches & Stumpings")
    fig3 = px.bar(df, x="player", y=["catches", "stumpings"], barmode="group", title="Dismissals by Player")
    st.plotly_chart(fig3)

    # Additional Insights
    st.subheader("🔥 Most Consistent Batters (Avg > 40)")
    consistent_batsmen = df[df["batting_avg"] > 40].sort_values("batting_avg", ascending=False)
    st.dataframe(consistent_batsmen[["player", "team", "batting_avg", "total_runs"]])

    st.subheader("⚡ Best Finishers (Strike Rate > 130)")
    best_finishers = df[df["batting_sr"] > 130].sort_values("batting_sr", ascending=False)
    st.dataframe(best_finishers[["player", "team", "batting_sr", "total_runs"]])

    st.subheader("🎳 Top Wicket-Takers with Low Economy (< 6)")
    top_bowlers_low_economy = df[(df["bowling_economy"] < 6) & (df["total_wickets"] > 50)]
    st.dataframe(top_bowlers_low_economy[["player", "team", "total_wickets", "bowling_economy"]])

if not df.empty:
    st.subheader("📥 Download Data")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "cricket_performance.csv", "text/csv")