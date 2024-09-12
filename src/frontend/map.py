from typing import List
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from frontend.utils import create_square
from src.api.strava_model import ExplorerSegment


def fetch_segments(bottom_left, top_right) -> List[ExplorerSegment]:
    segments = st.session_state["strava_api"].explore_segments(
        bottom_left_point=bottom_left, top_right_point=top_right
    )
    return segments


# Default location Lecco
DEFAULT_LATITUDE = 45.85
DEFAULT_LONGITUDE = 9.39

# Get geolocation
location = get_geolocation()
latitude = location["coords"]["latitude"] if location else DEFAULT_LATITUDE
longitude = location["coords"]["longitude"] if location else DEFAULT_LONGITUDE

# State management for selected coordinates
if "selected_latitude" not in st.session_state:
    st.session_state.selected_latitude = latitude
if "selected_longitude" not in st.session_state:
    st.session_state.selected_longitude = longitude

# Initialize the map
m = folium.Map(location=[latitude, longitude], zoom_start=14)
m.add_child(folium.LatLngPopup())

# Add previously selected square if exists
if "square_coords" in st.session_state:
    folium.PolyLine(st.session_state.square_coords, color="blue", weight=2.5, opacity=1).add_to(m)

f_map = st_folium(m, width=725, height=500)

if f_map.get("last_clicked"):
    st.session_state.selected_latitude = f_map["last_clicked"]["lat"]
    st.session_state.selected_longitude = f_map["last_clicked"]["lng"]

    st.session_state.square_coords = create_square(
        st.session_state.selected_latitude, st.session_state.selected_longitude
    )

    # Clear the previous map instance and add updated elements
    m = folium.Map(location=[latitude, longitude], zoom_start=15)
    m.add_child(folium.LatLngPopup())
    folium.PolyLine(st.session_state.square_coords, color="blue", weight=2.5, opacity=1).add_to(m)

    # Display the updated map
    f_map = st_folium(m, width=725)


form = st.form("Position entry form")
submit = form.form_submit_button(label="Search segments inside the box")


if submit:
    if "square_coords" in st.session_state:
        bottom_left = st.session_state.square_coords[0]
        top_right = st.session_state.square_coords[2]

        segments = fetch_segments(bottom_left, top_right)

        table_data = []
        for segment in segments:
            detailed_segment = st.session_state["strava_api"].get_segment(segment.id)
            segment_url = f"https://www.strava.com/segments/{segment.id}"
            table_data.append(
                {
                    "Name": detailed_segment.name,
                    "Distance": detailed_segment.distance,
                    "Total Elevation Gain": detailed_segment.total_elevation_gain,
                    "Athlete Count": detailed_segment.athlete_count,
                    "kom": detailed_segment.xoms.kom,
                    "Elevation Profile": f"![Elevation Profile]( {detailed_segment.elevation_profile} )",
                    "Strava Segment Link": f"[↗️]({segment_url})",
                }
            )

        df = pd.DataFrame(table_data)
        st.write(df.to_markdown(), unsafe_allow_html=True)
    else:
        st.warning("Please select a square area on the map first.")
