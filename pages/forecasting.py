import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

def forecasting_page():
    st.title("🔮 Forecasting - Business Trend Prediction")

    if "uploaded_data" not in st.session_state or st.session_state.uploaded_data is None:
        st.warning("⚠️ Please upload your dataset on the Home page first.")
        return

    data = st.session_state.uploaded_data.copy()

    st.sidebar.header("📅 Forecast Settings")
    date_col = st.sidebar.selectbox("Select Date Column", options=data.columns)
    revenue_col = st.sidebar.selectbox("Select Revenue Column", options=data.columns)

    # Convert and clean the selected columns
    try:
        data[date_col] = pd.to_datetime(data[date_col], errors="coerce")
        data[revenue_col] = pd.to_numeric(data[revenue_col], errors="coerce")
        data = data.dropna(subset=[date_col, revenue_col])
    except Exception as e:
        st.error(f"❌ Error processing columns: {e}")
        return

    if data.empty:
        st.error("❌ No valid data available after cleaning. Please check the column selections.")
        return

    df = data[[date_col, revenue_col]].copy()
    df.columns = ["ds", "y"]

    if len(df) < 2:
        st.error("❌ Not enough data to build forecast. Need at least 2 rows.")
        return

    periods = st.sidebar.slider("📆 Months to Forecast", min_value=1, max_value=24, value=6)

    try:
        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(periods=periods, freq="M")
        forecast = model.predict(future)

        st.subheader("📈 Forecasted Revenue")
        fig1 = model.plot(forecast)
        st.pyplot(fig1)

        st.subheader("🧠 Forecast Components")
        fig2 = model.plot_components(forecast)
        st.pyplot(fig2)

        st.subheader("📊 Forecasted Data Preview")
        st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods))

    except Exception as e:
        st.error(f"❌ Forecasting failed: {e}")
