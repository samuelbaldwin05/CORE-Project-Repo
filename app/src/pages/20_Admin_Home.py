import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide', page_title = 'Admin Home', page_icon = 'static/core-4.png')

SideBarLinks()

st.title('System Admin Home Page')

# Buttons link to other pages
if st.button('Delete Incorrect Data',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Delete_Data.py')

if st.button('Change Company Info',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Change_Company_Info.py')

if st.button('Manage Job Postings',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_Job_Posting_Mgmt.py')

