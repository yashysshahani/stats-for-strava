import streamlit as st
from urllib.parse import urlencode
import webbrowser as wb


class Authorization:
    CLIENT_ID = "130208"
    CLIENT_SECRET = "27e2ad6b4be13544e7e02fbe523c7d20d8a52f4a"
    REDIRECT_URI = "http://localhost:8506"

    def __init__(self):
        pass

    def get_auth_url(self) -> str:
        params = {
            "client_id": self.CLIENT_ID,
            "redirect_uri": self.REDIRECT_URI,
            "response_type": "code",
            "approval_prompt": "auto",
            "scope": "read_all,activity:read_all",
        }
        encoded_params = urlencode(params)
        return f"https://www.strava.com/oauth/authorize?{encoded_params}"
    
    def open_auth_window(self):
        auth_url = self.get_auth_url()
        new_window = st.query_params.get("new_window", [False])[0]
        if not new_window:
            wb.open(auth_url, new=0)

    
