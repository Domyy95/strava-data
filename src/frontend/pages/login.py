import streamlit as st
from src.settings import get_settings, get_Client_ID
from src.api.strava import StravaAPI


@st.cache_data
def load_strava_api(access_token, client_id, client_secret, auth_code):
    return StravaAPI(access_token, client_id, client_secret, auth_code)


@st.cache_data
def load_settings():
    return get_settings()


st.title("Login Page")


def display_first_part(client_id):
    st.subheader("Ottieni Codice Accesso")
    st.write("Accedi con strava per visualizzare i grafici", " 🔑")
    link = f"http://www.strava.com/oauth/authorize?client_id={client_id}<&response_type=code&redirect_uri=http://localhost:8506/&approval_prompt=force&scope=activity:read_all"
    if st.link_button("Login With Strava", link):
        st.markdown(
            """
            <script>
            window.close();
            </script>
            """,
            unsafe_allow_html=True,
        )


if "code" not in st.query_params.keys():
    client_id = get_Client_ID()
    display_first_part(client_id)
else:
    settings = load_settings()
    if "strava_api" not in st.session_state:
        st.session_state["strava_api"] = load_strava_api(
            settings.access_token,
            settings.client_id,
            settings.client_secret,
            st.query_params["code"],
        )
    with st.spinner("Getting your strava data"):
        st.session_state["strava_api"].autorization()
    st.subheader("Ti sei Loggato Correttamente . . .")
    st.write("")
    st.write("Ora puoi accedere alle tue informazioni tramite le pagine a sinistra")
