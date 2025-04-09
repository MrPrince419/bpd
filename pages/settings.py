import streamlit as st

def settings_page():
    st.set_page_config(page_title="Settings", page_icon="⚙️")
    st.title("⚙️ App Settings")

    st.markdown("Manage Smart Insights preferences and configurations here.")

    st.subheader("Appearance")
    st.radio("Choose Theme", ["Light", "Dark", "System default"], index=2, help="Streamlit uses system theme by default.")

    st.subheader("Data Settings")
    st.info("All uploaded data is stored in session state and shared across pages.\n\nTo upload or reset your dataset, please return to the **Home** page.")

    st.subheader("Upcoming Features")
    st.markdown("- Multi-user support\n- Save app state\n- API integrations")
