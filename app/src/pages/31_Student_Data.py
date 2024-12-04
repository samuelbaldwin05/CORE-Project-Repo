import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('View Student Data')

def fetch_data(position_id=None):
    if position_id:
        url = f'http://localhost:4000/PositionReview/{position_id}'  # Replace with your actual API base URL
    else:
        url = 'http://localhost:4000/PositionReview'  # Endpoint for all reviews

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx/5xx)
        data = response.json()
        return pd.DataFrame(data)  # Convert to DataFrame for easy manipulation
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        st.error("Failed to fetch data. Please check the server.")
        return pd.DataFrame()  # Return an empty DataFrame on error


# Input PositionID
st.sidebar.title("Filter by Position")
position_id_input = st.sidebar.text_input("Enter Position ID", value="1")  # Default to PositionID 1

# Fetch data from API
position_id = int(position_id_input) if position_id_input.isdigit() else None
df = fetch_data(position_id)

# Display the raw data for reference (optional)
st.subheader("Raw Data")
st.write(df)

# Dropdown to select acceptance rate filter
acceptance_rate = st.selectbox("Select Acceptance Rate", ["All", "Accepted", "Rejected"])

# Filter data based on dropdown
if acceptance_rate == "Accepted":
    df_filtered = df[df['accepted'] == True]
elif acceptance_rate == "Rejected":
    df_filtered = df[df['accepted'] == False]
else:
    df_filtered = df

# Group by year and count the number of students
students_by_year = df_filtered.groupby('year').size()

# Plot the number of students per year
st.subheader("Number of Students Per Year")
fig, ax = plt.subplots()
students_by_year.plot(kind='bar', ax=ax)
ax.set_title("Number of Students per Year")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Students")
st.pyplot(fig)

# Calculate acceptance rate by year
acceptance_rate_by_year = df_filtered.groupby('year')['accepted'].mean()

# Plot the acceptance rate per year
st.subheader("Acceptance Rate Per Year")
fig2, ax2 = plt.subplots()
acceptance_rate_by_year.plot(kind='line', marker='o', ax=ax2)
ax2.set_title("Acceptance Rate per Year")
ax2.set_xlabel("Year")
ax2.set_ylabel("Acceptance Rate")
st.pyplot(fig2)
