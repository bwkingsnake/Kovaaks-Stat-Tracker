import pandas as pd
import plotly.graph_objects as go

csv_path = "LastScenario/filepath.csv"

# Load and clean data
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()

# Parse datetime
df["DateAndTime"] = pd.to_datetime(df["DateAndTime"], format="%Y.%m.%d-%H.%M")
df["Date"] = df["DateAndTime"].dt.date

# Aggregate both mean and max Score per day
daily_agg = (
    df.groupby("Date")
    .agg(
        AvgScore=("Score", "mean"),
        MaxScore=("Score", "max"),
        Accuracy=("Accuracy", "mean")
    )
    .reset_index()
)

# Get scenario name and stats
scenario_name = df["Scenario"].iloc[0]

overall_avg_score = daily_agg["AvgScore"].mean()
overall_max_score = daily_agg["MaxScore"].max()
overall_avg_accuracy = daily_agg["Accuracy"].mean()
highest_accuracy = daily_agg["Accuracy"].max()

# Create figure
fig = go.Figure()

# Scatter plot for raw scores
fig.add_trace(go.Scatter(
    x=df["DateAndTime"],
    y=df["Score"],
    mode="markers",
    name="Raw Scores",
    marker=dict(color="lightskyblue", size=7, opacity=0.65),
    hoverinfo="x+y"
))

# Line for average scores per day
fig.add_trace(go.Scatter(
    x=daily_agg["Date"],
    y=daily_agg["AvgScore"],
    mode="lines+markers",
    name="Avg Score (Daily)",
    line=dict(shape="spline", color="green", width=3),
    marker=dict(size=7),
    hoverinfo="x+y",
    visible=True  # default visible
))

# Line for max scores per day
fig.add_trace(go.Scatter(
    x=daily_agg["Date"],
    y=daily_agg["MaxScore"],
    mode="lines+markers",
    name="High Score (Daily)",
    line=dict(shape="spline", color="blue", width=3),
    marker=dict(size=7),
    hoverinfo="x+y",
    visible=True  # default visible
))

# Layout setup
fig.update_layout(
    title=(
        f"{scenario_name} | "
        f"Avg of Daily Avgs: {overall_avg_score:.2f} • Highest Score: {overall_max_score:.2f} | "
        f"Avg Accuracy: {overall_avg_accuracy:.2f}% • Highest Accuracy: {highest_accuracy:.2f}%"
    ),
    xaxis_title="Date",
    yaxis_title="Score",
    xaxis_tickangle=45,
    template="plotly_white",
    legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.5)"),
)

fig.show()
