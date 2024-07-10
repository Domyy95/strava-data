from math import pi, cos
import streamlit as st
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import folium


def create_square(lat, lon, size_meters=1000):
    R = 6378000.0  # Earth radius in meters

    # Coordinate offsets in radians
    d_lat = size_meters / R
    d_lon = size_meters / (R * cos(pi * lat / 180))

    d_lat = d_lat * (180 / pi)
    d_lon = d_lon * (180 / pi)

    sw = [lat - d_lat, lon - d_lon]  # Southwest
    nw = [lat + d_lat, lon - d_lon]  # Northwest
    ne = [lat + d_lat, lon + d_lon]  # Northeast
    se = [lat - d_lat, lon + d_lon]  # Southeast

    return [sw, nw, ne, se, sw]


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

f_map = st_folium(m, width=725)

if f_map.get("last_clicked"):
    st.session_state.selected_latitude = f_map["last_clicked"]["lat"]
    st.session_state.selected_longitude = f_map["last_clicked"]["lng"]

    st.session_state.square_coords = create_square(
        st.session_state.selected_latitude, st.session_state.selected_longitude
    )

    # Clear the map and add updated elements
    m = folium.Map(location=[latitude, longitude], zoom_start=15)
    m.add_child(folium.LatLngPopup())
    folium.PolyLine(st.session_state.square_coords, color="blue", weight=2.5, opacity=1).add_to(m)

    # Display the updated map
    st_folium(m, width=725)


form = st.form("Position entry form")
submit = form.form_submit_button(label="Search segments inside the box")

if submit:
    st.success(
        f"Stored position: {st.session_state.selected_latitude}, {st.session_state.selected_longitude}"
    )
    print(st.session_state.selected_latitude, st.session_state.selected_longitude)

# segments = st.session_state['strava_api'].explore_segments(
#     bottom_left_point=[45.768661, 9.452020], top_right_point=[45.790124, 9.496888]
# )

# for segment in segments.segments:
#     detailed_segment = st.session_state['strava_api'].get_segment(segment.id)
#     print(detailed_segment.name, detailed_segment.distance, detailed_segment.average_grade)
