import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide', page_title = 'About', page_icon = 'static/core-4.png')

# Be able to go back to home from about page, but dont show 
# home when using about page from authenticated user
if not st.session_state['authenticated']:
    SideBarLinks(show_home=True)
else:
    SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    This is an app intended to help Northeastern students
    find co-ops that are right for them.
    
    Students can leave reviews on co-ops or the company they have worked for or applied to a position for,
    rating and describing their experience so other students
    can get a better sense of if they want to apply. 
    """
        )
