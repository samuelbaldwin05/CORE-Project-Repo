import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide', page_title = 'User Management', page_icon = 'static/core-4.png')

SideBarLinks()

# Routes to fetching data
def fetch_user_data():
        url = f'http://api:4000/u/users'
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        return pd.DataFrame(data)

def fetch_company_data():
        url = f'http://api:4000/c/Company'
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        return pd.DataFrame(data)

def fetch_jobposting_data():
        url = f'http://api:4000/j/JobPosting'
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        return pd.DataFrame(data)

def fetch_positionreview_data():
        url = f'http://api:4000/p/PositionReview'
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        return pd.DataFrame(data)

def fetch_companyreview_data():
        url = f'http://api:4000/c/CompanyReview'
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        return pd.DataFrame(data)



st.title('Delete Incorrect Or Malacious Entries')
delete_type = st.selectbox("Choose Entry Type", ["User",  "Company", "Job Posting", "Position Review", "Company Review"])

if delete_type == "User":
    df = fetch_user_data()
    col_order = ["NUID", "Username", "MajorID", "GPA", "AppCount", "OfferCount", "AdvisorId"]
    df = df[col_order]
    st.dataframe(df)
    st.subheader("Delete User")
    nuid = st.text_input("Enter the NUID to delete:")
    if st.button("Delete User"):
        if nuid.strip():
            try:
                url = f"http://api:4000/u/deleteusers/{nuid}"
                response = requests.delete(url)

                # Display response message
                if response.status_code == 200:
                    st.success(response.json().get("message", "User deleted successfully!"))
                else:
                    st.error(f"Failed to delete user. Error: {response.status_code}, {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid NUID.")

elif delete_type == "Company":
    df = fetch_company_data()
    st.dataframe(df)
    st.subheader("Delete Company")
    company_id = st.text_input("Enter the Company ID to delete:")
    
    if st.button("Delete Company"):
        if company_id.strip():
            try:
                url = f"http://api:4000/c/Company/{company_id}"
                response = requests.delete(url)

                # Display response message
                if response.status_code == 200:
                    st.success(response.json().get("message", "Company deleted successfully!"))
                else:
                    st.error(f"Failed to delete company. Error: {response.status_code}, {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid Company ID.")

elif delete_type == "Job Posting":
    # Get data
    df = fetch_jobposting_data()
    # Change column order
    col_order = ["PostingID", "CompanyID", "PositionID", "Status", "DatePosted"]
    df = df[col_order]
    # Show df
    st.dataframe(df)
    # Input for deleting
    st.subheader("Delete Job Posting")
    posting_id = st.text_input("Enter the Job Posting ID to delete:")

    # Delete route
    if st.button("Delete Job Posting"):
        if posting_id.strip():
            try:
                url = f"http://api:4000/j/JobPosting/{posting_id}"
                response = requests.delete(url)

                # Display response message
                if response.status_code == 200:
                    st.success(response.json().get("message", "Posting deleted successfully!"))
                else:
                    st.error(f"Failed to delete posting. Error: {response.status_code}, {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid Posting ID.")

elif delete_type == "Position Review":

    # View all reviews in df
    df = fetch_positionreview_data()
    col_order = ["prr.PosReviewID", "u.NUID", "Username", "Description", "ApplicationRating", 
                 "EnvironmentRating", "EducationRating", "EnjoymentRating"]
    df = df[col_order]
    rename_columns = {
        "prr.PosReviewID": "PosReviewID",
        "u.NUID": "NUID"
    }
    # Rename the columns
    df.rename(columns=rename_columns, inplace=True)
    st.dataframe(df)

    # Enter a review ID to delete review
    st.subheader("Delete Position Review")
    review_id = st.text_input("Enter the Position Review ID to delete:")

    if st.button("Delete Review"):
        if review_id.strip():
            try:
                url = f"http://api:4000/p/PositionReview/{review_id}"
                response = requests.delete(url)

                # Display response message
                if response.status_code == 200:
                    st.success(response.json().get("message", "Review deleted successfully!"))
                else:
                    st.error(f"Failed to delete review. Error: {response.status_code}, {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid Position Review ID.")

elif delete_type == "Company Review":

    # View all reviews in df
    df = fetch_companyreview_data()
    col_order = ["ComReviewID", "u.NUID", "Username", "Description", "EnvironmentRating", "CultureRating"]
    df = df[col_order]
    rename_columns = {"u.NUID": "NUID"}
    # Rename the columns
    df.rename(columns=rename_columns, inplace=True)
    st.dataframe(df)

    # Enter a review ID to delete review
    st.subheader("Delete Company Review")
    review_id = st.text_input("Enter the Company Review ID to delete:")

    if st.button("Delete Review"):
        if review_id.strip():
            try:
                url = f"http://api:4000/c/CompanyReview/{review_id}"
                response = requests.delete(url)

                # Display response message
                if response.status_code == 200:
                    st.success(response.json().get("message", "Review deleted successfully!"))
                else:
                    st.error(f"Failed to delete review. Error: {response.status_code}, {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid Company Review ID.")

else:
    st.write("Please select an entry option")