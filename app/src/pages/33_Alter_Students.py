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
st.title('Alter or Add Student Data')
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

# Form for wanting to alter students
if choice == 'Alter Student':
    st.subheader('Student Alteration Form')
    nuid = st.selectbox("Select Student", df['NUID'].unique())
    index = df.index[df['NUID'] == nuid].tolist()
    index = index[0] if index else None
    st.write("Only fill out sections you would like to change.")
    
    with st.form(key='student_alterations'):
        username = st.text_input("Username")
        majorid = st.number_input("MajorID")
        gpa = st.number_input("GPA")
        advisorid = st.number_input("AdvisorID")
        appcount = st.number_input("Application Count")
        offercount = st.number_input('Offer Count')
        previous_offercount = st.number_input('Previous Offer Count')
        submit_button = st.form_submit_button(label='Submit')

        # Making values None if not filled out
        username = username if username else None
        majorid = majorid if majorid != 0 else None
        gpa = gpa if gpa != 0 else None
        advisorid = advisorid if advisorid != 0 else None
        appcount = appcount if appcount != 0 else None
        offercount = offercount if offercount != 0 else None
        previous_offercount = previous_offercount if previous_offercount != 0 else None

        if submit_button:
            if not username and not gpa and not appcount and not majorid and not offercount and not advisorID and not previous_offercount:
                st.error("Missing Input")
            else:
                comreview_data = {
                    "Username": username,
                    "MajorID": majorid,
                    "GPA": gpa,
                    "AdvisorId": advisorid,
                    "AppCount": appcount,
                    "OfferCount": offercount,
                    "PreviousCount": previous_offercount
                }
                logger.info(f"User data alteration form submitted with data: {comreview_data}")
                
                try:
                    # Using PUT instead of POST
                    response = requests.put(f'http://api:4000/u/users/update/{nuid}', json=comreview_data)
                    if response.status_code == 200:
                        st.success("User data updated successfully!")
                    else:
                        st.error(f"Error updating user data: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")

# Form for wanting to add a student
if choice == 'Add Student':
    st.subheader('Student Addition Form')
    with st.form(key='addstudent'):
        nuid = st.text_input("NUID")
        username = st.text_input("Username")
        majorid = st.number_input("MajorID")
        gpa = st.number_input("GPA")
        advisorid = st.number_input("AdvisorID")
        appcount = st.number_input("Application Count")
        offercount = st.number_input('Offer Count')
        previous_offercount = st.number_input('Previous Offer Count')
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            if not nuid and not username and not gpa and not appcount and not majorid and not offercount and not advisorID and not previous_offercount:
                st.error("Missing Input")
            else:
                comreview_data = {
                    "NUID": nuid,
                    "Username": username,
                    "MajorID": majorid,
                    "GPA": gpa,
                    "AdvisorId": advisorid,
                    "AppCount": appcount,
                    "OfferCount": offercount,
                    "PreviousCount": previous_offercount
                }
                logger.info(f"User data alteration form submitted with data: {comreview_data}")
                
                try:
                    # Using PUT instead of POST
                    response = requests.post(f'http://api:4000/u/user/add', json=comreview_data)
                    if response.status_code == 200:
                        st.success("User data updated successfully!")
                    else:
                        st.error(f"Error updating user data: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")