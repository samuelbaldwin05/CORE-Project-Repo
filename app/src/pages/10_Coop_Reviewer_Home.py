import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide', page_title = 'Reviewer Home', page_icon = 'static/core-4.png')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Reviewer, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

# Buttons link to other pages
if st.button('Review a Coop',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Coop_Review.py')

if st.button("Review a Company",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Company_Review.py')

if st.button('Search Co-ops By Position',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Search_By_Position.py')

if st.button('Search Co-ops By Company',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Search_By_Company.py')