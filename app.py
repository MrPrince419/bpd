import streamlit as st
from pages.home import home_page
from pages.dashboard import dashboard_page
from pages.forecasting import forecasting_page
from pages.ml_insights import ml_insights_page
from pages.export import export_page
from pages.settings import settings_page

# Set wide layout
st.set_page_config(page_title="Business Performance Dashboard", layout="wide")

# Sidebar Navigation
st.sidebar.title("📊 Business Dashboard")
page = st.sidebar.radio("Go to", [
    "🏠 Home",
    "📈 Dashboard",
    "🔮 Forecasting",
    "🤖 ML Insights",
    "📤 Export",
    "⚙️ Settings"
])

# Load the selected page
if page == "🏠 Home":
    home_page()
elif page == "📈 Dashboard":
    dashboard_page()
elif page == "🔮 Forecasting":
    forecasting_page()
elif page == "🤖 ML Insights":
    ml_insights_page()
elif page == "📤 Export":
    export_page()
elif page == "⚙️ Settings":
    settings_page()
