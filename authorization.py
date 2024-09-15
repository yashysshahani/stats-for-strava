import streamlit as st
from urllib.parse import urlencode
import webbrowser as wb
import strava_api


# Set mode to "dev" for development and "prod" for production

mode = "prod"
CLIENT_ID = None
CLIENT_SECRET = None
REDIRECT_URI = None

if mode == "dev":
    CLIENT_ID = st.secrets["DEV_ID"]
    CLIENT_SECRET = st.secrets["DEV_SECRET"]
    REDIRECT_URI = st.secrets["DEV_URI"]

elif mode == "prod":
    CLIENT_ID = st.secrets["CLIENT_ID"]
    CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
    REDIRECT_URI = st.secrets["REDIRECT_URI"]


class Authorization:
    CLIENT_ID = CLIENT_ID
    CLIENT_SECRET = CLIENT_SECRET
    REDIRECT_URI = REDIRECT_URI

    def __init__(self):
        self.code = None
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

    def get_strava_code(self):
        try:
            code = st.query_params["code"]
            self.code = code
        except KeyError:
            return False
        return code
    
    def handle_access_token(self, code):
        token_response = strava_api.get_access_token(
        CLIENT_ID, CLIENT_SECRET, code
        )
        access_token = token_response.get("access_token")
        return access_token
    


    
