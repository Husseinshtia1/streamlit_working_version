
import streamlit as st
import pandas as pd
import plotly.express as px

# Enable session state for collaborative purposes
if 'data' not in st.session_state:
    st.session_state['data'] = None

# Title of the Streamlit App
st.title("Sourcetable-Powered Streamlit App")

# Sidebar for Data Upload and ETL Simulation
st.sidebar.header("Upload Data & Options")

# Simulated ETL Process
def simulated_etl():
    return {"status": "Simulated ETL process complete"}

etl_sync = st.sidebar.button("Run Simulated ETL")
if etl_sync:
    etl_status = simulated_etl()
    st.write(etl_status)

# File Upload for Data Analysis
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# If the user uploads a file, proceed with data analysis and visualization
if uploaded_file is not None:
    st.session_state['data'] = pd.read_csv(uploaded_file)
    st.write("### Data Preview")
    st.dataframe(st.session_state['data'].head())

    # Show Summary Statistics
    st.write("### Summary Statistics")
    st.write(st.session_state['data'].describe())

    # Correlation Heatmap
    st.write("### Correlation Heatmap")
    corr = st.session_state['data'].corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Matrix")
    st.plotly_chart(fig)

    # Scatter Plot
    st.write("### Scatter Plot")
    x_column = st.selectbox("Select X-axis", st.session_state['data'].columns)
    y_column = st.selectbox("Select Y-axis", st.session_state['data'].columns)
    if st.button("Generate Scatter Plot"):
        fig = px.scatter(st.session_state['data'], x=x_column, y=y_column, title=f"Scatter Plot of {x_column} vs {y_column}")
        st.plotly_chart(fig)

    # Bar Chart
    st.write("### Bar Chart")
    bar_column = st.selectbox("Select Column for Bar Chart", st.session_state['data'].columns)
    if st.button("Generate Bar Chart"):
        fig = px.bar(st.session_state['data'], x=bar_column, title=f"Bar Chart of {bar_column}")
        st.plotly_chart(fig)

    # Export Data
    st.write("### Export Data")
    if st.button("Export Data as CSV"):
        st.session_state['data'].to_csv('exported_data.csv')
        st.write("Data exported successfully.")

else:
    st.write("Please upload a CSV file for analysis.")
