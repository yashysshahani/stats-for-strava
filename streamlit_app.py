import streamlit as st
from authorization import Authorization
from urllib.parse import urlparse, parse_qs
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
                auth_button.auth_button()
        else:
            st.subheader("Welcome!")
            auth_url = auth.get_auth_url()
            auth_button.auth_button()

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
                auth_button.auth_button()
        else:
            auth.handle_access_token(code)
            try:
                page.page()
            except KeyError:
                st.session_state.clear()
                auth_url = auth.get_auth_url()
                st.write("Session expired. Please re-authorize. (3)")
                auth_button.auth_button()
