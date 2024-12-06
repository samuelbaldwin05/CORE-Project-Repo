import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide', page_title = 'Faculty Home', page_icon = 'static/core-4.png')

SideBarLinks()

st.title(f"Welcome Faculty Advisor, {st.session_state['first_name']}.")

# Buttons link to other pages
if st.button('View Student Data',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/31_Student_Data.py')

if st.button('Alter Student Data',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/33_Alter_Students.py')

if st.button('View Current Positions',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_View_Job_Postings.py')

if st.button('View Student Information',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/32_View_Student_Info.py')