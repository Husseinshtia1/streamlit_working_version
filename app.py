
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Title of the Streamlit App
st.title("Fully Functional Streamlit App")

# Sidebar: Simulated ETL and Data Processing Options
st.sidebar.header("Options")

# Simulated ETL Process
def simulated_etl():
    return {"status": "Simulated ETL process complete"}

etl_sync = st.sidebar.button("Run Simulated ETL")
if etl_sync:
    etl_status = simulated_etl()
    st.write(etl_status)

# File Upload for Data Analysis
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# If the user uploads a file, proceed with data analysis and visualization
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.dataframe(data.head())

    # Show Summary Statistics
    st.write("### Summary Statistics")
    st.write(data.describe())

    # Correlation Heatmap
    st.write("### Correlation Heatmap")
    corr = data.corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Matrix")
    st.plotly_chart(fig)

    # Scatter Plot
    st.write("### Scatter Plot")
    x_column = st.selectbox("Select X-axis", data.columns)
    y_column = st.selectbox("Select Y-axis", data.columns)
    if st.button("Generate Scatter Plot"):
        fig = px.scatter(data, x=x_column, y=y_column, title=f"Scatter Plot of {x_column} vs {y_column}")
        st.plotly_chart(fig)

    # Histogram
    st.write("### Histogram")
    hist_column = st.selectbox("Select Column for Histogram", data.columns)
    if st.button("Generate Histogram"):
        fig = px.histogram(data, x=hist_column, nbins=20, title=f"Histogram of {hist_column}")
        st.plotly_chart(fig)
else:
    st.write("Please upload a CSV file for analysis.")
