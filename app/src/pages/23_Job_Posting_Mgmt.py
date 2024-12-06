import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from datetime import datetime

st.set_page_config(layout='wide', page_title='Company Review', page_icon='static/core-4.png')
SideBarLinks()

# Creating title and getting relationship of user to the company
def fetch_company():
    url = f'http://api:4000/c/Company/stats'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)

st.title("Job Posting Management")
def fetch_positions():
    url = f'http://api:4000/p/positions/info'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)

col1, col2= st.columns(2)
# Route to fetch data
def fetch_data():
    url = f'http://api:4000/j/JobPosting'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)
# Fetch Data

with col1:
    df = fetch_data()
    st.subheader("Change Posting Status")
    selected_pos_name= st.selectbox("Choose a Posting", df["PositionName"].unique())

    PositionID = df.loc[df['PositionName'] == selected_pos_name, 'PositionID'].iloc[0]
    status_value = df.loc[df['PositionName'] == selected_pos_name, 'Status'].iloc[0]
    #st.dataframe(selected_posting)
    if status_value == 1:
        st.write("Current Status: Posted")
    else:
        st.write("Current Status: Unposted")
    checkbox_status = st.checkbox("Status", value=(status_value == 1))

    if checkbox_status:
        status = "TRUE"
        st.write("New Status: Posted")
    else:
        status = "FALSE"
        st.write("New Status: Unposted")



    posting_update = {"Status":bool(status)}
    logger.info(f"Posting form submitted with data: {PositionID}")
    if st.button("Submit"):
        try:
            # using the requests library to POST to /p/product.  Passing
            # product_data to the endpoint through the json parameter.
                        # This particular end point is located in the products_routes.py
                        # file found in api/backend/products folder. 
            response = requests.put(f'http://api:4000/j/JobPosting/{PositionID}', json=posting_update)
            if response.status_code == 204:
                st.success("Posting Updated!")
            else:
                st.write(response.text)
        except:
            st.write("Error")

with col2:
    st.subheader("Create New Posting")
    df = fetch_positions()
    df2 = fetch_company()
    PositionName = st.selectbox("Choose a PositionID", df["PositionName"].unique())
    CompanyName = st.selectbox("Choose a companyID", df2["CompanyName"])
    PositionID = df.loc[df['PositionName'] == PositionName, 'PositionID'].iloc[0]
    CompanyID = df2.loc[df2['CompanyName'] == CompanyName, 'CompanyID'].iloc[0]
    DatePosted = st.date_input("Select Posting Date", value=datetime.now().date())
    checkbox_status2 = st.checkbox("Posting Status")
    if checkbox_status2:
        Status = 1
    else:
        Status = 0
    posting_json= {"DatePosted": str(DatePosted), "Status":bool(Status), "PositionID":int(PositionID), "CompanyID": int(CompanyID)}
    if st.button("Submit New Posting"):
        response = requests.post('http://api:4000/j/JobPosting', json=posting_json)
        if response.status_code == 204:
                    st.success("Posting Created!")
    