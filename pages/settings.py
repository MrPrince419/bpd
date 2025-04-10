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
        holidays = get_holidays(country=selected_country, year=year)
        if holidays.empty:
            st.warning("No holidays found for the selected country and year.")
        else:
            st.table(holidays)

    if st.button("Save Settings"):
        st.success("✅ Settings saved!")
