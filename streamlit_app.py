import streamlit as st
import strava_api
from activities import Activities
import data_analysis
from authorization import Authorization
from urllib.parse import urlparse, parse_qs
import visualization
import text
import page

# Title
st.title("🚴 Stats for Strava")

# Authorization
if __name__ == "__main__":
    auth = Authorization()
    code = auth.get_strava_code()
    if st.session_state.get("code") is None:
        st.session_state.code = code
    code = st.session_state.code

    if "access_token" not in st.session_state:
        st.session_state.access_token = None

    if code:
        access_token = auth.handle_access_token(code)
        if st.session_state.access_token is None:
            st.session_state.access_token = access_token
        try:
            page.page()
        except KeyError:
            st.session_state.clear()
            auth_url = auth.get_auth_url(
            )
            auth.handle_access_token(code)
            st.write("Session expired. Please re-authorize. (1)")
            st.link_button("Connect with Strava", url=auth_url)
    else:
        st.subheader("Welcome!")
        st.write("Hit the authorization button below to get insights.")
        auth_url = auth.get_auth_url()
        st.link_button("Connect with Strava", url=auth_url)
