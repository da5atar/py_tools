'''
dataset_generator.py
This script generates random test data based on the selected columns and number of rows.
The user can select the columns to generate data for and specify the number of rows to generate.

To run the script, simply execute it. The user can select the columns and number of rows in the
 sidebar and click the "Generate Data" button to generate the random test data.

You can customize the script by adding more data generators to the 'generators'
 dictionary and modifying the data generation settings.

Note: You need to install the 'streamlit' and 'mimesis' libraries to run this script.
'''

import streamlit as st
import pandas as pd
from mimesis import Person, Address
from mimesis.enums import Gender
from io import StringIO

# Dictionary of available data generators
generators = {
    "Name": lambda: person.full_name(),
    "Email": lambda: person.email(),
    "Address": lambda: address.address(),
    "Phone Number": lambda: person.telephone(),
    "Job": lambda: person.occupation(),
}

# Function to generate data
def generate_data(columns, rows):
    data = {col: [generators[col]() for _ in range(rows)] for col in columns}
    return pd.DataFrame(data)

# Streamlit interface
st.title("Test Data Generator 📊")

# Sidebar for settings
st.sidebar.header("Data Generation Settings")
selected_columns = st.sidebar.multiselect("Select Columns:", list(generators.keys()))
num_rows = st.sidebar.number_input("Number of Rows:", min_value=1, max_value=1000, value=10)

if st.sidebar.button("Generate Data"):
    if selected_columns:
        person = Person()  # Initialize Mimesis Person provider
        address = Address()  # Initialize Mimesis Address provider
        df = generate_data(selected_columns, num_rows)

        st.write("### Generated Data")
        st.dataframe(df)

        # Convert DataFrame to CSV and create download link
        csv = df.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name="random_data.csv", mime="text/csv")
    else:
        st.warning("Please select at least one column.")
