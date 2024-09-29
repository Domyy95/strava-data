import streamlit as st
from src.api.strava_model import DetailedAthlete, ActivityStats, ActivityTotal

st.title("📈 Personal Data")


def format_distance(distance_km: float) -> str:
    return f"{distance_km / 1000:.1f} km"


def format_moving_time(total_seconds: int) -> str:
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours} h {minutes} min"


def display_activity_stats(title: str, stats: ActivityTotal):
    st.subheader(title)
    distance = format_distance(stats.distance)
    moving_time = format_moving_time(stats.moving_time)
    st.write(f"- Distance: {distance}")
    st.write(f"- Moving Time: {moving_time}")
    st.write(f"- Elevation Gain: {int(stats.elevation_gain)} m")


def display_user_stats(athlete: DetailedAthlete, stats: ActivityStats):
    # 1. Display profile picture, weight, friend count, and follower count
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        profile_img = athlete.profile_medium
        st.image(profile_img, width=80)
    with col2:
        st.write("**Weight**")
        st.write(f"{athlete.weight} kg")
    with col3:
        st.write("**Following**")
        st.write(f"{athlete.friend_count}")
    with col4:
        st.write("**Followers**")
        st.write(f"{athlete.follower_count}")

    # 2. Display shoes with some data
    st.subheader("Shoes 👟")
    shoe_cols = st.columns(3)
    for idx, shoe in enumerate(athlete.shoes):
        with shoe_cols[idx % 3]:
            if not shoe.retired:
                st.write(f"**Shoe Name**: {shoe.name}")
                st.write(f"**Distance Covered**: {shoe.converted_distance} km")

    # 3. Display activity stats (all-time, year-to-date, and recent)
    st.subheader("Activity Stats 📊")
    col1, col2, col3 = st.columns(3)
    with col1:
        display_activity_stats("All Time", stats.all_run_totals)
    with col2:
        display_activity_stats("Year", stats.ytd_run_totals)
    with col3:
        display_activity_stats("Month", stats.recent_run_totals)

    # 4. Display clubs with the link and image
    st.subheader("Clubs 🏃‍♂️")
    cols = st.columns(3)
    for idx, club in enumerate(athlete.clubs):
        with cols[idx % 3]:
            club_img = club.cover_photo
            club_link = f'<a href="https://www.strava.com/clubs/{club.url}" target="_blank"><img src="{club_img}" width="150"></a>'
            st.markdown(club_link, unsafe_allow_html=True)


display_user_stats(
    st.session_state["strava_api"].authenticated_athlete,
    st.session_state["strava_api"].authenticated_athlete_stats,
)
