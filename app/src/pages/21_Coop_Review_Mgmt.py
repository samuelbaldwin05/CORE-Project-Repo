import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide', page_title = 'User Management', page_icon = 'static/core-4.png')

SideBarLinks()

st.title('Coop Review Management')

# Route to all the reviews
def fetch_data():
    url = f'http://api:4000/p/PositionReview'
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    return pd.DataFrame(data)

# View all reviews in df
df = fetch_data()
col_order = ["prr.PosReviewID", "u.NUID", "Username", "Description", "AdvisorId"]
df = df[col_order]
rename_columns = {
    "prr.PosReviewID": "PosReviewID",
    "u.NUID": "NUID",
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
            url = f"http://api:4000/PositionReview/{review_id}"
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
