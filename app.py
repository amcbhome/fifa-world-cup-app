import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="FIFA World Cup Stats Visualizer",
    page_icon="⚽",
    layout="wide",
)


# 2. Load and Cache Data
@st.cache_data
def load_data():
  """Generates or loads the FIFA World Cup dataset."""
  data = {
      "Year": [
          1998,
          1998,
          2002,
          2002,
          2006,
          2006,
          2010,
          2010,
          2014,
          2014,
          2018,
          2018,
          2022,
          2022,
      ],
      "Tournament": [
          "France 1998",
          "France 1998",
          "Korea/Japan 2002",
          "Korea/Japan 2002",
          "Germany 2006",
          "Germany 2006",
          "South Africa 2010",
          "South Africa 2010",
          "Brazil 2014",
          "Brazil 2014",
          "Russia 2018",
          "Russia 2018",
          "Qatar 2022",
          "Qatar 2022",
      ],
      "Team": [
          "France",
          "Brazil",
          "Brazil",
          "Germany",
          "Italy",
          "France",
          "Spain",
          "Netherlands",
          "Germany",
          "Argentina",
          "France",
          "Croatia",
          "Argentina",
          "France",
      ],
      "Stage": [
          "Final",
          "Final",
          "Final",
          "Final",
          "Final",
          "Final",
          "Final",
          "Final",
          "Final",
          "Final",
          "Final",
          "Final",
          "Final",
          "Final",
      ],
      "GoalsScored": [3, 0, 2, 0, 1, 1, 1, 0, 1, 0, 4, 2, 3, 3],
      "MatchesPlayed": [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
      "YellowCards": [12, 11, 8, 14, 10, 15, 8, 22, 10, 11, 12, 15, 20, 16],
      "PossessionAvg": [
          52.0,
          58.0,
          54.0,
          46.0,
          48.0,
          53.0,
          58.0,
          47.0,
          52.0,
          48.0,
          48.0,
          54.0,
          47.0,
          46.0,
      ],
  }
  return pd.DataFrame(data)


df = load_data()

# 3. App Header
st.title("⚽ FIFA World Cup Data Explorer")
st.markdown(
    "Explore historical team statistics, goals scored, disciplinary records,"
    " and performance metrics across different FIFA World Cup tournaments."
)

# 4. Sidebar Filters
st.sidebar.header("Filter Options")

tournaments = sorted(df["Tournament"].unique())
selected_tournaments = st.sidebar.multiselect(
    "Select Tournaments", options=tournaments, default=tournaments
)

teams = sorted(df["Team"].unique())
selected_teams = st.sidebar.multiselect(
    "Select Teams", options=teams, default=teams[:5]
)

filtered_df = df[
    df["Tournament"].isin(selected_tournaments) & df["Team"].isin(selected_teams)
]

# 5. Main Content: Metrics / KPIs
st.subheader("📊 Tournament Overview")

if filtered_df.empty:
  st.warning(
      "No data available for the selected filters. Please select more options"
      " in the sidebar."
  )
else:
  total_goals = int(filtered_df["GoalsScored"].sum())
  total_yellow_cards = int(filtered_df["YellowCards"].sum())
  avg_possession = round(filtered_df["PossessionAvg"].mean(), 2)

  col1, col2, col3 = st.columns(3)
  col1.metric(label="Total Goals Scored", value=total_goals)
  col2.metric(label="Total Yellow Cards", value=total_yellow_cards)
  col3.metric(label="Average Possession (%)", value=f"{avg_possession}%")

  st.divider()

  # 6. Visualizations
  col_chart1, col_chart2 = st.columns(2)

  with col_chart1:
    st.markdown("### Goals Scored by Team")
    fig_goals = px.bar(
        filtered_df,
        x="Team",
        y="GoalsScored",
        color="Tournament",
        barmode="group",
        title="Goals Scored Comparison",
    )
    st.plotly_chart(fig_goals, use_container_width=True)

  with col_chart2:
    st.markdown("### Possession vs. Goals")
    fig_scatter = px.scatter(
        filtered_df,
        x="PossessionAvg",
        y="GoalsScored",
        color="Team",
        size="YellowCards",
        hover_name="Tournament",
        title="Average Possession vs Goals Scored",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

  # 7. Raw Data Table
  with st.expander("🔍 View Raw Dataset"):
    st.dataframe(filtered_df, use_container_width=True)
