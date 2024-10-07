import streamlit as st

front_end_dir = "./frontend/pages/"


def home():
    personal_stats = st.Page(f"{front_end_dir}/user_stats.py", title="Personal Stats", icon="👤")
    run_comparison = st.Page(f"{front_end_dir}/compare.py", title="Compare Runs", icon="⏱️")
    map_page = st.Page(f"{front_end_dir}/map.py", title="Segment Map Search", icon="🗺️")
    # other_user_stats = st.Page(f"{front_end_dir}/other_user_stats.py", title="Other User Stats", icon="👥")

    pg = st.navigation([personal_stats, run_comparison, map_page])
    pg.run()
