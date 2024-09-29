import pandas as pd
import streamlit as st

from src.frontend.utils import convert_seconds_to_minutes


def validate_strava_activity_link(link):
    if (
        link.startswith("https://www.strava.com/activities/")
        and link[len("https://www.strava.com/activities/") :].isdigit()
    ):
        return True
    return False


def fetch_activity_laps(url, name) -> pd.DataFrame:
    activity_id = int(url.split("/")[-1])
    laps = st.session_state["strava_api"].get_activity_laps(activity_id=activity_id)
    result = pd.DataFrame([lap.dict() for lap in laps])
    result[f"Elapsed Time {name}"] = result["elapsed_time"].apply(convert_seconds_to_minutes)
    result[f"elapsed_time_{name}"] = result["elapsed_time"]
    return result[[f"Elapsed Time {name}", f"elapsed_time_{name}"]]


def highlight_best_row(row):
    styles = ["" for _ in row]

    col_index_1 = 1  # Second column (Elapsed Time 1)
    col_index_2 = 2  # Third column (Elapsed Time 2)
    value1 = row[col_index_1]
    value2 = row[col_index_2]

    if value1 == min(value1, value2):
        styles[col_index_1] = "background-color: green"
    if value2 == min(value1, value2):
        styles[col_index_2] = "background-color: green"

    return styles


st.title("⏱️ Compare Runs")

col1, col2 = st.columns(2)

with col1:
    link1 = st.text_input("Activity Link 1")

with col2:
    link2 = st.text_input("Activity Link 2")

if link1 and link2:
    link1_valid = validate_strava_activity_link(link1)
    link2_valid = validate_strava_activity_link(link2)

    if link1_valid and link2_valid:
        if st.button("Compute"):
            activity1_df = fetch_activity_laps(link1, 1)
            activity2_df = fetch_activity_laps(link2, 2)
            activities = pd.concat([activity1_df, activity2_df], axis=1)
            activities["Difference"] = activities["elapsed_time_1"] - activities["elapsed_time_2"]
            activities["Difference"] = activities["Difference"].apply(convert_seconds_to_minutes)
            activities.drop(columns=["elapsed_time_1", "elapsed_time_2"], inplace=True)
            activities.insert(0, "Km", range(1, len(activities) + 1))
            st.dataframe(activities.style.apply(highlight_best_row, axis=1), hide_index=True)

    else:
        if not link1_valid:
            st.write("Link 1 is not a valid Strava activity link.")
        if not link2_valid:
            st.write("Link 2 is not a valid Strava activity link.")
