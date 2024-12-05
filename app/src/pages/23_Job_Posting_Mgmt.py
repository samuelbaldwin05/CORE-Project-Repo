import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide', page_title = 'Job Posting Management', page_icon = 'static/core-4.png')

SideBarLinks()

st.title('Job Postings Management')
