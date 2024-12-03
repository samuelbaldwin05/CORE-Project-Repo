import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Reviewer, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Review a Coop',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Coop_Review.py')

if st.button('View Coops',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_View_Coops.py')

if st.button("Review a Company",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Company_Review.py')