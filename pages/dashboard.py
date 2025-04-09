import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def dashboard_page():
    st.title("📊 Business Dashboard")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is None:
        st.info("Please upload a CSV file to see the dashboard.")
        return

    try:
        data = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return

    # Column selectors
    st.sidebar.header("Column Configuration")
    date_col = st.sidebar.selectbox("Select Date Column", options=data.columns)
    revenue_col = st.sidebar.selectbox("Select Revenue Column", options=data.columns)

    # Convert date column
    data[date_col] = pd.to_datetime(data[date_col], errors='coerce')
    data = data.dropna(subset=[date_col, revenue_col])

    if data.empty:
        st.warning("Your dataset doesn't contain any valid date or revenue entries.")
        return

    # Filter by date range
    min_date, max_date = data[date_col].min(), data[date_col].max()
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date],
                                       min_value=min_date, max_value=max_date)

    if len(date_range) != 2:
        st.warning("Please select a valid start and end date.")
        return

    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_data = data[(data[date_col] >= start_date) & (data[date_col] <= end_date)]

    # Current and previous month comparison
    current_month = filtered_data[date_col].max().month
    previous_month = current_month - 1

    current_data = filtered_data[filtered_data[date_col].dt.month == current_month]
    previous_data = filtered_data[filtered_data[date_col].dt.month == previous_month]

    current_sum = current_data[revenue_col].sum()
    previous_sum = previous_data[revenue_col].sum()
    change = ((current_sum - previous_sum) / previous_sum * 100) if previous_sum else 0

    st.metric(label="📅 Current Month Revenue", value=f"${current_sum:,.2f}", delta=f"{change:.2f}%")

    # Line chart
    st.subheader("📉 Revenue Over Time")
    time_series = filtered_data.groupby(filtered_data[date_col].dt.to_period("M"))[revenue_col].sum()
    time_series.index = time_series.index.to_timestamp()
    st.line_chart(time_series)

    # Top 10 days
    st.subheader("🏆 Top 10 Revenue Days")
    top_days = filtered_data.groupby(data[date_col].dt.date)[revenue_col].sum().nlargest(10)
    st.bar_chart(top_days)

    # Revenue distribution
    st.subheader("📊 Revenue Distribution")
    fig, ax = plt.subplots()
    sns.histplot(filtered_data[revenue_col], kde=True, ax=ax)
    st.pyplot(fig)
