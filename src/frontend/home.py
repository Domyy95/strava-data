import streamlit as st

front_end_dir = "./frontend/pages/"


def home():
    map_page = st.Page(f"{front_end_dir}/map.py", title="Segment Map Search", icon="🗺️")
    run_comparison = st.Page(f"{front_end_dir}/compare.py", title="Compare Runs", icon="⏱️")
    personal_stats = st.Page(f"{front_end_dir}/user_stats.py", title="Personal Stats", icon="👤")
    # other_user_stats = st.Page(f"{front_end_dir}/other_user_stats.py", title="Other User Stats", icon="👥")

    pg = st.navigation([map_page, run_comparison, personal_stats])
    pg.run()
