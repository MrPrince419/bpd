import streamlit as st

def home_page():
    st.title("📊 Small Business Analytics Dashboard")
    st.markdown("Welcome to your all-in-one dashboard for small business data insights!")

    st.image("https://images.unsplash.com/photo-1556761175-4b46a572b786", use_column_width=True)

    st.markdown("""
        ### What You Can Do Here
        - 📈 **Dashboard**: See trends, revenue, and growth at a glance.
        - 🔮 **Forecasting**: Predict future performance with smart forecasting.
        - 🧠 **ML Insights**: Get AI-powered insights from your business data.
        - 📤 **Export**: Download reports in Excel or PDF format.
        - ⚙️ **Settings**: Customize your experience.

        ---
        👈 Use the sidebar to navigate through the pages.
    """)
