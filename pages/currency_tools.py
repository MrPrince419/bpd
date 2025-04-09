import streamlit as st
import requests

def currency_tools_page():
    st.title("💱 Currency Tools - Convert Currencies")

    # === Currency Converter ===
    st.subheader("Currency Converter")

    # Dropdowns for currency selection
    currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "NGN"]
    
    # Fallback to detected currency
    default_currency = st.session_state["ipinfo"].get("country", "USD")
    from_currency = st.selectbox("From Currency", currencies, index=currencies.index(default_currency))
    to_currency = st.selectbox("To Currency", currencies, index=currencies.index("NGN"))

    # Input for amount
    amount = st.number_input("Amount", min_value=0.0, value=1.0, step=0.01)

    # Convert button
    if st.button("Convert"):
        try:
            response = requests.get(f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}")
            if response.status_code == 200:
                result = response.json().get("result", 0.0)
                st.metric(label=f"{amount} {from_currency} = ", value=f"{result:.2f} {to_currency}")
            else:
                st.error("Failed to fetch conversion rate. Try again later.")
        except Exception as e:
            st.error(f"Error: {e}")
