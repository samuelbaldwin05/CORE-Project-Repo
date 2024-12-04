import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()


def fetch_data(position_id=None):
    if position_id:
        url = f'http://localhost:4000/PositionReview/{position_id}'  # Replace with your actual API base URL
    else:
        url = 'http://localhost:4000/PositionReview'  # Endpoint for all reviews
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx/5xx)
        data = response.json()
        return pd.DataFrame(data)  # Convert to DataFrame for easy manipulation
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        st.error("Failed to fetch data. Please check the server.")
        return pd.DataFrame()  # Return an empty DataFrame on error
    
    


st.title('Review a Coop')
menu = ['Rejected', 'Interview Stage', 'Offered Job', 'Took Position']
choice = st.selectbox("Stage Reached", menu)


if choice == 'Rejected':
    st.subheader("Position Form")
    with st.form(key='RejectForm'):
        difficulty = st.number_input('Application Difficulty Rating (1-5)', 1, 5)
        data_applied = st.date_input('Date of Application')
        date_results = st.date_input('Date of Results')
        gpa = st.number_input('GPA')
        review = st.text_input('Review Space')
        appyield = 0
        interviewnum = 0
        submit_button = st.form_submit_button(label='Submit')

if choice == 'Interview Stage':
    with st.form(key='IntForm'):
        difficulty = st.number_input('Application Difficulty Rating (1-5)', 1, 5)
        data_applied = st.date_input('Date of Application')
        date_results = st.date_input('Date of Results')
        gpa = st.number_input('GPA')
        interviewnum = st.number_input('Number of Interviews Had')
        review = st.text_input('Review Space')
        appyield = 0
        submit_button = st.form_submit_button(label='Submit')

if choice == 'Offered Job':
     with st.form(key='OfferForm'):
        difficulty = st.number_input('Application Difficulty Rating (1-5)', 1, 5)
        data_applied = st.date_input('Date of Application')
        date_results = st.date_input('Date of Results')
        gpa = st.number_input('GPA')
        interviewnum = st.number_input('Number of Interviews Had')
        review = st.text_input('Review Space')
        appyield = 1
        submit_button = st.form_submit_button(label='Submit')

if choice == 'Took Position':
    with st.form(key='PosWorkForm'):
        difficulty = st.number_input('Application Difficulty Rating (1-5)', 1, 5)
        data_applied = st.date_input('Date of Application')
        date_results = st.date_input('Date of Results')
        gpa = st.number_input('GPA')
        interviewnum = st.number_input('Number of Interviews Had')
        env_rating = st.number_input('Rating of Environment While Working (1-5)', 1, 5)
        education_rating = st.number_input('Rating of Education Received While Working (1-5)', 1, 5)
        professionality_rating = st.number_input('Overall Enjoyment of Position (1-5)', 1, 5)
        review = st.text_input('Review Space')
        appyield = 1
        submit_button = st.form_submit_button(label='Submit')

results = requests.get(f'http://api:4000/PostStats').json()
st.dataframe(results)

# Either a get route that automatically runs to show all co-ops that can be reviewed
# Or a form that can be filled out then submitted as a put route to enter info into
# Review database. 1st is better, 2nd is easier


# # create a 2 column layout
# col1, col2 = st.columns(2)
#
# # add one number input for variable 1 into column 1
# with col1:
#   var_01 = st.number_input('Variable 01:',
#                            step=1)
#
# # add another number input for variable 2 into column 2
# with col2:
#   var_02 = st.number_input('Variable 02:',
#                            step=1)
#
# logger.info(f'var_01 = {var_01}')
# logger.info(f'var_02 = {var_02}')
#
# # add a button to use the values entered into the number field to send to the
# # prediction function via the REST API
# if st.button('Calculate Prediction',
#              type='primary',
#              use_container_width=True):
#   results = requests.get(f'http://api:4000/c/prediction/{var_01}/{var_02}').json()
#   st.dataframe(results)
#
# st.write("# Accessing a REST API from Within Streamlit")
#
# """
# Simply retrieving data from a REST api running in a separate Docker Container.
#
# If the container isn't running, this will be very unhappy.  But the Streamlit app
# should not totally die.
# """
# data = {}
# try:
#   data = requests.get('http://api:4000/data').json()
# except:
#   st.write("**Important**: Could not connect to sample api, so using dummy data.")
#   data = {"a":{"b": "123", "c": "hello"}, "z": {"b": "456", "c": "goodbye"}}
#
# st.dataframe(data)