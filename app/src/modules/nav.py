# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/40_About.py", label="About", icon="🧠")


#### ------------------------ Roles of Coop Searcher ------------------------
def PolStratAdvHomeNav():
    st.sidebar.page_link(
        "pages/00_Coop_Searcher_Home.py", label="Coop Searcher Home", icon="👤"
    )


def ViewCoopsNav():
    st.sidebar.page_link(
        "pages/01_View_Coops.py", label="View Coops", icon="🏦"
    )


def ViewCompaniesNav():
    st.sidebar.page_link(
        "pages/02_View_Companies.py", label="View Companies", icon="🗺️"
    )


def ViewPostingsNav():
    st.sidebar.page_link(
        "pages/03_View_Job_Postings.py", label="View Job Postings", icon="🗺️"
    )


## ------------------------ Roles of coop reviewer ------------------------
def ReviewerHomeNav():
    st.sidebar.page_link(
        "pages/10_Coop_Reviewer_Home.py", label="Reviewer Home", icon="🏠"
    )

def CoopReviewNav():
    st.sidebar.page_link("pages/11_Coop_Review.py", label="Review Coops", icon="🛜")


def CompanyReviewNav():
    st.sidebar.page_link(
        "pages/12_Company_Review.py", label="Review Companies", icon="📈"
    )

## ------------------------ Roles of faculty coop advisor ---------------------
def FacultyHomeNav():
    st.sidebar.page_link(
        "pages/30_Faculty_Home.py", label="Faculty Home", icon="🏠"
    )

def StudentDataNav():
    st.sidebar.page_link(
        "pages/31_Student_Data.py", label="View Student Data", icon="🏠"
    )

def CoopDataNav():
    st.sidebar.page_link(
        "pages/32_Coop_Data.py", label="View Coop Data", icon="🏠"
    )
#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link(
        "pages/20_Admin_Home.py", label="System Admin", icon="🖥️"
    )
    st.sidebar.page_link(
        "pages/21_Coop_Review_Mgmt.py", label="Coop Review Management", icon="🏢"
    )
    st.sidebar.page_link(
        "pages/22_Company_Review_Mgmt.py", label="Company Review Management", icon="🏢"
    )
    st.sidebar.page_link(
        "pages/23_Job_Posting_Mgmt.py", label="Job Posting Management", icon="🏢"
    )


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """
    # add a logo to the sidebar always
    st.sidebar.image('static/logo.png', width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "coop_searcher":
            PolStratAdvHomeNav()
            ViewCoopsNav()
            ViewCompaniesNav()
            ViewPostingsNav()

        # If the user role is reviewer, show the Api Testing page
        if st.session_state["role"] == "reviewer":
            ReviewerHomeNav()
            CoopReviewNav()
            ViewCoopsNav()
            CompanyReviewNav()

        if st.session_state["role"] == "faculty":
            FacultyHomeNav()
            StudentDataNav()
            CoopDataNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
