import streamlit as st

front_end_dir = "./frontend/pages/"


def home():
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # Page to add your credentials that unlock all the other pages --> This file
    user_stats = st.Page(f"{front_end_dir}/user_stats.py", title="Personal Stats", icon="👤")
    run_comparison = st.Page(f"{front_end_dir}/compare.py", title="Compare Your Runs", icon="⏱️")
    map_page = st.Page(f"{front_end_dir}/map.py", title="Segment Map Search", icon="🗺️")
    chart_page = st.Page(f"{front_end_dir}/charts.py", title="Charts Page", icon="📊")
    login = st.Page(f"{front_end_dir}/login.py", title="Login", icon="🔑")
    # my_koms = st.Page(f"{front_end_dir}/my_koms.py", title="My Koms", icon="")
    # last_activities = st.Page(f"{front_end_dir}/last_activities.py", title="Last Activities", icon="")

    pg = st.navigation(
        [login, run_comparison, map_page, chart_page, user_stats]
    )  #  my_koms, last_activities
    pg.run()
