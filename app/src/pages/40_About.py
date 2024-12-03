import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks(show_home=True)

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
