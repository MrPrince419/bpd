import streamlit as st
import pandas as pd
from utils import get_ip_info

if "ipinfo" not in st.session_state:
    st.session_state["ipinfo"] = get_ip_info()

if "currency" not in st.session_state:
    st.session_state["currency"] = st.session_state["ipinfo"].get("currency", "USD")

if "uploaded_data" not in st.session_state:
    st.session_state["uploaded_data"] = None

def process_uploaded_file(uploaded_file):
    try:
        data = pd.read_csv(uploaded_file)
        if data.empty:
            st.error("The uploaded file is empty. Please upload a valid dataset.")
            return None
        return data
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

def home_page():
    st.title("🏠 Home")
    st.write("Welcome to Smart Insights!")
