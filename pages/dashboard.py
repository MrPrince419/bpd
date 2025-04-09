import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def dashboard_page():
    st.title("📊 Dashboard - Business KPIs Overview")

    # Check if data exists from Home page
    if "uploaded_data" not in st.session_state or st.session_state.uploaded_data is None:
        st.warning("⚠️ Please upload your dataset from the Home page.")
        return

    data = st.session_state.uploaded_data.copy()

    st.sidebar.header("📅 Select Columns")
    date_col = st.sidebar.selectbox("Select Date Column", options=data.columns)
    revenue_col = st.sidebar.selectbox("Select Revenue Column", options=data.columns)

    try:
        data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
    except Exception as e:
        st.error(f"❌ Date column conversion error: {e}")
        return

    data = data.dropna(subset=[date_col, revenue_col])
    if data.empty:
        st.error("❌ No valid data after filtering. Check your column selection.")
        return

    # Filter by date range
    min_date = data[date_col].min()
    max_date = data[date_col].max()

    date_range = st.sidebar.date_input("Filter Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    if len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        data = data[(data[date_col] >= start_date) & (data[date_col] <= end_date)]

    st.subheader("📌 Key Metrics")

    try:
        current_month = pd.Timestamp.today().month
        this_month_data = data[data[date_col].dt.month == current_month]

        current_revenue = pd.to_numeric(this_month_data[revenue_col], errors="coerce").sum()
        total_revenue = pd.to_numeric(data[revenue_col], errors="coerce").sum()
        avg_revenue = pd.to_numeric(data[revenue_col], errors="coerce").mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("📈 Current Month Revenue", f"${current_revenue:,.2f}")
        col2.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
        col3.metric("📊 Average Revenue", f"${avg_revenue:,.2f}")
    except Exception as e:
        st.error(f"❌ KPI Calculation Error: {e}")
        return

    # Monthly Revenue Chart
    st.subheader("📆 Monthly Revenue Overview")
    try:
        monthly_data = data.groupby(data[date_col].dt.to_period("M"))[revenue_col].sum()
        monthly_data.index = monthly_data.index.to_timestamp()

        fig, ax = plt.subplots()
        monthly_data.plot(kind="bar", ax=ax)
        ax.set_title("Monthly Revenue")
        ax.set_xlabel("Month")
        ax.set_ylabel("Revenue")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"❌ Revenue chart error: {e}")
