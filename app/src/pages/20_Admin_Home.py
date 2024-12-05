import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide', page_title = 'Admin Home', page_icon = 'static/core-4.png')

SideBarLinks()

st.title('System Admin Home Page')

if st.button('Delete Incorrect Data',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Coop_Review_Mgmt.py')

if st.button('Manage Coop Reviews',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Company_Review_Mgmt.py')

if st.button('Manage Job Postings',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_Job_Posting_Mgmt.py')

