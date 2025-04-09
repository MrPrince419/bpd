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
from datetime import datetime
from utils.calendarific import get_holidays
from utils import get_ip_info, fetch_ip_info
import pycountry
import emoji
from ipinfo_tools import get_location_info

def settings_page():
    st.title("⚙️ Settings")
    st.sidebar.markdown("### Settings")

    # Show current IP info
    ipinfo = st.session_state.get("ipinfo", {})
    st.write("### Current IP Information")
    st.json(ipinfo)

    # Country and currency settings
    countries = [country.name for country in pycountry.countries]
    selected_country = st.selectbox("Select Country", options=countries)
    st.session_state["country"] = selected_country

    currencies = ["USD", "EUR", "GBP", "JPY", "NGN"]
    selected_currency = st.selectbox("Select Currency", options=currencies)
    st.session_state["currency"] = selected_currency

    year = st.number_input("Select Year", min_value=2000, max_value=2100, value=2023)
    if st.button("Fetch Holidays"):
        holidays = get_holidays(selected_country, year)
        st.table(holidays)

    if st.button("Save Settings"):
        st.success("✅ Settings saved!")
