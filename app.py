import streamlit as st

st.set_page_config(page_title="Testing App", page_icon="🚀")

st.title("App is running ✅")
st.write("Before importing dashboard...")from pages.dashboard import dashboard_pagest.write("Dashboard page imported ✅")from pages.home import home_pagefrom pages.forecasting import forecasting_pagefrom pages.ml_insights import ml_insights_pagefrom pages.export import export_pagefrom pages.settings import settings_pagefrom ipinfo_tools import get_location_info# Initialize session stateif "uploaded_data" not in st.session_state:    st.session_state["uploaded_data"] = Noneif "currency" not in st.session_state:    st.session_state["currency"] = "USD"if "country" not in st.session_state:    st.session_state["country"] = "United States"if "ipinfo" not in st.session_state:    st.session_state["ipinfo"] = get_location_info()# Sidebar setupst.sidebar.title("Smart Insights")st.sidebar.markdown("Helping small businesses make data-driven decisions.")st.sidebar.info(f"🌍 {st.session_state.get('ipinfo', {}).get('country', 'Unknown')}, {st.session_state.get('ipinfo', {}).get('city', 'Unknown')}")st.sidebar.markdown("---")st.sidebar.markdown("**Version 1.0** | © 2025 Smart Insights")# Sidebar navigationpage = st.sidebar.radio(    "Navigate",    ["Home", "Dashboard", "Forecasting", "ML Insights", "Export", "Settings"],    index=0)# Page routingif page == "Home":    home_page()elif page == "Dashboard":    dashboard_page()elif page == "Forecasting":    forecasting_page()elif page == "ML Insights":
    ml_insights_page()
elif page == "Export":
    export_page()
elif page == "Settings":
    settings_page()
