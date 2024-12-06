import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide', page_title = 'Co-op Data', page_icon = 'static/core-4.png')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('View Co-op Data')

def fetch_data():
    url = f'http://api:4000/c/Company'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)