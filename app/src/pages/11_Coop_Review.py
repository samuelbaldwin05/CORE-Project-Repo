import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide', page_title = 'Co-op Review', page_icon = 'static/core-4.png')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

# Title and retrieving users relationship to position up for review
st.title('Review a Coop')



# Getting position data to select position under review
def fetch_data():
    url = f'http://api:4000/p/positions/info'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)

# Getting PositionID
df = fetch_data()
position = st.selectbox("Select Position", df['PositionName'].unique())
index = df.index[df['PositionName'] == position].tolist()
if index:
    posID = int(df.loc[index[0], 'PositionID'])
    st.write(f"**PositionID**: {posID}")
else:
    posID = None
    st.error("No PositionID found for the selected position.")



menu = ['Rejected', 'Interview Stage', 'Offered Job', 'Took Position']
choice = st.selectbox("Stage Reached", menu)

# Creating form for if they were rejected from the job
if choice == 'Rejected':
    st.subheader("Position Review Form")
    with st.form(key='RejectForm'):
        difficulty = st.number_input('Application Difficulty Rating (1-5)', 1, 5)
        date_applied = st.date_input('Date of Application')
        date_results = st.date_input('Date of Results')
        review = st.text_input('Review Space')
        submit_button = st.form_submit_button(label='Submit')
        # Posting data to database
        if submit_button:
            if not difficulty or not date_results or not date_applied or not review:
                st.error("Mising Input")
            else:
                review_data1 = {
                    "Description": review,
                    "Offer": False,
                    "ApplicationRating": difficulty,
                    "EnvironmentRating": None,
                    "EducationRating": None,
                    "EnjoymentRating": None,
                    "Applied": True,
                    "AppliedDate": date_applied.isoformat(),
                    "ResponseDate": date_results.isoformat(),
                    "PositionID": posID
                }
                logger.info(f"Reject form submitted with data: {review_data1}")
                try:
                    # using the requests library to POST to /p/product.  Passing
                    # product_data to the endpoint through the json parameter.
                    # This particular end point is located in the products_routes.py
                    # file found in api/backend/products folder. 
                    response = requests.post('http://api:4000/p/PositionReview/post', json=review_data1)
                    if response.status_code == 200:
                        st.success("Product added successfully!")
                    else:
                        st.error(f"Error adding product: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")
    st.subheader("Position Stat Form")  
    with st.form(key='rejectstatform'):
        gpa = st.number_input('GPA')
        submit_button = st.form_submit_button(label='Submit')
        # Posting data to database
        if submit_button:
            if gpa == 0:
                st.error("Mising Input")
            else:
                review_data = {
                    "YieldRate": 0,
                    "AvgAppAmount": 1,
                    "AvgInterview": 0,
                    "AvgGpa": gpa,
                    "AvgLearning": 0,
                    "AvgEnvironment": 0,
                    "AvgInterviewTime": 0,
                }
                logger.info(f"Reject stat form submitted with data: {review_data}")
                try:
                    # using the requests library to POST to /p/product.  Passing
                    # product_data to the endpoint through the json parameter.
                    # This particular end point is located in the products_routes.py
                    # file found in api/backend/products folder. 
                    response = requests.put(f'http://api:4000/p/posstats/{posID}', json=review_data)
                    if response.status_code == 200:
                        st.success("Product added successfully!")
                    else:
                        st.error(f"Error adding product: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")

