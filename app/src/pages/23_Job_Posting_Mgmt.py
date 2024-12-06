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
st.title("Job Posting Management")

def fetch_data():
    url = f'http://api:4000/j/JobPosting'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)
company_data = fetch_data()
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
with col1:
    st.subheader("Update Job Posting")
    status = st.text_input("Update Status")



with col2:
    st.subheader("Select Existing Posting")
    selected_posting= st.selectbox("Choose a PostingID", company_data["PostingID"])
    posting_update = {"Status": status}
    logger.info(f"Posting form form submitted with data: {selected_posting}")
    if st.button("Submit"):
        try:
            # using the requests library to POST to /p/product.  Passing
            # product_data to the endpoint through the json parameter.
                        # This particular end point is located in the products_routes.py
                        # file found in api/backend/products folder. 
            response = requests.put(f'http://api:4000/j/JobPosting/{selected_posting}', json=posting_update)
            if response.status_code == 200:
                st.write(f"Updated, go to Jobpostingview to see")
        except:
            print("not cool")

with col3:
    

with col4:
   