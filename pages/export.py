import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def export_page():
    if "data" not in st.session_state:
        st.warning("Please upload data from the Home page.")
        return

    st.header("📤 Export & Share Insights")

    data = st.session_state["data"]

    st.subheader("⬇️ Download Data")
    file_type = st.selectbox("Choose file format", ["CSV", "Excel"])

    if file_type == "CSV":
        csv = data.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "business_data.csv", "text/csv")
    else:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            data.to_excel(writer, index=False, sheet_name="Data")
        st.download_button("Download Excel", buffer.getvalue(), "business_data.xlsx", "application/vnd.ms-excel")

    st.divider()

    st.subheader("📧 Email Report")
    st.markdown("Send your current dataset to any email as an attachment.")

    recipient = st.text_input("Recipient Email")
    subject = st.text_input("Email Subject", "Business Analytics Report")
    body = st.text_area("Email Body", "Hi, please find attached your business analytics report.")

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

    # Create attachment
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    attachment = buffer.getvalue()

    # Email structure
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    part = MIMEApplication(attachment, Name="business_data.xlsx")
    part["Content-Disposition"] = 'attachment; filename="business_data.xlsx"'
    msg.attach(part)

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
