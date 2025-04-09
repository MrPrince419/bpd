import streamlit as st
st.set_page_config(page_title="Smart Insights", page_icon="📊", layout="wide")

from pages.home import home_page
from pages.dashboard import dashboard_page
from pages.forecasting import forecasting_page
from pages.ml_insights import ml_insights_page
from pages.export import export_page
from pages.settings import settings_page
from ipinfo_tools import get_location_info

# Initialize session state
if "uploaded_data" not in st.session_state:
    st.session_state["uploaded_data"] = None
if "currency" not in st.session_state:
    st.session_state["currency"] = "USD"
if "country" not in st.session_state:
    st.session_state["country"] = "United States"
if "ipinfo" not in st.session_state:
    st.session_state["ipinfo"] = get_location_info()

# Sidebar setup
st.sidebar.title("Smart Insights")
st.sidebar.markdown("Helping small businesses make data-driven decisions.")
st.sidebar.info(f"🌍 {st.session_state.get('ipinfo', {}).get('country', 'Unknown')}, {st.session_state.get('ipinfo', {}).get('city', 'Unknown')}")
st.sidebar.markdown("---")
st.sidebar.markdown("**Version 1.0** | © 2025 Smart Insights")

# Sidebar navigation
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Dashboard", "Forecasting", "ML Insights", "Export", "Settings"],
    index=0
)

# Page routing
if page == "Home":
    home_page()
elif page == "Dashboard":
    dashboard_page()
elif page == "Forecasting":
    forecasting_page()
elif page == "ML Insights":
    ml_insights_page()
elif page == "Export":
    export_page()
elif page == "Settings":
    settings_page()
