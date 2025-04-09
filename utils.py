import requests
import streamlit as st
import pandas as pd
from functools import lru_cache

@st.cache_data
def fetch_ip_info():
    """Fetch IP information using the IPInfo API."""
    try:
        token = st.secrets["ipinfo_token"]
        response = requests.get(f"https://ipinfo.io?token={token}")
        return response.json()
    except Exception as e:
        st.error(f"IPInfo API error: {e}")
        return {}

@st.cache_data
def get_holidays(country, year):
    """Fetch public holidays for a given country and year using Calendarific API."""
    try:
        api_key = st.secrets.get("CALENDARIFIC_API_KEY")
        response = requests.get(f"https://calendarific.com/api/v2/holidays?api_key={api_key}&country={country}&year={year}")
        return response.json().get("response", {}).get("holidays", [])
    except Exception as e:
        print(f"Calendarific API error: {e}")
        return []

@st.cache_data
def get_ip_info():
    try:
        token = st.secrets["ipinfo_token"]
        response = requests.get(f"https://ipinfo.io?token={token}")
        return response.json()
    except Exception as e:
        st.error(f"Error fetching IP info: {e}")
        return {}

def get_filtered_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with missing values."""
    df = df.copy()
    df.dropna(inplace=True)
    return df

def is_valid_dataset(df: pd.DataFrame) -> bool:
    """Check if uploaded data has the required structure."""
    return not df.empty and df.select_dtypes(include=["number", "datetime", "object"]).shape[1] >= 2

@st.cache_data
def convert_currency(value, to_currency):
    try:
        response = requests.get(f"https://api.exchangerate.host/convert?from=USD&to={to_currency}&amount={value}")
        return response.json().get("result", value)
    except Exception as e:
        st.error(f"Error converting currency: {e}")
        return value

def fetch_api_with_retry(url, headers=None, retries=3):
    """
    Attempts to call the given API URL up to `retries` times.
    Returns JSON response or None on failure.
    """
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if attempt == retries - 1:
                st.error(f"API call failed after {retries} attempts: {e}")
                return None
