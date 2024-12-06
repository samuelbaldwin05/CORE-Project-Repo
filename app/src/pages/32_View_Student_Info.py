import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide', page_title = 'Co-op Data', page_icon = 'static/core-4.png')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('View Student Information')

# Getting position data to select position under review
def fetch_data():
    url = f'http://api:4000/u/users/info'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)

df = fetch_data()
df = df[df["c.CollegeID"] == df["CollegeID"]]
df['AdvisorName'] = df['FirstName'] + " " + df['LastName']
col_order = ["Username", "NUID", "CollegeName", "MajorName", "GPA", "AppCount", "OfferCount", "AdvisorName"]
df = df[col_order]
#Rename the columns
rename_columns = {
        "CollegeName": "College",
        "MajorName": "Major",
        "AppCount": "# Apps",
        "OfferCount": "# Offers",
        "AdvisorName": "Advisor"
    }
df.rename(columns=rename_columns, inplace=True)
use_advisor = st.checkbox("View Only Your Students")
if use_advisor:
    df = df[df["Advisor"] == "Cammy Giles"]
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.dataframe(df, use_container_width=True, hide_index=True)