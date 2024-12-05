import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout = 'wide', page_title = 'Student Data', page_icon = 'static/core-4.png')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('View Student Data')

def fetch_data():
    url = 'http://api:4000/p/PositionReview'
    response = requests.get(url) 
    data = response.json()
    return pd.DataFrame(data)  # Dataframe to make graph easier

# Get df data
df = fetch_data()

# Dropdown to select acceptance rate filter
graph = st.selectbox("Select Metric", ["Total Accepted", "Acceptance Rate", "Total Applied"])

# Create a column with just the year
df["AppliedDate"] = pd.to_datetime(df["AppliedDate"], errors="coerce")
df['year'] = df['AppliedDate'].dt.year

# Group by year and calculate the appropriate metric
if graph == "Total Accepted":
    # Group by year and count the number of accepted students
    df_filtered = df[df['Offer'] == 1]
    students_accepted_by_year = df_filtered.groupby('year').size()

    # Plot the number of accepted students per year
    st.subheader("Number of Accepted Students Per Year")
    students_accepted_by_year.plot(kind='line', marker='o')
    plt.xticks(students_accepted_by_year.index)
    plt.title("Total Accepted Students per Year")
    plt.ylabel("Year")
    plt.xlabel("Total Accepted Students")
    st.pyplot(plt.gcf())
    plt.clf()

elif graph == "Acceptance Rate":
    # Group by year and calculate the total number of applicants and the number of accepted students
    total_applicants_by_year = df.groupby('year').size()
    accepted_by_year = df[df['Offer'] == 1].groupby('year').size()

    # Calculate the acceptance rate as the number of accepted students divided by the total applicants
    acceptance_rate_by_year = accepted_by_year / total_applicants_by_year

    # Plot the acceptance rate per year
    st.subheader("Acceptance Rate Per Year")
    acceptance_rate_by_year.plot(kind='line', marker='o')
    plt.xticks(acceptance_rate_by_year.index)
    plt.title("Acceptance Rate per Year")
    plt.xlabel("Year")
    plt.ylabel("Acceptance Rate (%)")
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y * 100:.2f}%'))
    st.pyplot(plt.gcf())
    plt.clf()


elif graph == "Total Applied":
    # Group by year and count the total number of students applied
    total_applied_by_year = df.groupby('year').size()

    # Plot the total number of students applied per year
    st.subheader("Total Applied Students Per Year")

    total_applied_by_year.plot(kind='line', marker='o')
    plt.xticks(total_applied_by_year.index)
    plt.title("Total Applied Students per Year")
    plt.xlabel("Year")
    plt.ylabel("Total Applied Students")
    st.pyplot(plt.gcf())
    plt.clf()

else: 
    st.write("Choose one of the drop down options")