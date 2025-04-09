import streamlit as st

import pandas as pd
from io import BytesIO
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from utils import convert_currency

# Validate dataset availability
if "uploaded_data" not in st.session_state or st.session_state["uploaded_data"] is None:
    st.warning("Please upload a dataset on the Home page to proceed.")
    st.stop()

data = st.session_state["uploaded_data"]

def export_page():
    st.title("📁 Export - Download Your Data")
    st.sidebar.markdown("### Export Options")

    if st.session_state["uploaded_data"] is None:
        st.warning("⚠️ No data available. Please upload data on the Home page.")
        return

    # Currency selection
    currency = st.session_state.get("currency", "USD")
    st.write(f"Exporting data in {currency} currency.")

    # File format and currency selection
    file_format = st.selectbox("Select file format", ["CSV", "Excel"])
    currency = st.selectbox("Select currency", ["USD", "EUR", "GBP"])  # Add more as needed

    # Convert currency if needed
    if currency != "USD":
        try:
            data["Converted"] = data["Amount"].apply(lambda x: convert_currency(x, currency))
        except Exception as e:
            st.error(f"❌ Currency conversion failed: {e}")
            return

    # Export functionality
    if st.button("Export"):
        try:
            if file_format == "CSV":
                data.to_csv("exported_data.csv", index=False)
                st.success("Data exported as CSV.")
            elif file_format == "Excel":
                data.to_excel("exported_data.xlsx", index=False)
                st.success("Data exported as Excel.")
        except Exception as e:
            st.error(f"Error exporting data: {e}")

    # Download buttons
    csv = data.to_csv(index=False)
    st.download_button("Download CSV", csv, "data.csv", "text/csv")

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        data.to_excel(writer, index=False, sheet_name="Sheet1")
    st.download_button("Download Excel", output.getvalue(), "data.xlsx", "application/vnd.ms-excel")

def send_email_with_attachment(to, subject, body, df):
    from_email = st.secrets["EMAIL"]
    from_password = st.secrets["EMAIL_PASSWORD"]
    smtp_server = st.secrets["SMTP_SERVER"]
    smtp_port = st.secrets["SMTP_PORT"]

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="SmartInsights")
    attachment = buffer.getvalue()

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    part = MIMEApplication(attachment, Name="smart_insights_data.xlsx")
    part["Content-Disposition"] = 'attachment; filename="smart_insights_data.xlsx"'
    msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
