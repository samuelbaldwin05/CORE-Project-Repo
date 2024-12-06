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
        "pages/00_Coop_Searcher_Home.py", label="Coop Searcher Home", icon="🏠"
    )


def ViewCoopsNav():
    st.sidebar.page_link(
        "pages/01_Search_By_Position.py", label="Search Co-ops By Position", icon="📋"
    )


def ViewCompaniesNav():
    st.sidebar.page_link(
        "pages/02_Search_By_Company.py", label="Search Co-ops By Company", icon="🏢"
    )


def ViewPostingsNav():
    st.sidebar.page_link(
        "pages/03_View_Job_Postings.py", label="View Job Postings", icon="📄"
    )

## ------------------------ Roles of Coop Reviewer ------------------------
def ReviewerHomeNav():
    st.sidebar.page_link(
        "pages/10_Coop_Reviewer_Home.py", label="Reviewer Home", icon="🏠"
    )

def CoopReviewNav():
    st.sidebar.page_link("pages/11_Coop_Review.py", label="Review Coops", icon="📝")


def CompanyReviewNav():
    st.sidebar.page_link(
        "pages/12_Company_Review.py", label="Review Companies", icon="📊"
    )

## ------------------------ Roles of Faculty Coop Advisor ---------------------
def FacultyHomeNav():
    st.sidebar.page_link(
        "pages/30_Faculty_Home.py", label="Faculty Home", icon="🏠"
    )

def StudentDataNav():
    st.sidebar.page_link(
        "pages/31_Student_Data.py", label="View Student Data", icon="👨‍🎓"
    )

def StudentInfoNav():
    st.sidebar.page_link(
        "pages/32_View_Student_Info.py", label="View Student Info", icon="📊"
    )

def AlterStudentDataNav():
    st.sidebar.page_link(
        "pages/33_Alter_Students.py", label="Alter Student Data", icon="✏️"
    )

#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link(
        "pages/20_Admin_Home.py", label="System Admin", icon="🛠️"
    )
    st.sidebar.page_link(
        "pages/21_Delete_Data.py", label="Delete Incorrect Data", icon="🗑️"
    )
    st.sidebar.page_link(
        "pages/22_Change_Company_Info.py", label="Change Company Info", icon="🏢"
    )
    st.sidebar.page_link(
        "pages/23_Job_Posting_Mgmt.py", label="Job Posting Management", icon="🗂️"
    )



# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    st.sidebar.image("static/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Sidebar links for coop searcher role
        if st.session_state["role"] == "coop_searcher":
            PolStratAdvHomeNav()
            ViewCoopsNav()
            ViewCompaniesNav()
            ViewPostingsNav()

        # Sidebars for reviewer role
        if st.session_state["role"] == "reviewer":
            ReviewerHomeNav()
            CoopReviewNav()
            CompanyReviewNav()
            ViewCoopsNav()
            ViewCompaniesNav()

        # Sidebar links for faculty role
        if st.session_state["role"] == "faculty":
            FacultyHomeNav()
            StudentDataNav()
            AlterStudentDataNav()
            ViewPostingsNav()
            StudentInfoNav()

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
