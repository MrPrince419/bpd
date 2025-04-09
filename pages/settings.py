import streamlit as st
import os
import json
from pathlib import Path

# Check if running on Streamlit Cloud
IS_CLOUD = os.environ.get("STREAMLIT_SERVER_HEADLESS", "0") == "1"
SETTINGS_PATH = Path("config.json")

def load_settings():
    if IS_CLOUD:
        # Read from Streamlit secrets
        email = st.secrets.get("email", "")
        password = st.secrets.get("password", "")
    elif SETTINGS_PATH.exists():
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
            email = settings.get("email", "")
            password = settings.get("password", "")
    else:
        email = ""
        password = ""
    return email, password

def save_settings(data):
    try:
        with open(SETTINGS_PATH, "w") as f:
            json.dump(data, f)
    except OSError:
        st.error("Unable to save settings (read-only file system).")

def settings_page():
    st.title("⚙️ App Settings")
    st.write("Update your configuration below (e.g. email report credentials).")

    email, password = load_settings()

    email = st.text_input("📧 Sender Email", value=email)
    password = st.text_input("🔐 Email Password", value=password, type="password")

    if st.button("💾 Save Settings"):
        if IS_CLOUD:
            st.warning("Settings cannot be saved on Streamlit Cloud. Use `.streamlit/secrets.toml`.")
        else:
            save_settings({"email": email, "password": password})
            st.success("Settings saved successfully!")
