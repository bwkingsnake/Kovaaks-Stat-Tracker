import fileUtilities as futils
import pandas as pd
import plotly.graph_objects as go


#define paths
outPutPath = ("Output")
files = futils.getFilesInDirectory(outPutPath)

#get data frame
for file in files:
    df = pd.read_csv(outPutPath + "/" + file)

#sort by time and date
newData =  df.copy()
newData["DateAndTime"] = pd.to_datetime(newData["DateAndTime"], format="%Y.%m.%d-%H.%M")
sortedData = newData.sort_values(by='DateAndTime')   

#init vars
scenario_name = df["Scenario"].iloc[0]

averageScore = round(df['Score'].mean(),2)
highestScore = round(df['Score'].max(),2)

averageAccuracy = round(df['Accuracy'].mean(),2)
highestAccuracy = round(df['Accuracy'].max(),2)

#display data

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=sortedData.index,
    y=sortedData["Score"],
    mode="lines+markers",
    name="Score Increase Over Time",
    line=dict(shape="spline", color="red", width=3),
    marker=dict(size=7),
    hoverinfo="y",
    visible=True  
))

fig.update_layout(
    title=(
        f"{scenario_name} | "
        f"Average Score: {averageScore} • Highest Score: {highestScore} | "
        f"Avg Accuracy: {averageAccuracy}% • Highest Accuracy: {highestAccuracy}%"
    ),
    xaxis_title="Time",
    yaxis_title="Score",
    xaxis_tickangle=45,
    template="plotly_white",
    legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.5)"),
)


fig.show()

