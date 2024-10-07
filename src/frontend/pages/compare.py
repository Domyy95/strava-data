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


def clean_activity_laps(laps, name) -> pd.DataFrame:
    result = pd.DataFrame([lap.dict() for lap in laps])
    result[f"Time {name}"] = result["elapsed_time"].apply(convert_seconds_to_minutes).fillna("0:00")
    result[f"time_{name}"] = result["elapsed_time"].fillna(0)
    result[f"Avg Heartrate {name}"] = result["average_heartrate"].fillna(0)
    return result[[f"Time {name}", f"time_{name}", f"Avg Heartrate {name}"]]


def convert_time_to_minutes(time_str):
    """Converts a time string in the format 'MM:SS' or 'HH:MM:SS' to total minutes."""
    if time_str == 0:
        time_str = "0:00"

    time_parts = list(map(int, time_str.split(":")))

    if len(time_parts) == 2:
        minutes, seconds = time_parts
        return minutes + seconds / 60
    elif len(time_parts) == 3:
        hours, minutes, seconds = time_parts
        return hours * 60 + minutes + seconds / 60
    else:
        raise ValueError(f"Unexpected time format: {time_str}")


def highlight_best_rows(row):
    styles = ["" for _ in row]

    col_index_1 = 1  # Second column (Elapsed Time 1)
    col_index_2 = 2  # Third column (Elapsed Time 2)
    value1 = row[col_index_1]
    value2 = row[col_index_2]

    if value1 != 0 and value2 != 0:
        time1_in_minutes = convert_time_to_minutes(value1)
        time2_in_minutes = convert_time_to_minutes(value2)

        if time1_in_minutes == min(time1_in_minutes, time2_in_minutes):
            styles[col_index_1] = "background-color: green"
        if time2_in_minutes == min(time1_in_minutes, time2_in_minutes):
            styles[col_index_2] = "background-color: green"

    # check if there are columns for heartrate
    if len(row) > 4:
        col_index_1 = 4
        col_index_2 = 5
        value1 = row[col_index_1]
        value2 = row[col_index_2]

        if value1 != 0 and value2 != 0:
            if value1 == min(value1, value2):
                styles[col_index_1] = "background-color: red"
            if value2 == min(value1, value2):
                styles[col_index_2] = "background-color: red"

    return styles


def build_compare_data(link1: str, link2: str):
    activity_id = int(link1.split("/")[-1])
    activity1 = st.session_state["strava_api"].get_activity(activity_id=activity_id)
    activity_id = int(link2.split("/")[-1])
    activity2 = st.session_state["strava_api"].get_activity(activity_id=activity_id)
    name1 = activity1.name + " " + activity1.start_date.split("-")[0]
    name2 = activity2.name + " " + activity2.start_date.split("-")[0]
    if name1 == name2:
        name1 += " 1"
        name2 += " 2"
    activity1_laps = clean_activity_laps(activity1.laps, name1)
    activity2_laps = clean_activity_laps(activity2.laps, name2)
    activities = pd.concat([activity1_laps, activity2_laps], axis=1)
    activities = activities.fillna(0)
    activities["Difference"] = activities[f"time_{name1}"] - activities[f"time_{name2}"]
    activities["Difference"] = activities["Difference"].apply(convert_seconds_to_minutes)
    activities["Difference Hearthrate"] = (
        activities[f"Avg Heartrate {name1}"] - activities[f"Avg Heartrate {name2}"]
    )
    activities.drop(columns=[f"time_{name1}", f"time_{name2}"], inplace=True)
    activities = activities[
        [
            f"Time {name1}",
            f"Time {name2}",
            "Difference",
            # f"Avg Heartrate {name1}",
            # f"Avg Heartrate {name2}",
            # "Difference Hearthrate",
        ]
    ]
    activities.insert(0, "Km", range(1, len(activities) + 1))
    st.dataframe(activities.style.apply(highlight_best_rows, axis=1), hide_index=True)


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
            build_compare_data(link1, link2)

    else:
        if not link1_valid:
            st.write("Link 1 is not a valid Strava activity link.")
        if not link2_valid:
            st.write("Link 2 is not a valid Strava activity link.")
