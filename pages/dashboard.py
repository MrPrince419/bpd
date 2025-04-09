import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_filtered_data  # Updated import

def dashboard_page():
    st.title("📊 Business Dashboard")

    if 'data' not in st.session_state:
        st.warning("Please upload data in the Home page.")
        return

    data = st.session_state['data']
    data = get_filtered_data(data)

    st.sidebar.subheader("Column Configuration")
    date_col = st.sidebar.selectbox("Select Date Column", options=data.columns)
    revenue_col = st.sidebar.selectbox("Select Revenue Column", options=data.columns)

    try:
        data[date_col] = pd.to_datetime(data[date_col], errors='coerce')
    except Exception as e:
        st.error(f"Error converting {date_col} to datetime: {e}")
        return

    if data[date_col].isna().all():
        st.error("No valid dates found in the dataset.")
        return

    data = data.dropna(subset=[date_col])
    min_date = data[date_col].min()
    max_date = data[date_col].max()
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

    if len(date_range) != 2:
        st.warning("Please select a valid date range.")
        return

    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    current_data = data[(data[date_col] >= start_date) & (data[date_col] <= end_date)]

    if current_data.empty:
        st.warning("No data available for selected date range.")
        return

    if not pd.api.types.is_numeric_dtype(current_data[revenue_col]):
        st.error("Selected revenue column is not numeric.")
        return

    st.subheader("🔢 Key Metrics")
    current_sum = current_data[revenue_col].sum()
    avg_revenue = current_data[revenue_col].mean()
    st.metric("Total Revenue", f"${current_sum:,.2f}")
    st.metric("Average Revenue", f"${avg_revenue:,.2f}")

    st.subheader("📈 Revenue Over Time")
    daily_revenue = current_data.groupby(current_data[date_col].dt.to_period("D"))[revenue_col].sum().reset_index()
    daily_revenue[date_col] = daily_revenue[date_col].dt.to_timestamp()
    fig = px.line(daily_revenue, x=date_col, y=revenue_col, labels={revenue_col: "Revenue"})
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 View Filtered Data"):
        st.dataframe(current_data)
