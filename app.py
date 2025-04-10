import streamlit as st
from utils import get_ip_info

# Set page configuration
st.set_page_config(page_title="Smart Insights", page_icon="📊")

# Initialize session state
if "uploaded_data" not in st.session_state:
    st.session_state["uploaded_data"] = None
if "currency" not in st.session_state:
    st.session_state["currency"] = "USD"
if "country" not in st.session_state:
    st.session_state["country"] = "United States"
if "ipinfo" not in st.session_state:
    st.session_state["ipinfo"] = get_ip_info()

# Sidebar setup
st.sidebar.title("Smart Insights")
st.sidebar.markdown("Helping small businesses make data-driven decisions.")
st.sidebar.markdown("---")
st.sidebar.info(
    f"🌍 {st.session_state['ipinfo'].get('country', 'Unknown')}, "
    f"{st.session_state['ipinfo'].get('city', 'Unknown')}"
)
st.sidebar.markdown("**Version 1.0** | © 2025 Smart Insights")

# Placeholder main page
st.title("Smart Insights App")
st.success("App loaded successfully ✅")
