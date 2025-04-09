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
from pages.home import home_page
from pages.dashboard import dashboard_page
from pages.forecasting import forecasting_page
from pages.ml_insights import ml_insights_page
from pages.export import export_page
from pages.settings import settings_page
from ipinfo_tools import get_location_info

st.set_page_config(page_title="Smart Insights", page_icon="📊", layout="wide")

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
