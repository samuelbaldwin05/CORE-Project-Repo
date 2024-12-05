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
st.title("Company Management")

def fetch_data():
    url = f'http://api:4000/c/Company/stats'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)
company_data = fetch_data()
col1, col2 = st.columns(2)

with col1:
    st.subheader("Add New Company")
    new_company_name = st.text_input("Input new company name")



with col2:
    st.subheader("Select Existing Company")
    selected_company = st.selectbox("Choose a company", company_data["CompanyName"].unique())
    st.write(f"Selected company: {selected_company}")
    company_update = {"Name": new_company_name}
    logger.info(f"Product form submitted with data: {company_update}")
    company_id = company_data.loc[company_data['CompanyName'] == selected_company, 'CompanyID'].iloc[0]
    st.write(company_id)
    if st.button("Submit"):
        try:
            # using the requests library to POST to /p/product.  Passing
            # product_data to the endpoint through the json parameter.
                        # This particular end point is located in the products_routes.py
                        # file found in api/backend/products folder. 
            response = requests.put(f'http://api:4000/c/Company/{company_id}', json=company_update)
            if response.status_code == 200:
                st.write("Hurray")
            else: st.write(response.text)
        except:
            print("not cool")
        company_data = fetch_data()
            
            # Update the selectbox dynamically
        selected_company = st.selectbox("Choose a company", company_data["CompanyName"].unique())
    st.experimental_rerun()