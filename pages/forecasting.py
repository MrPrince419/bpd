import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from utils import convert_currency  # Import currency conversion utility

def forecasting_page():
    st.title("🔮 Forecasting - Business Trend Prediction")
    st.sidebar.markdown("### Forecasting Tools")

    if "uploaded_data" not in st.session_state or st.session_state["uploaded_data"] is None:
        st.warning("Please upload a dataset on the Home page to proceed.")
        st.stop()

    try:
        data = st.session_state["uploaded_data"].copy()
        # Ensure data compatibility
        if "date" not in data.columns or "value" not in data.columns:
            st.error("The dataset must contain 'date' and 'value' columns for forecasting.")
            st.stop()

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
