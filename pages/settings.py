import streamlit as st
import toml
import os

SETTINGS_PATH = ".streamlit/secrets.toml"

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        return toml.load(SETTINGS_PATH)
    return {}

def save_settings(data):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        toml.dump(data, f)

def settings_page():
    st.title("⚙️ Settings")
    st.markdown("Update your configuration below (e.g. email report credentials).")

    settings = load_settings()

    # Load existing values or default to blank
    email = st.text_input("📧 Sender Email", value=settings.get("email", ""))
    password = st.text_input("🔑 Email Password", value=settings.get("password", ""), type="password")

    if st.button("💾 Save Settings"):
        if not email or not password:
            st.error("Both fields are required.")
        else:
            save_settings({"email": email, "password": password})
            st.success("Settings saved successfully!")
