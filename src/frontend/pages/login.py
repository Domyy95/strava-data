import streamlit as st


def login_page(authorize_url):
    st.title("Login Page")
    st.write("Accedi con strava per visualizzare i grafici", " 🔑")
    if st.link_button("Login With Strava", authorize_url):
        st.markdown(
            """
            <script>
            window.close();
            </script>
            """,
            unsafe_allow_html=True,
        )

    query_params = st.query_params.keys()
    if "code" in query_params:
        auth_code = st.query_params["code"]

        if auth_code:
            st.success("Login effettuato con successo!")
            st.session_state.logged_in = True
            st.session_state.auth_code = auth_code
            st.switch_page("./main.py")
        else:
            st.error("Errore durante il login. Riprova.")
