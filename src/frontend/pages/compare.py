import pandas as pd
import streamlit as st
from src.frontend.utils import convert_seconds_to_hm


def validate_strava_activity_link(link):
    if (
        link.startswith("https://www.strava.com/activities/")
        and link[len("https://www.strava.com/activities/") :].isdigit()
    ):
        return True
    return False


def get_activities_data(link1, link2):
    activity_id = int(link1.split("/")[-1])
    activity1 = st.session_state["strava_api"].get_activity(activity_id=activity_id)
    activity_id = int(link2.split("/")[-1])
    activity2 = st.session_state["strava_api"].get_activity(activity_id=activity_id)
    if not activity1 or not activity2:
        if not activity1:
            # CRAWL IT
            st.write("Activity 1 not found.")
        if not activity2:
            # CRAWL IT
            st.write("Activity 2 not found.")

    return activity1, activity2


def clean_activity_laps(laps, name) -> pd.DataFrame:
    result = pd.DataFrame([lap.dict() for lap in laps])
    result[f"Time {name}"] = result["elapsed_time"].apply(convert_seconds_to_hm).fillna("0:00")
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


def build_compare_data(activity1: str, activity2: str):
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
    activities["Difference"] = activities["Difference"].apply(convert_seconds_to_hm)
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

    total_time_1 = convert_seconds_to_hm(activity1.elapsed_time)
    total_time_2 = convert_seconds_to_hm(activity2.elapsed_time)
    diff = convert_seconds_to_hm(activity1.elapsed_time - activity2.elapsed_time)

    final_row = pd.DataFrame(
        {
            "Km": ["Total"],
            f"Time {name1}": [total_time_1],
            f"Time {name2}": [total_time_2],
            "Difference": [diff],
        }
    )

    activities = pd.concat([activities, final_row], ignore_index=True)
    st.dataframe(activities.style.apply(highlight_best_rows, axis=1), hide_index=True)

    comparison = {
        "Name": [name1, name2],
        "Distance (km)": [activity1.distance / 1000, activity2.distance / 1000],
        "Moving Time (min)": [
            convert_seconds_to_hm(activity1.moving_time),
            convert_seconds_to_hm(activity2.moving_time),
        ],
        "Elapsed Time (min)": [
            convert_seconds_to_hm(activity1.elapsed_time),
            convert_seconds_to_hm(activity2.elapsed_time),
        ],
        "Average Speed (m/s)": [activity1.average_speed, activity2.average_speed],
        "Total Elevation Gain (m)": [
            activity1.total_elevation_gain,
            activity2.total_elevation_gain,
        ],
        "Average Cadence (spm)": [activity1.average_cadence, activity2.average_cadence],
        "Suffer Score": [activity1.suffer_score, activity2.suffer_score],
        "Calories Burned": [activity1.calories, activity2.calories],
    }

    df = pd.DataFrame(comparison, index=["Activity 1", "Activity 2"])
    st.dataframe(df)


def load_page():
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
                activity1, activity2 = get_activities_data(link1, link2)
                if activity1 and activity2:
                    build_compare_data(activity1, activity2)

        else:
            if not link1_valid:
                st.write("Link 1 is not a valid Strava activity link.")
            if not link2_valid:
                st.write("Link 2 is not a valid Strava activity link.")


st.title("⏱️ Compare Runs")

if "strava_api" not in st.session_state:
    st.warning("You Need To Login")
else:
    load_page()