# Creating form for if they were interviewed for the job
if choice == 'Interview Stage':
    st.subheader("Position Review Form")
    with st.form(key='IntForm'):
        difficulty = st.number_input('Application Difficulty Rating (1-5)', 1, 5)
        data_applied = st.date_input('Date of Application')
        date_results = st.date_input('Date of Results')
        review = st.text_input('Review Space')
        submit_button = st.form_submit_button(label='Submit')
        # Posting data to database
        if submit_button:
            if not difficulty or not date_results or not date_applied or not review:
                st.error("Mising Input")
            else:
                review_data1 = {
                    "Description": review,
                    "Offer": False,
                    "ApplicationRating": difficulty,
                    "EnvironmentRating": None,
                    "EducationRating": None,
                    "EnjoymentRating": None,
                    "Applied": True,
                    "AppliedDate": date_applied.isoformat(),
                    "ResponseDate": date_results.isoformat(),
                    "PositionID": posID
                }
                logger.info(f"Reject form submitted with data: {review_data1}")
                try:
                    # using the requests library to POST to /p/product.  Passing
                    # product_data to the endpoint through the json parameter.
                    # This particular end point is located in the products_routes.py
                    # file found in api/backend/products folder. 
                    response = requests.post('http://api:4000/p/PositionReview/post', json=review_data1)
                    if response.status_code == 200:
                        st.success("Product added successfully!")
                    else:
                        st.error(f"Error adding product: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")
    st.subheader("Position Stat Form")  
    with st.form(key='rejectstatform'):
        gpa = st.number_input('GPA')
        interviewnum = st.number_input('Number of Interviews Had')
        inttime = st.number_input('Estimated Interview Time in Mins')
        submit_button = st.form_submit_button(label='Submit')
        # Posting data to database
        if submit_button:
            if gpa == 0 or inttime == 0 or interviewnum == 0 :
                st.error("Mising Input")
            else:
                review_data = {
                    "YieldRate": 0,
                    "AvgAppAmount": 1,
                    "AvgInterview": interviewnum,
                    "AvgGpa": gpa,
                    "AvgLearning": 0,
                    "AvgEnvironment": 0,
                    "AvgInterviewTime": inttime,
                }
                logger.info(f"Reject stat form submitted with data: {review_data}")
                try:
                    # using the requests library to POST to /p/product.  Passing
                    # product_data to the endpoint through the json parameter.
                    # This particular end point is located in the products_routes.py
                    # file found in api/backend/products folder. 
                    response = requests.put(f'http://api:4000/p/posstats/{posID}', json=review_data)
                    if response.status_code == 200:
                        st.success("Product added successfully!")
                    else:
                        st.error(f"Error adding product: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")


# Creating form for if they were offered the job
if choice == 'Offered Job':
     st.subheader("Position Review Form")
     with st.form(key='OfferForm'):
        difficulty = st.number_input('Application Difficulty Rating (1-5)', 1, 5)
        data_applied = st.date_input('Date of Application')
        date_results = st.date_input('Date of Results')
        review = st.text_input('Review Space')
        submit_button = st.form_submit_button(label='Submit')
        # Posting data to database
        if submit_button:
            if not difficulty or not date_results or not date_applied or not gpa or not review:
                st.error("Mising Input")
            else:
                review_data = {
                    "Description": review,
                    "Offer": True,
                    "ApplicationRating": difficulty,
                    "EnvironmentRating": None,
                    "EducationRating": None,        
                    "EnjoymentRating": None,
                    "Applied": True,
                    "AppliedDate": date_applied,
                    "ResposeDate": date_results,
                    "PositionID": posID
                }
                logger.info(f"Product form submitted with data: {review_data}")
                try:
                    # using the requests library to POST to /p/product.  Passing
                    # product_data to the endpoint through the json parameter.
                    # This particular end point is located in the products_routes.py
                    # file found in api/backend/products folder. 
                    response = requests.post('http://api:4000/p/product', json=review_data)
                    if response.status_code == 200:
                        st.success("Product added successfully!")
                    else:
                        st.error(f"Error adding product: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")
     st.subheader("Position Stat Form")
     with st.form(key='rejectstatform'):
        gpa = st.number_input('GPA')
        interviewnum = st.number_input('Number of Interviews Had')
        inttime = st.number_input('Estimated Interview Time in Mins')
        submit_button = st.form_submit_button(label='Submit')
        # Posting data to database
        if submit_button:
            if gpa == 0 or inttime == 0 or interviewnum == 0 :
                st.error("Mising Input")
            else:
                review_data = {
                    "YieldRate": 1,
                    "AvgAppAmount": 1,
                    "AvgInterview": interviewnum,
                    "AvgGpa": gpa,
                    "AvgLearning": 0,
                    "AvgEnvironment": 0,
                    "AvgInterviewTime": inttime,
                }
                logger.info(f"Reject stat form submitted with data: {review_data}")
                try:
                    # using the requests library to POST to /p/product.  Passing
                    # product_data to the endpoint through the json parameter.
                    # This particular end point is located in the products_routes.py
                    # file found in api/backend/products folder. 
                    response = requests.put(f'http://api:4000/p/posstats/{posID}', json=review_data)
                    if response.status_code == 200:
                        st.success("Product added successfully!")
                    else:
                        st.error(f"Error adding product: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")


