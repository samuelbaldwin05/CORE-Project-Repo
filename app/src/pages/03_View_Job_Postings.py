import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import numpy as np
import random
import time
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide', page_title = 'Job Search', page_icon = 'static/core-4.png')
SideBarLinks()

def fetch_data():
    url = f'http://api:4000/j/job_posting/JobPosting'

    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        st.error("Failed to fetch data. Please check the server.")
        return pd.DataFrame()
    
df = fetch_data()

