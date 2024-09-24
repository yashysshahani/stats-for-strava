import streamlit as st
import base64
from pathlib import Path

CLIENT_ID = st.secrets["CLIENT_ID"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded_img = base64.b64encode(img_bytes).decode()
    return encoded_img

def auth_button():
    img = img_to_bytes("connect.png")
    st.markdown(
        f'''<a href="https://www.strava.com
        oauth/authorize?client_id={CLIENT_ID}
        &redirect_uri={REDIRECT_URI}&response_type=code
        &approval_prompt=auto&scope=read_all,activity:read_all"
          target="_blank">
        <img src="data:image/png;base64,{img}">
        </a>''',
        unsafe_allow_html=True
    )
    