import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide', page_title = 'Company Search', page_icon = 'static/core-4.png')
SideBarLinks()

st.title("Search By Company")
# You can access the session state to make a more customized/personalized app experience

def fetch_data():
    url = f'http://api:4000/c/Company/info'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)


df = fetch_data()

position = st.selectbox("Select Company", df['CompanyName'].unique())
filtered_df = df[df['CompanyName'] == position]

if len(filtered_df) != 0:
    # Create two columns
    col1, col2 = st.columns(2)

    # Display position info in the first column
    with col1:   
        # Get the first row of filtered data
        comp_info = filtered_df.iloc[0]
        
        st.header(f"Company Name: {comp_info['CompanyName']}")

        st.subheader("General Information")
        st.write(f"**Address**: {(comp_info['Address'])}")
        st.write(f"**City**: {comp_info['City']}")
        st.write(f"**Country**: {comp_info['CountryCode']}")
        st.write(f"**State**: {comp_info['State']}")
        st.write(f"**Company Size**: {comp_info['CompanySize']}")
        st.write(f"**Industry**: {comp_info['Industry']}")
        
    # Display reviewer information in the second column
    with col2:
        st.header(f"Employee Reviews")
 
        for _, reviewer in filtered_df.iterrows():
            st.subheader(f"Reviewer: {reviewer['ReviewerUsername']}")
            st.write(f"**Employment Type**: {reviewer['ReviewType']}")
            st.write(f"**Description**: {comp_info['ReviewDescription']}")
            st.write(f"**Environment Rating**: {reviewer['EnvironmentRating']}")
            st.write(f"**Culture Rating**: {reviewer['CultureRating']}")

            st.write("----------")
            st.write("")

else:
    st.write("No data available for the selected position.")