# Creating form for if they took the job
if choice == 'Took Position':
    st.subheader("Position Review Form")
    with st.form(key='PosWorkForm'):
        difficulty = st.number_input('Application Difficulty Rating (1-5)', 1, 5)
        data_applied = st.date_input('Date of Application')
        date_results = st.date_input('Date of Results')
        env_rating = st.number_input('Rating of Environment While Working (1-5)', 1, 5)
        education_rating = st.number_input('Rating of Education Received While Working (1-5)', 1, 5)
        enjoyment_rating = st.number_input('Overall Enjoyment of Position (1-5)', 1, 5)
        review = st.text_input('Review Space')
        appyield = 1
        submit_button = st.form_submit_button(label='Submit')
        # Posting data to database
        if submit_button:
            if not difficulty or not date_results or not date_applied or not gpa or not review:
                st.error("Mising Input")
            else:
                review_data = {
                    "Description": review,
                    "Offer": True,
                    "ApplicationRating": difficulty,
                    "EnvironmentRating": env_rating,
                    "EducationRating": education_rating,
                    "EnjoymentRating": enjoyment_rating,
                    "Applied": True,
                    "AppliedDate": date_applied,
                    "ResponseDate": date_results,
                    "PositionID": posID
                }
                logger.info(f"Product form submitted with data: {review_data}")
                try:
                    # using the requests library to POST to /p/product.  Passing
                    # product_data to the endpoint through the json parameter.
                    # This particular end point is located in the products_routes.py
                    # file found in api/backend/products folder. 
                    response = requests.post('http://api:4000/p/product', json=review_data)
                    if response.status_code == 200:
                        st.success("Product added successfully!")
                    else:
                        st.error(f"Error adding product: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")
    st.subheader("Position Stat Form")
    with st.form(key='rejectstatform'):
        gpa = st.number_input('GPA')
        interviewnum = st.number_input('Number of Interviews Had')
        inttime = st.number_input('Estimated Interview Time in Mins')
        submit_button = st.form_submit_button(label='Submit')
        # Posting data to database
        if submit_button:
            if gpa == 0 or inttime == 0 or interviewnum == 0 :
                st.error("Mising Input")
            else:
                review_data = {
                    "YieldRate": 1,
                    "AvgAppAmount": 1,
                    "AvgInterview": interviewnum,
                    "AvgGpa": gpa,
                    "AvgLearning": education_rating,
                    "AvgEnvironment": env_rating,
                    "AvgInterviewTime": inttime,
                }
                logger.info(f"Reject stat form submitted with data: {review_data}")
                try:
                    # using the requests library to POST to /p/product.  Passing
                    # product_data to the endpoint through the json parameter.
                    # This particular end point is located in the products_routes.py
                    # file found in api/backend/products folder. 
                    response = requests.put(f'http://api:4000/p/posstats/{posID}', json=review_data)
                    if response.status_code == 200:
                        st.success("Product added successfully!")
                    else:
                        st.error(f"Error adding product: {response.text}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to server: {str(e)}")