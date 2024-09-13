import pandas as pd
import streamlit as st


def validate_strava_link(link):
    if (
        link.startswith("https://www.strava.com/activities/")
        and link[len("https://www.strava.com/activities/") :].isdigit()
    ):
        return True
    return False


def convert_seconds_to_minutes(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes}:{remaining_seconds:02d}"


def fetch_activity_laps(url) -> pd.DataFrame:
    activity_id = int(url.split("/")[-1])
    laps = st.session_state["strava_api"].get_activity_laps(activity_id=activity_id)
    result = pd.DataFrame([lap.dict() for lap in laps])
    result["time_per_km"] = result["elapsed_time"] / (result["distance"] / 1000)
    result = result[["distance", "elapsed_time", "time_per_km"]]
    result["elapsed_time"] = result["elapsed_time"].apply(convert_seconds_to_minutes)
    return result


st.title("⏱️ Compare Runs")

col1, col2 = st.columns(2)

with col1:
    link1 = st.text_input("Your Activity Link")

with col2:
    link2 = st.text_input("Other Activity Link")

if link1 and link2:
    link1_valid = validate_strava_link(link1)
    link2_valid = validate_strava_link(link2)

    if link1_valid and link2_valid:
        if st.button("Compute"):
            activity1_df = fetch_activity_laps(link1)
            # activity2_df = fetch_activity_laps(link2)
            st.table(activity1_df)

    else:
        if not link1_valid:
            st.write("Link 1 is not a valid Strava activity link.")
        if not link2_valid:
            st.write("Link 2 is not a valid Strava activity link.")
