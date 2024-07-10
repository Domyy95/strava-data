import streamlit as st
from src.api.strava import StravaAPI

front_end_dir = "./frontend"


def page2():
    st.title("Second page")


def home(strava_api: StravaAPI = None):
    map_page = st.Page(f"{front_end_dir}/map.py", title="Map", icon=":material/map:")
    test_page = st.Page(page2, title="test")

    pg = st.navigation([map_page, test_page])
    pg.run()
