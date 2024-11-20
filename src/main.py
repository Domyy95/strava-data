import streamlit as st
from src.api.strava import StravaAPI
from src.settings import get_settings
from src.frontend.home import home


@st.cache_data
def load_settings():
    return get_settings()


@st.cache_data
def load_strava_api(access_token, client_id, client_secret):
    return StravaAPI(access_token, client_id, client_secret)


def run():
    settings = load_settings()
    if "strava_api" not in st.session_state:
        st.session_state["strava_api"] = load_strava_api(
            settings.access_token, settings.client_id, settings.client_secret
        )

    home()


if __name__ == "__main__":
    run()
