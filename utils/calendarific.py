import requests
import pandas as pd
import streamlit as st
from datetime import datetime

def get_public_holidays(api_key: str, country: str, year: int):
    """Fetch public holidays for a given country and year using Calendarific API."""
    url = f"https://calendarific.com/api/v2/holidays?api_key={api_key}&country={country}&year={year}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            holidays = response.json().get("response", {}).get("holidays", [])
            return pd.DataFrame([{
                "name": h["name"],
                "date": h["date"]["iso"],
                "type": ", ".join(h["type"])
            } for h in holidays])
        else:
            return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

@st.cache_data
def get_holidays(country=None, year=None):
    """
    Fetch public holidays for a given country and year using the Calendarific API.
    """
    country = country or st.session_state["ipinfo"].get("country", "US")
    year = year or datetime.now().year
    api_key = st.secrets.get("CALENDARIFIC_API_KEY")
    if not api_key:
        st.error("Missing Calendarific API key in secrets.")
        return []

    url = "https://calendarific.com/api/v2/holidays"
    params = {"api_key": api_key, "country": country, "year": year}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("response", {}).get("holidays", [])
    else:
        st.error("Failed to fetch holidays.")
        return []
