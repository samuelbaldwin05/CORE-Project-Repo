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
    url = f'http://api:4000/j/Info'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)

st.title("Current Job Postings")   
st.write("Learning and Environment are the average of position ratings, GPA is the average applicant GPA.")
df = fetch_data()
# Reorder columns
col_order = ["Name", "PositionName", "DatePosted", "YieldRate", "AvgAppAmount", "AvgGpa", "AvgLearning", "AvgEnvironment"]
df = df[col_order]

# Rename the columns
rename_columns = {
        "Name": "Company",
        "PositionName": "Position",
        "DatePosted": "Date Posted",
        "YieldRate": "Yield (%)",
        "AvgAppAmount": "# Apps",
        "AvgGpa": "GPA",
        "AvgLearning": "Learning",
        "AvgEnvironment": "Environment"
    }
df.rename(columns=rename_columns, inplace=True)
df['Yield (%)'] = (df['Yield (%)'] * 100)
st.dataframe(df, use_container_width=True, hide_index=True)
