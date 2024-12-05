import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide', page_title = 'Co-op Data', page_icon = 'static/core-4.png')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('Alter Student Data')
st.write("This page allows alteration or addition of students for a specific advisor. Since you are already logged, this only shows your students")

advisorID = 1

def fetch_data():
    url = f'http://api:4000/u/users/{advisorID}'
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        # Assuming your data is a list of dictionaries
        if data:
            return pd.DataFrame(data)
        else:
            st.warning("No data available for the given advisor ID.")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return pd.DataFrame()

df = fetch_data()
st.dataframe(df)

st.subheader("What Would You Like To Do?")
menu = [df['NUID']]
position = st.selectbox("Select User", menu.unique())

