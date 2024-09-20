
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlalchemy

# Session state for collaborative purposes
if 'data' not in st.session_state:
    st.session_state['data'] = None

# Title of the Streamlit App
st.title("Advanced Streamlit App with Dynamic Dashboards")

# Sidebar for Data Integration and Transformations
st.sidebar.header("Data Source & Options")

# Database Integration
def connect_to_database(db_url, query):
    engine = sqlalchemy.create_engine(db_url)
    with engine.connect() as connection:
        return pd.read_sql_query(query, connection)

# Data Export
def export_data(data, export_format):
    if export_format == 'CSV':
        return data.to_csv(index=False)
    elif export_format == 'Excel':
        return data.to_excel("exported_data.xlsx", index=False)

# Simulated ETL Process
def simulated_etl():
    return {"status": "Simulated ETL process complete"}

etl_sync = st.sidebar.button("Run Simulated ETL")
if etl_sync:
    etl_status = simulated_etl()
    st.write(etl_status)

# Data Source Selection
data_source = st.sidebar.selectbox("Select Data Source", ["Upload CSV", "SQL Database"])

# Handling different data sources
if data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        st.session_state['data'] = pd.read_csv(uploaded_file)

elif data_source == "SQL Database":
    db_url = st.sidebar.text_input("Database URL")
    query = st.sidebar.text_area("SQL Query")
    if db_url and query:
        st.session_state['data'] = connect_to_database(db_url, query)

# If data is loaded, proceed with analysis and transformations
if st.session_state['data'] is not None:
    st.write("### Data Preview")
    st.dataframe(st.session_state['data'].head())

    # Show Summary Statistics
    st.write("### Summary Statistics")
    st.write(st.session_state['data'].describe())

    # Pivot Table and Grouping
    st.write("### Pivot Table and Grouping")
    group_by_column = st.selectbox("Select Column to Group By", st.session_state['data'].columns)
    aggregation_method = st.selectbox("Aggregation Method", ["sum", "mean", "count"])
    
    if aggregation_method == "sum":
        pivot_table = st.session_state['data'].groupby(group_by_column).sum()
    elif aggregation_method == "mean":
        pivot_table = st.session_state['data'].groupby(group_by_column).mean()
    else:
        pivot_table = st.session_state['data'].groupby(group_by_column).count()
        
    st.write("### Pivot Table")
    st.dataframe(pivot_table)

    # Correlation Heatmap
    st.write("### Correlation Heatmap")
    corr = st.session_state['data'].corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Matrix")
    st.plotly_chart(fig)

    # Dynamic Scatter Plot
    st.write("### Scatter Plot")
    x_column = st.selectbox("Select X-axis", st.session_state['data'].columns)
    y_column = st.selectbox("Select Y-axis", st.session_state['data'].columns)
    if st.button("Generate Scatter Plot"):
        fig = px.scatter(st.session_state['data'], x=x_column, y=y_column, title=f"Scatter Plot of {x_column} vs {y_column}")
        st.plotly_chart(fig)

    # Export Data
    st.write("### Export Data")
    export_format = st.selectbox("Select Export Format", ["CSV", "Excel"])
    if st.button("Export Data"):
        export_data(st.session_state['data'], export_format)
        st.write(f"Data exported successfully as {export_format}.")
else:
    st.write("Please select or upload a data source.")
