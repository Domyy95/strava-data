import streamlit as st
import settings
from src.api.strava import StravaAPI
from src.frontend.utils import get_weeks, get_data_run
import plotly.graph_objs as go


st.title("🔑 Personal Running Charts")
secret_token = settings.Settings()


def display_charts(access_token: str):
    st.write("charts")
    StravaAPI.autorization(secret_token.client_id, secret_token.client_secret, access_token)
    date_time, time_week_x = get_weeks(4)
    data_run, km, min, gain = get_data_run(time_week_x, access_token)
    fig_distance = go.Figure()
    fig_hr = go.Figure()
    fig_gain = go.Figure()

    fig_distance.add_trace(go.Scatter(x=time_week_x, y=km))
    fig_gain.add_trace(go.Scatter(x=time_week_x, y=gain))
    fig_hr.add_trace(go.Scatter(x=time_week_x, y=min))

    st.write("")
    st.write("")
    st.write("Distance Chart")
    st.plotly_chart(fig_distance)

    st.write("")
    st.write("")
    st.write("Elevation Gain Chart")
    st.plotly_chart(fig_gain)

    st.write("")
    st.write("")
    st.write("Hour Chart")
    st.plotly_chart(fig_hr)


def display_first_part(client_id: str):
    st.subheader("Ottieni Codice Accesso")
    st.write("Accedi con strava per visualizzare i grafici 🔑")
    link = f"http://www.strava.com/oauth/authorize?client_id={client_id}<&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all"
    st.link_button("Login With Strava", link)

    access_token = st.text_input("Incolla il Codice", "")
    if st.button("Ottieni Dati", use_container_width=True):
        with st.spinner("waiting"):
            display_charts(access_token)


display_first_part(settings.Settings().client_id)
