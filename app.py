import streamlit as st

# Show test markers to debug startup
st.write("📦 Starting app...")

# Imports (one per line)
st.write("📥 Importing pages...")
from pages.dashboard import dashboard_page
st.write("✅ dashboard imported")

from pages.home import home_page
st.write("✅ home imported")

from pages.forecasting import forecasting_page
st.write("✅ forecasting imported")

from pages.ml_insights import ml_insights_page
st.write("✅ ml_insights imported")

from pages.export import export_page
st.write("✅ export imported")

from pages.settings import settings_page
st.write("✅ settings imported")

from ipinfo_tools import get_location_info
st.write("✅ ipinfo_tools imported")

# Set config before anything else
st.set_page_config(page_title="Smart Insights", page_icon="📊")

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
st.sidebar.info(
    f"🌍 {st.session_state['ipinfo'].get('country', 'Unknown')}, "
    f"{st.session_state['ipinfo'].get('city', 'Unknown')}"
)
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

# Placeholder main page
st.title("Smart Insights App")
st.success("App loaded successfully ✅")
