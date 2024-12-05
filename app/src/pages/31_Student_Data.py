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
        url = f'http://api:4000/p/PositionReview/{position_id}'
    else:
        url = 'http://api:4000/p/PositionReview'
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data)
  # Dataframe to make graph easier
    #except requests.exceptions.RequestException as e:
       # logger.error(f"Error fetching data: {e}")
       # st.error("Failed to fetch data. Please check the server.")
       #return pd.DataFrame()  # Empty dataframe if error


# Input PositionID
st.header("Filter by Position or Leave Blank For All Positions")
position_id_input = st.text_input("Enter Position ID")

# Fetch data from API

position_id = int(position_id_input) if position_id_input.isdigit() else None
df = fetch_data(position_id)
st.write(df)

# Dropdown to select acceptance rate filter
graph = st.selectbox("Select Application Metric", ["Total Accepted", "Acceptance Rate", "Total Applied"])

# Create a column with just the year
df['year'] = df['AppliedDate'].dt.year

# Group by year and calculate the appropriate metric
if graph == "Total Accepted":
    # Group by year and count the number of accepted students
    df_filtered = df[df['Offer'] == 1]
    students_accepted_by_year = df_filtered.groupby('year').size()

    # Plot the number of accepted students per year
    st.subheader("Number of Accepted Students Per Year")
    fig, ax = plt.subplots()
    students_accepted_by_year.plot(kind='bar', ax=ax)
    ax.set_title("Total Accepted Students per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Accepted Students")
    st.pyplot(fig)

elif graph == "Acceptance Rate":
    # Group by year and calculate the total number of applicants and the number of accepted students
    total_applicants_by_year = df.groupby('year').size()
    accepted_by_year = df[df['Offer'] == 1].groupby('year').size()

    # Calculate the acceptance rate as the number of accepted students divided by the total applicants
    acceptance_rate_by_year = accepted_by_year / total_applicants_by_year

    # Plot the acceptance rate per year
    st.subheader("Acceptance Rate Per Year")
    fig2, ax2 = plt.subplots()
    acceptance_rate_by_year.plot(kind='line', marker='o', ax=ax2)
    ax2.set_title("Acceptance Rate per Year")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Acceptance Rate (%)")
    ax2.set_ylim(0, 1)  # Acceptance rate is between 0 and 1
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y * 100:.2f}%'))  # Format y-axis as percentage
    st.pyplot(fig2)


elif graph == "Total Applied":
    # Group by year and count the total number of students applied
    total_applied_by_year = df_filtered.groupby('year').size()

    # Plot the total number of students applied per year
    st.subheader("Total Applied Students Per Year")
    fig3, ax3 = plt.subplots()
    total_applied_by_year.plot(kind='line', marker='o', ax=ax3)
    ax3.set_title("Total Applied Students per Year")
    ax3.set_xlabel("Year")
    ax3.set_ylabel("Total Applied Students")
    st.pyplot(fig3)

else: 
    st.write("Choose one of the drop down options")