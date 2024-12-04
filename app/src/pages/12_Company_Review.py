import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Review a Company")
menu = ['Applied To Work For', 'Worked For']
choice = st.selectbox("Connection To Company", menu)

if choice == 'Applied To Work For':
    st.subheader("ComAppForm")
    with st.form(key='RejectForm'):
        difficulty = st.number_input('Application Difficulty Rating (1-5)', 1, 5)
        data_applied = st.date_input('Date of Application')
        date_results = st.date_input('Date of Results')
        gpa = st.number_input('GPA')
        review = st.text_input('Review Space')
        appyield = 0
        interviewnum = 0
        submit_button = st.form_submit_button(label='Submit')

if choice == 'Worked For':
    with st.form(key='ComWorkForm'):
        difficulty = st.number_input('Application Difficulty Rating (1-5)', 1, 5)
        data_applied = st.date_input('Date of Application')
        date_results = st.date_input('Date of Results')
        gpa = st.number_input('GPA')
        interviewnum = st.number_input('Number of Interviews Had')
        review = st.text_input('Review Space')
        appyield = 0
        submit_button = st.form_submit_button(label='Submit')