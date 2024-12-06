import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

st.set_page_config(layout='wide', page_title='Company Review', page_icon='static/core-4.png')
SideBarLinks()

# Creating title and getting relationship of user to the company
st.title("Change Company Info")

# Function to get company stats
def fetch_data():
    url = f'http://api:4000/c/Company/stats'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)

# Call fetch function to get company stats
company_data = fetch_data()

# Choose Existing Company to Change Name
st.subheader("Select Existing Company")
selected_company = st.selectbox("Choose Company", company_data["CompanyName"].unique())

# Input New Company
st.subheader("Change Company Name")
new_company_name = st.text_input("Input New Company Name")

company_update = {"Name": new_company_name}
logger.info(f"Product form submitted with data: {company_update}")
company_id = company_data.loc[company_data['CompanyName'] == selected_company, 'CompanyID'].iloc[0]
if st.button("Submit"):
    try:
        # Put request to update company name from id
        response = requests.put(f'http://api:4000/c/Company/{company_id}', json=company_update)
        if response.status_code == 200:
            st.write(f"Properly Updated Company Name")
    except:
        print("Error")

        
   