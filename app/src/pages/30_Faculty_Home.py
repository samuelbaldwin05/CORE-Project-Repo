import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f'Welcome Faculty Advisor, {st.session_state['first_name']}.')

if st.button('View Student Data',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/31_Student_Data.py')

if st.button('View Coop Data',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/32_Coop_Data.py')


