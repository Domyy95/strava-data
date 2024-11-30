import streamlit as st
from src.api.strava import StravaAPI
from src.settings import Settings
from src.frontend.pages.login import login_page
from src.frontend.home import home


@st.cache_data
def load_settings():
    return Settings()


@st.cache_data
def load_strava_api(access_token):
    return StravaAPI(access_token)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

settings = load_settings()
if not st.session_state.logged_in:
    login_page(settings)
else:
    if "strava_api" not in st.session_state:
        settings.get_access_token(st.session_state.auth_code)
        st.session_state["strava_api"] = load_strava_api(settings.access_token)
    home()
