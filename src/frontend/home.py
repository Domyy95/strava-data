import streamlit as st

front_end_dir = "./frontend"


def home():
    map_page = st.Page(f"{front_end_dir}/map.py", title="Map", icon=":material/map:")
    run_comparison = st.Page(f"{front_end_dir}/compare.py", title="Compare runs", icon="⏱️")

    pg = st.navigation([map_page, run_comparison])
    pg.run()
