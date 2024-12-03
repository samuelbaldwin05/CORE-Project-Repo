import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('Review a Coop')

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