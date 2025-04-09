import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def export_page():
    st.header("📤 Export & Share Insights")

    # Check if data is uploaded
    if "data" not in st.session_state or st.session_state["data"] is None:
        st.warning("⚠️ Please upload data on the Home page first.")
        return

    data = st.session_state["data"]

    # ---- Download Section ----
    st.subheader("⬇️ Download Your Dataset")
    file_type = st.selectbox("Select File Format", ["CSV", "Excel"])

    if file_type == "CSV":
        csv = data.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="smart_insights_data.csv",
            mime="text/csv"
        )
    else:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            data.to_excel(writer, index=False, sheet_name="SmartInsights")
        st.download_button(
            label="Download Excel",
            data=buffer.getvalue(),
            file_name="smart_insights_data.xlsx",
            mime="application/vnd.ms-excel"
        )

    st.divider()

    # ---- Email Section ----
    st.subheader("📧 Email Your Report")
    st.markdown("Easily send your current dataset as an Excel attachment.")

    recipient = st.text_input("Recipient Email")
    subject = st.text_input("Email Subject", "Smart Insights Business Report")
    body = st.text_area(
        "Email Body",
        "Hi,\n\nPlease find attached your business analytics report.\n\nBest regards,\nSmart Insights"
    )

    if st.button("Send Email"):
        if not recipient:
            st.error("Recipient email is required.")
            return
        try:
            send_email_with_attachment(recipient, subject, body, data)
            st.success("✅ Email sent successfully!")
        except Exception as e:
            st.error(f"❌ Failed to send email: {str(e)}")


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
