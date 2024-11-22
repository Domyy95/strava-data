import streamlit as st
from src.frontend.utils.graphs import get_weeks, get_data_run
import plotly.graph_objs as go


def display_charts():
    _, time_week_x = get_weeks(4)
    _, km, min, gain = get_data_run(time_week_x)
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


st.title("📊 Personal Running Charts")
display_charts()
