import streamlit as st
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import folium

def map_select():
    # Lecco
    DEFAULT_LATITUDE = 45.85
    DEFAULT_LONGITUDE = 9.39

    latitude = None
    longitude = None

    location = get_geolocation()
    if location and not latitude and not longitude:
        latitude = location["coords"]["latitude"]
        longitude = location["coords"]["longitude"]
    else:
        latitude = DEFAULT_LATITUDE
        longitude = DEFAULT_LONGITUDE

    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    m.add_child(folium.LatLngPopup())

    f_map = st_folium(m, width=725)

    selected_latitude = latitude
    selected_longitude = longitude

    if f_map.get("last_clicked"):
        selected_latitude = f_map["last_clicked"]["lat"]
        selected_longitude = f_map["last_clicked"]["lng"]


    form = st.form("Position entry form")
    submit = form.form_submit_button()

    if submit:
        st.success(f"Stored position: {selected_latitude}, {selected_longitude}")
        print(selected_latitude, selected_longitude)
                                    