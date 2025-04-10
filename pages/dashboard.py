# GitHub Copilot Prompt:
# This app is a Streamlit-based data analytics dashboard called Smart Insights.
# Ensure the following logic is preserved across all pages:
# 1. Only the Home page allows users to upload, add, or remove datasets.
# 2. Once a dataset is uploaded, it is stored in st.session_state["uploaded_data"] and must be persistently accessible across all pages.
# 3. All other pages (Dashboard, Forecasting, ML Insights, Export, Settings) must use this session data without asking the user to upload again.
# 4. If "uploaded_data" is not found in the session state, pages should show a friendly warning and stop.
# 5. Currency and country selections (for conversion or API use) are stored in st.session_state["currency"] and st.session_state["country"], and should be respected globally.
# 6. IP location data is retrieved once and stored in st.session_state["ipinfo"] for sidebar display and optional logic.
# 7. Do not use st.set_page_config() anywhere except the root app.py file.
# 8. All data manipulation must be robust: handle nulls, invalid formats, and incorrect column selections with clear error messages.
# 9. Forecasting and ML models must not break if the dataset is small, empty, or mismatched — always validate input first.
# 10. Export page must allow exporting the current session dataset and computed outputs.
# 11. All API integrations (currency, holidays, IPInfo) must be non-blocking, handle errors gracefully, and cache where possible.
# 12. Sidebar must remain consistent across all pages — include branding, user location, and a working navigation menu.
# 13. Optimize for clarity, user experience, and no repeated uploads or broken logic. Each page should load and function independently but share session state.

import streamlit as st
st.set_page_config(page_title="Dashboard", page_icon="📊")

import pandas as pd
import matplotlib.pyplot as plt
from utils import convert_currency

def dashboard_page():
    st.title("📊 Dashboard - Business KPIs Overview")
    st.sidebar.markdown("### Dashboard Tools")

    # Validate dataset availability
    if "uploaded_data" not in st.session_state or st.session_state["uploaded_data"] is None:
        st.warning("Please upload a dataset on the Home page to proceed.")
        st.stop()

    data = st.session_state["uploaded_data"]
    currency = st.session_state.get("currency", "USD")

    # Validate selected columns
    date_col = st.selectbox("Select Date Column", options=data.columns)
    revenue_col = st.selectbox("Select Revenue Column", options=data.columns)

    try:
        data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
        data[revenue_col] = pd.to_numeric(data[revenue_col], errors="coerce")
        filtered_data = data.dropna(subset=[date_col, revenue_col])
        if filtered_data.empty:
            st.warning("No valid data after filtering. Check your column selection.")
            st.stop()
    except Exception as e:
        st.error(f"Error processing columns: {e}")
        st.stop()

    st.dataframe(filtered_data)

    # Display KPIs
    st.write("### Key Performance Indicators")
    st.metric("Total Rows", len(filtered_data))
    st.metric("Total Columns", len(filtered_data.columns))

    # Suggest default columns based on patterns
    date_col_default = next((col for col in filtered_data.columns if "date" in col.lower() or "time" in col.lower()), None)
    revenue_col_default = next((col for col in filtered_data.columns if "revenue" in col.lower() or "amount" in col.lower()), None)

    st.sidebar.header("📅 Select Columns")
    date_col = st.sidebar.selectbox("Select Date Column", options=filtered_data.columns, index=filtered_data.columns.get_loc(date_col_default) if date_col_default else 0)
    revenue_col = st.sidebar.selectbox("Select Revenue Column", options=filtered_data.columns, index=filtered_data.columns.get_loc(revenue_col_default) if revenue_col_default else 0)

    try:
        filtered_data[date_col] = pd.to_datetime(filtered_data[date_col], errors="coerce")
        filtered_data = filtered_data.dropna(subset=[date_col, revenue_col])
        if filtered_data.empty:
            st.warning("No valid data after filtering. Check your column selection.")
            return
        st.success("Data loaded successfully!")
    except Exception as e:
        st.error(f"Error processing data: {e}")
        return

    st.subheader("📌 Key Metrics")
    try:
        total_revenue = pd.to_numeric(filtered_data[revenue_col], errors="coerce").sum()
        avg_revenue = pd.to_numeric(filtered_data[revenue_col], errors="coerce").mean()

        try:
            total_revenue_converted = convert_currency(total_revenue, currency)
            avg_revenue_converted = convert_currency(avg_revenue, currency)
        except Exception as e:
            st.error(f"Error converting currency: {e}")
            return

        col1, col2 = st.columns(2)
        col1.metric("💰 Total Revenue", f"{total_revenue_converted:,.2f} {currency}")
        col2.metric("📊 Average Revenue", f"{avg_revenue_converted:,.2f} {currency}")
    except Exception as e:
        st.error(f"❌ KPI Calculation Error: {e}")
        return

    st.subheader("📆 Monthly Revenue Overview")
    try:
        monthly_data = filtered_data.groupby(filtered_data[date_col].dt.to_period("M"))[revenue_col].sum()
        monthly_data.index = monthly_data.index.to_timestamp()

        fig, ax = plt.subplots()
        monthly_data.plot(kind="bar", ax=ax)
        ax.set_title("Monthly Revenue")
        ax.set_xlabel("Month")
        ax.set_ylabel("Revenue")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"❌ Revenue chart error: {e}")
