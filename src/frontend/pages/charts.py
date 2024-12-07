import streamlit as st
from src.frontend.utils import get_data_run, make_charts_figure

st.title("📊 Personal Running Charts")

dict_date_times = {
    "Years": ("2", "3", "4", "5"),
    "Months": ("3", "6", "12", "18", "24", "30"),
    "Weeks": ("4", "8", "12", "16", "24", "30", "40"),
}
colors = ["blue", "red", "white"]
type_plot = ["scatter", "bar"]


def display_charts(code):
    topcol1, topcol2 = st.columns(2)

    with topcol1:
        block = st.selectbox("Grandezza Blocco Base", dict_date_times.keys())

        span = st.selectbox("Span Temporale", dict_date_times[block])
        st.write("Watch my data over ", span, block)

    with topcol2:
        chart = st.selectbox("Tipologia Grafico", type_plot)

        color = st.selectbox("Colore grafico", colors)

        st.write("Watch my data on ", chart, color)

    x, km, gain, mins = get_data_run(block, int(span))
    fig_distance, fig_gain, fig_hr = make_charts_figure(x, km, gain, mins, chart, color)

    st.write("")
    st.write("")
    st.write("Distance Chart")

    st.plotly_chart(fig_distance)
    col1, col2 = st.columns(2)

    with col1:
        st.write("")
        st.write("")
        st.write("Elevation Gain Chart")
        st.plotly_chart(fig_gain)

    with col2:
        st.write("")
        st.write("")
        st.write("Hour Chart")
        st.plotly_chart(fig_hr)


if "strava_api" not in st.session_state:
    st.warning("You Need To Login")
else:
    display_charts(st.session_state["strava_api"].auth_code)
