import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

def forecasting_page():
    st.title("📈 Revenue Forecasting")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is None:
        st.info("Please upload a CSV file to see forecasting.")
        return

    try:
        data = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return

    # Sidebar config
    st.sidebar.header("Column Configuration")
    date_col = st.sidebar.selectbox("Select Date Column", options=data.columns)
    revenue_col = st.sidebar.selectbox("Select Revenue Column", options=data.columns)

    # Convert date column
    data[date_col] = pd.to_datetime(data[date_col], errors='coerce')
    data = data.dropna(subset=[date_col, revenue_col])

    if data.empty:
        st.warning("No valid data after cleaning. Please check your file.")
        return

    # Prepare data for Prophet
    df = data[[date_col, revenue_col]].copy()
    df.columns = ["ds", "y"]

    try:
        df["y"] = pd.to_numeric(df["y"], errors="coerce")
        df = df.dropna()
        df = df.groupby("ds").sum().reset_index()
    except Exception as e:
        st.error(f"Error preparing data: {e}")
        return

    if len(df) < 2:
        st.warning("Not enough data for forecasting.")
        return

    # Forecasting
    st.subheader("📅 Forecast Configuration")
    periods = st.slider("Select number of future days to forecast", 7, 90, 30)

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    # Plotting
    st.subheader("🔮 Forecast Results")
    fig1 = model.plot(forecast)
    st.pyplot(fig1)

    st.subheader("📉 Forecast Components")
    fig2 = model.plot_components(forecast)
    st.pyplot(fig2)
