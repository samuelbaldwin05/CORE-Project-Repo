import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests
from datetime import datetime

st.set_page_config(layout = 'wide', page_title = 'Position Search', page_icon = 'static/core-4.png')
# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.title('Search Co-ops By Position')

# You can access the session state to make a more customized/personalized app experience

def fetch_data():
    url = f'http://api:4000/p/positions/info'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)

# Maybe a drop down bar which allows you to search by position, industry, or company
# Dont need a home page then

df = fetch_data()

position = st.selectbox("Select Position", df['PositionName'].unique())
filtered_df = df[df['PositionName'] == position]

if len(filtered_df) != 0:
    # Create two columns
    col1, col2 = st.columns(2)

    # Display position info in the first column
    with col1:   
        # Get the first row of filtered data
        pos_info = filtered_df.iloc[0]
        
        # Use if-else to check for 1/0 and display Yes/No
        st.header(f"Position: {pos_info['PositionName']}")
        st.write(f"**Description**: {pos_info['PositionDescription']}")

        st.subheader("General Position Information")
        st.write(f"**Yield Rate**: {(pos_info['YieldRate']) * 100}%")
        #st.write(f"**Average Application Amount**: {pos_info['AvgAppAmount']}")
        #st.write(f"**Average Interview Amount**: {pos_info['AvgInterview']}")
        st.write(f"**Average Applicant GPA**: {pos_info['AvgGpa']}")
        st.write(f"**Average Learning Rating**: {pos_info['AvgLearning']}")
        st.write(f"**Average Environment Rating**: {pos_info['AvgEnvironment']}")
        
    # Display reviewer information in the second column
    with col2:
        st.header(f"Applicant Reviews")
 
        for _, reviewer in filtered_df.iterrows():
            st.subheader(f"Reviewer: {reviewer['Username']}")
            st.write(f"**Offer**: {'Yes' if reviewer['Offer'] == 1 else 'No'}")
            st.write(f"**Application Rating**: {reviewer['ApplicationRating']}")
            st.write(f"**Environment Rating**: {reviewer['EnvironmentRating']}")
            st.write(f"**Education Rating**: {reviewer['EducationRating']}")
            st.write(f"**Enjoyment Rating**: {reviewer['EnjoymentRating']}")
            st.write(f"**Position Applied**: {'Yes' if reviewer['Applied'] == 1 else 'No'}")
            st.write(f"**Applied Date**: {reviewer['AppliedDate']}")
            st.write(f"**Response Date**: {reviewer['ResponseDate']}")
            st.write("----------")
            st.write("")

else:
    st.write("No data available for the selected position.")