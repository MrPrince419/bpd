import requests
import streamlit as st
import pandas as pd  # Add this line to import pandas

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

def get_ip_info():
    """
    Fetch IP information using the IPInfo API.
    Returns a dictionary with relevant fields or fallback values.
    """
    try:
        data = fetch_ip_info()
        return {
            "ip": data.get("ip", "Unknown"),
            "city": data.get("city", "Unknown"),
            "region": data.get("region", "Unknown"),
            "country": data.get("country", "US"),
            "loc": data.get("loc", "0,0"),
            "timezone": data.get("timezone", "Unknown"),
        }
    except Exception as e:
        st.error(f"Failed to fetch IP info: {e}")
        return {
            "ip": "Unknown",
            "city": "Unknown",
            "region": "Unknown",
            "country": "US",
            "loc": "0,0",
            "timezone": "Unknown",
        }

def get_filtered_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with missing values."""
    df = df.copy()
    df.dropna(inplace=True)
    return df

def is_valid_dataset(df: pd.DataFrame) -> bool:
    """Check if uploaded data has the required structure."""
    return not df.empty and df.select_dtypes(include=["number", "datetime", "object"]).shape[1] >= 2

@st.cache_data
def convert_currency(value: float, to_currency: str) -> float:
    try:
        if "currency_rate" not in st.session_state or st.session_state.get("currency") != to_currency:
            response = requests.get(f"https://api.exchangerate.host/latest?base=USD&symbols={to_currency}")
            rate = response.json()["rates"].get(to_currency, 1.0)
            st.session_state["currency_rate"] = rate
            st.session_state["currency"] = to_currency
        return value * st.session_state["currency_rate"]
    except Exception as e:
        st.error(f"Currency conversion failed: {e}")
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
