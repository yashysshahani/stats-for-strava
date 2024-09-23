import streamlit as st
import strava_api
from activities import Activities
import data_analysis
from authorization import Authorization
from urllib.parse import urlparse, parse_qs
import visualization
import text
import page
import auth_button

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

    if st.session_state.get("access_token") is None:
        if code:
            auth.handle_access_token(code)
            try:
                page.page()
            except KeyError:
                st.session_state.clear()
                auth_url = auth.get_auth_url()
                st.write("Session expired. Please re-authorize. (1)")
                st.link_button("Connect with Strava", url=auth_url)
        else:
            st.subheader("Welcome!")
            st.write("Hit the authorization button below to get insights.")
            auth_url = auth.get_auth_url()
            st.link_button("Connect with Strava", url=auth_url)

    else:
        if st.session_state.code is None:
            auth.get_strava_code()
            auth.handle_access_token(code)
            try:
                page.page()
            except KeyError:
                st.session_state.clear()
                auth_url = auth.get_auth_url()
                st.write("Session expired. Please re-authorize. (2)")
                st.link_button("Connect with Strava", url=auth_url)
        else:
            auth.handle_access_token(code)
            try:
                page.page()
            except KeyError:
                st.session_state.clear()
                auth_url = auth.get_auth_url()
                st.write("Session expired. Please re-authorize. (3)")
                auth_button.auth_button()
