import streamlit as st
import requests

def get_location_info():
    ipinfo_token = st.secrets["IPINFO_API_KEY"]
    url = f"https://ipinfo.io/json?token={ipinfo_token}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "ip": data.get("ip"),
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country"),
                "loc": data.get("loc"),
                "org": data.get("org"),
                "timezone": data.get("timezone"),
                "flag_url": f"https://flagsapi.com/{data.get('country')}/flat/64.png"
            }
        else:
            st.warning("Failed to fetch location data.")
            return None
    except Exception as e:
        st.error(f"IP info error: {e}")
        return None
