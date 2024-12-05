import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

# Title and retrieving users relationship to position up for review
st.title('Review a Coop')
menu = ['Rejected', 'Interview Stage', 'Offered Job', 'Took Position']
choice = st.selectbox("Stage Reached", menu)

# Creating form for if they were rejected from the job
if choice == 'Rejected':
    st.subheader("Position Form")
    with st.form(key='RejectForm'):
        difficulty = st.number_input('Application Difficulty Rating (1-5)', 1, 5)
        date_applied = st.date_input('Date of Application')
        date_results = st.date_input('Date of Results')
        gpa = st.number_input('GPA')
        review = st.text_input('Review Space')
        appyield = 0
        interviewnum = 0
        submit_button = st.form_submit_button(label='Submit')
        # # Posting data to database
        # if submit_button:
        #     if not difficulty or not date_results or not date_applied or not gpa or not review:
        #         st.error("Mising Input")
        #     else:
        #         review_data = {
        #             "Description": review,
        #             "Offer": False,
        #             "ApplicationRating": difficulty,
        #             "EnvironmentRating": None,
        #             "EnjoymentRating": None,
        #             "Applied": True,
        #             "AppliedDate": date_applied,
        #             "ResposeDate": date_results,
        #             "PositionID": None
        #         }
        #         logger.info(f"Product form submitted with data: {review_data}")
        #         try:
        #             # using the requests library to POST to /p/product.  Passing
        #             # product_data to the endpoint through the json parameter.
        #             # This particular end point is located in the products_routes.py
        #             # file found in api/backend/products folder. 
        #             response = requests.post('http://api:4000/p/product', json=review_data)
        #             if response.status_code == 200:
        #                 st.success("Product added successfully!")
        #             else:
        #                 st.error(f"Error adding product: {response.text}")
        #         except requests.exceptions.RequestException as e:
                    # st.error(f"Error connecting to server: {str(e)}")


# Creating form for if they were interviewed for the job
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
        # # Posting data to database
        # if submit_button:
        #     if not difficulty or not date_results or not date_applied or not gpa or not review:
        #         st.error("Mising Input")
        #     else:
        #         review_data = {
        #             "Description": review,
        #             "Offer": False,
        #             "ApplicationRating": difficulty,
        #             "EnvironmentRating": None,
        #             "EnjoymentRating": None,
        #             "Applied": True,
        #             "AppliedDate": date_applied,
        #             "ResposeDate": date_results,
        #             "PositionID": None
        #         }
        #         logger.info(f"Product form submitted with data: {review_data}")
        #         try:
        #             # using the requests library to POST to /p/product.  Passing
        #             # product_data to the endpoint through the json parameter.
        #             # This particular end point is located in the products_routes.py
        #             # file found in api/backend/products folder. 
        #             response = requests.post('http://api:4000/p/product', json=review_data)
        #             if response.status_code == 200:
        #                 st.success("Product added successfully!")
        #             else:
        #                 st.error(f"Error adding product: {response.text}")
        #         except requests.exceptions.RequestException as e:
                    # st.error(f"Error connecting to server: {str(e)}")


# Creating form for if they were offered the job
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
        # # Posting data to database
        # if submit_button:
        #     if not difficulty or not date_results or not date_applied or not gpa or not review:
        #         st.error("Mising Input")
        #     else:
        #         review_data = {
        #             "Description": review,
        #             "Offer": True,
        #             "ApplicationRating": difficulty,
        #             "EnvironmentRating": None,
        #             "EnjoymentRating": None,
        #             "Applied": True,
        #             "AppliedDate": date_applied,
        #             "ResposeDate": date_results,
        #             "PositionID": None
        #         }
        #         logger.info(f"Product form submitted with data: {review_data}")
        #         try:
        #             # using the requests library to POST to /p/product.  Passing
        #             # product_data to the endpoint through the json parameter.
        #             # This particular end point is located in the products_routes.py
        #             # file found in api/backend/products folder. 
        #             response = requests.post('http://api:4000/p/product', json=review_data)
        #             if response.status_code == 200:
        #                 st.success("Product added successfully!")
        #             else:
        #                 st.error(f"Error adding product: {response.text}")
        #         except requests.exceptions.RequestException as e:
                    # st.error(f"Error connecting to server: {str(e)}")


# Creating form for if they took the job
if choice == 'Took Position':
    with st.form(key='PosWorkForm'):
        difficulty = st.number_input('Application Difficulty Rating (1-5)', 1, 5)
        data_applied = st.date_input('Date of Application')
        date_results = st.date_input('Date of Results')
        gpa = st.number_input('GPA')
        interviewnum = st.number_input('Number of Interviews Had')
        env_rating = st.number_input('Rating of Environment While Working (1-5)', 1, 5)
        education_rating = st.number_input('Rating of Education Received While Working (1-5)', 1, 5)
        enjoyment_rating = st.number_input('Overall Enjoyment of Position (1-5)', 1, 5)
        review = st.text_input('Review Space')
        appyield = 1
        submit_button = st.form_submit_button(label='Submit')
        # # Posting data to database
        # if submit_button:
        #     if not difficulty or not date_results or not date_applied or not gpa or not review:
        #         st.error("Mising Input")
        #     else:
        #         review_data = {
        #             "Description": review,
        #             "Offer": True,
        #             "ApplicationRating": difficulty,
        #             "EnvironmentRating": env_rating,
        #             "EnjoymentRating": enjoyment_rating,
        #             "Applied": True,
        #             "AppliedDate": date_applied,
        #             "ResposeDate": date_results,
        #             "PositionID": None
        #         }
        #         logger.info(f"Product form submitted with data: {review_data}")
        #         try:
        #             # using the requests library to POST to /p/product.  Passing
        #             # product_data to the endpoint through the json parameter.
        #             # This particular end point is located in the products_routes.py
        #             # file found in api/backend/products folder. 
        #             response = requests.post('http://api:4000/p/product', json=review_data)
        #             if response.status_code == 200:
        #                 st.success("Product added successfully!")
        #             else:
        #                 st.error(f"Error adding product: {response.text}")
        #         except requests.exceptions.RequestException as e:
                    # st.error(f"Error connecting to server: {str(e)}")


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