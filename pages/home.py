import streamlit as st
import pandas as pd

def home_page():
    st.title("🏠 Home - Upload Your Business Data")

    st.info("📌 Upload your dataset here. It will be used across all pages like Dashboard, Forecasting, ML Insights, and Export. To change or remove data, come back here.")

    # File uploader
    uploaded_file = st.file_uploader("📤 Upload your CSV file", type=["csv"])

    # Save to session if uploaded
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.uploaded_data = df
            st.success("✅ Data uploaded and saved in session.")
            st.write("📄 Here's a preview of your data:")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

    # If data is already uploaded, show clear button
    elif "uploaded_data" in st.session_state and st.session_state.uploaded_data is not None:
        st.success("✅ Data already loaded in session.")
        st.dataframe(st.session_state.uploaded_data.head())

        st.markdown("---")
        if st.button("🗑️ Remove Uploaded Data"):
            del st.session_state.uploaded_data
            st.success("✅ Uploaded data removed. Upload new data to continue.")
