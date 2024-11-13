import streamlit as st

front_end_dir = "./frontend/pages/"


def home():
    # Page to add your credentials that unlock all the other pages --> This file
    user_stats = st.Page(f"{front_end_dir}/user_stats.py", title="Personal Stats", icon="👤")
    run_comparison = st.Page(f"{front_end_dir}/compare.py", title="Compare Your Runs", icon="⏱️")
    map_page = st.Page(f"{front_end_dir}/map.py", title="Segment Map Search", icon="🗺️")
    chart_page = st.Page(f"{front_end_dir}/get_token.py", title="Charts Page", icon="🔑")
    # my_koms = st.Page(f"{front_end_dir}/my_koms.py", title="My Koms", icon="")
    # last_activities = st.Page(f"{front_end_dir}/last_activities.py", title="Last Activities", icon="")

    pg = st.navigation(
        [user_stats, run_comparison, map_page, chart_page]
    )  #  my_koms, last_activities
    pg.run()
