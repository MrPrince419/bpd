import streamlit as st
from pages.home import home_page
from pages.dashboard import dashboard_page
from pages.forecasting import forecasting_page
from pages.ml_insights import ml_insights_page
from pages.export import export_page
from pages.settings import settings_page

# Set Streamlit page config
st.set_page_config(
    page_title="Smart Insights",
    page_icon="📊",
    layout="wide"
)

# Initialize session state for uploaded data
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

# Sidebar header and navigation
st.sidebar.markdown("## 📊 Business Dashboard")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📈 Dashboard", "📉 Forecasting", "🤖 ML Insights", "📤 Export", "⚙️ Settings"]
)

# Route to pages
if page == "🏠 Home":
    home_page()
else:
    if st.session_state.uploaded_data is None:
        st.warning("Please upload your dataset from the Home page first.")
    else:
        if page == "📈 Dashboard":
            dashboard_page()
        elif page == "📉 Forecasting":
            forecasting_page()
        elif page == "🤖 ML Insights":
            ml_insights_page()
        elif page == "📤 Export":
            export_page()
        elif page == "⚙️ Settings":
            settings_page()
