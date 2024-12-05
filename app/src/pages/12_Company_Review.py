import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Review a Company")
menu = ['Applied To Work For', 'Worked For']
choice = st.selectbox("Connection To Company", menu)

if choice == 'Applied To Work For':
    with st.form(key='RejectForm'):
        type = st.text_input("Extent of Relationship With Company")
        review = st.text_input("Review Space")
        submit_button = st.form_submit_button(label='Submit')
        # if submit_button:
        #     if not type or not review:
        #         st.error("Mising Input")
        #     else:
        #         product_data = {
        #             "Type": type,
        #             "Description": review,
        #             "EnvironmentRating": None,
        #             "CultureRating": None
        #         }
        #         logger.info(f"Product form submitted with data: {product_data}")
        #         try:
        #             # using the requests library to POST to /p/product.  Passing
        #             # product_data to the endpoint through the json parameter.
        #             # This particular end point is located in the products_routes.py
        #             # file found in api/backend/products folder. 
        #             response = requests.post('http://api:4000/p/product', json=product_data)
        #             if response.status_code == 200:
        #                 st.success("Product added successfully!")
        #             else:
        #                 st.error(f"Error adding product: {response.text}")
        #         except requests.exceptions.RequestException as e:
        #             st.error(f"Error connecting to server: {str(e)}")


if choice == 'Worked For':
    with st.form(key='ComWorkForm'):
        type = st.text_input("Extent of Relationship With Company")
        review = st.text_input("Review Space")
        envrating = st.number_input("Environment Rating (1-5)", 1, 5)
        culturerating = st.number_input("Culture Rating (1-5)", 1, 5)
        submit_button = st.form_submit_button(label='Submit')