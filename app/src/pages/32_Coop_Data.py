import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide', page_title = 'Co-op Data', page_icon = 'static/core-4.png')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('View Co-op Data')

# Getting position data to select position under review
def fetch_data():
    url = f'http://api:4000/p/positions/info'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)

# Getting PositionID
df = fetch_data()
position = st.selectbox("Select Position", df['PositionName'].unique())
index = df.index[df['PositionName'] == position].tolist()
if index:
    posID = int(df.loc[index[0], 'PositionID'])
    st.write(f"**PositionID**: {posID}")
else:
    posID = None
    st.error("No PositionID found for the selected position.")

def fetch_poststats_data(posID):
    url = f'http://api:4000/j/JobPosting/id/{posID}'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)

df = fetch_poststats_data(posID)
st.dataframe(df)
