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
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from utils import convert_currency  # Import currency conversion utility

st.set_page_config(page_title="Forecasting", page_icon="📉")

def forecasting_page():
    st.title("🔮 Forecasting - Business Trend Prediction")
    st.sidebar.markdown("### Forecasting Tools")

    if "uploaded_data" not in st.session_state or st.session_state["uploaded_data"] is None:
        st.warning("⚠️ Please upload a dataset on the Home page.")
        st.stop()

    try:
        data = st.session_state["uploaded_data"].copy()

        date_col = st.selectbox("Select Date Column", options=data.columns)
        revenue_col = st.selectbox("Select Revenue Column", options=data.columns)

        try:
            data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
            data[revenue_col] = pd.to_numeric(data[revenue_col], errors="coerce")
            data = data.dropna(subset=[date_col, revenue_col])
        except Exception as e:
            st.error(f"Error processing columns: {e}")
            st.stop()

        if data.empty:
            st.error("❌ No valid data available after cleaning. Please check the column selections.")
            return

        aggregated_data = data.groupby(date_col).sum()
        st.line_chart(aggregated_data[revenue_col])

        df = data[[date_col, revenue_col]].copy()
        df.columns = ["ds", "y"]

        if len(df) < 2:
            st.error("❌ Not enough data to build forecast. Need at least 2 rows.")
            return

        periods = st.sidebar.slider("📆 Months to Forecast", min_value=1, max_value=24, value=6)

        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(periods=periods, freq="M")
        forecast = model.predict(future)

        # Convert forecasted revenue to selected currency
        currency = st.session_state.get("currency", "USD")
        forecast["yhat"] = forecast["yhat"].apply(lambda x: convert_currency(x, currency))
        forecast["yhat_lower"] = forecast["yhat_lower"].apply(lambda x: convert_currency(x, currency))
        forecast["yhat_upper"] = forecast["yhat_upper"].apply(lambda x: convert_currency(x, currency))

        st.subheader(f"📈 Forecasted Revenue ({currency})")
        fig1 = model.plot(forecast)
        st.pyplot(fig1)

        st.subheader("🧠 Forecast Components")
        fig2 = model.plot_components(forecast)
        st.pyplot(fig2)

        st.subheader(f"📊 Forecasted Data Preview ({currency})")
        st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods))
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
