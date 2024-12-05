import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide', page_title = 'Co-op Data', page_icon = 'static/core-4.png')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

# Titles and description
st.title('Alter Student Data')
st.subheader("Students")
st.write("This page allows alteration or addition of students for a specific advisor. Since you are already logged, this only shows your students")

# Hardcoding advisor ID since already logged in
advisorID = 1

# Getting student data for advisor
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

# Getting operaiton info
choice = st.selectbox("What Would You Like To Do?", ['Alter Student', 'Add Student'])

# Creating form for student data alteration
if choice == 'Alter Student':
    position = st.selectbox("Select Student", df['NUID'].unique())
    index = df.index[df['NUID'] == position].tolist()
    index = index[0]
    st.write("Only fill out sections you would like to change.")
    with st.form(key='student_alterations'):
        nuid = st.number_input("NUID")
        username = st.text_input("Username")
        gpa = st.number_input("GPA")
        appcount = st.number_input("Application Count")
        offercount = st.numer_input('Offer Count')
        previous_offercount = st.numer_input('Offer Count')
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            if not nuid and not username and not gpa and not appcount and not offercount and not previous_offercount:
                st.error("Mising Input")
            else:
                comreview_data = {
                    "NUID": comID,
                    "Type": type,
                    "Description": review,
                    "EnvironmentRating": env_rating,
                    "CultureRating": culture_rating
                }
                logger.info(f"Product form submitted with data: {comreview_data}")
                try:
                    # using the requests library to POST to /p/product.  Passing
                    # product_data to the endpoint through the json parameter.
                    # This particular end point is located in the products_routes.py
                    # file found in api/backend/products folder. 
                    response = requests.post('http://api:4000/c/CompanyReview', json=comreview_data)
                    if response.status_code == 200:
                        st.success("Product added successfully!")
                    else:
                        st.error(f"Error adding product: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")

