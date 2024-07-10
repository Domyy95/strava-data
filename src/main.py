import streamlit as st
from src.api.strava import StravaAPI
from src.settings import get_settings
from src.frontend.home import home


@st.cache_data
def load_settings():
    return get_settings()


def run():
    settings = load_settings()
    if "strava_api" not in st.session_state:
        st.session_state["strava_api"] = StravaAPI(settings.access_token)

    home()


if __name__ == "__main__":
    run()
