# GitHub Copilot Prompt:
# This app is a Streamlit-based data analytics dashboard called Smart Insights.
# Ensure the following logic is preserved across all pages:
# 1. Only the Home page allows users to upload, add, or remove datasets.
# 2. Once a dataset is uploaded, it is stored in st.session_state["uploaded_data"] and must be persistently accessible across all pages.
# 3. All other pages (Dashboard, Forecasting, ML Insights, Export, Settings) must use this session data without asking the user to upload again.
# 4. If "uploaded_data" is not found in the session state, pages should show a friendly warning and stop.
# 5. Currency and country selections (for conversion or API use) are stored in st.session_state["currency"] and st.session_state["country"], and should be respected globally.
# 6. IP location data is retrieved once and stored in st.session_state["ipinfo"] for sidebar display and optional logic.
# 7. Do not use st.set_page_config() anywhere except the root app.py file.
# 8. All data manipulation must be robust: handle nulls, invalid formats, and incorrect column selections with clear error messages.
# 9. Forecasting and ML models must not break if the dataset is small, empty, or mismatched — always validate input first.
# 10. Export page must allow exporting the current session dataset and computed outputs.
# 11. All API integrations (currency, holidays, IPInfo) must be non-blocking, handle errors gracefully, and cache where possible.
# 12. Sidebar must remain consistent across all pages — include branding, user location, and a working navigation menu.
# 13. Optimize for clarity, user experience, and no repeated uploads or broken logic. Each page should load and function independently but share session state.

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import classification_report, mean_squared_error, accuracy_score

st.set_page_config(page_title="ML Insights", page_icon="🤖")

def ml_insights_page():
    st.title("🤖 ML Insights - Automated Machine Learning Analysis")
    st.sidebar.markdown("### ML Tools")

    if "uploaded_data" not in st.session_state or st.session_state["uploaded_data"] is None:
        st.warning("⚠️ Please upload a dataset on the Home page.")
        st.stop()

    data = st.session_state["uploaded_data"]

    if data.shape[0] < 2:
        st.warning("⚠️ Dataset must have at least 2 rows.")
        st.stop()

    numeric_columns = data.select_dtypes(include=["number"]).columns
    categorical_columns = data.select_dtypes(include=["object"]).columns

    # Validate dataset size before train-test split
    if data.shape[1] < 2:
        st.error("Dataset must have at least 2 columns for ML Insights.")
        return

    st.sidebar.header("⚙️ Model Settings")

    target_col = st.selectbox("Select Target Column", options=data.columns)
    if pd.api.types.is_datetime64_any_dtype(data[target_col]):
        st.error("Target column cannot be of type datetime.")
        st.stop()

    features = st.multiselect("Select Features", options=numeric_columns.union(categorical_columns))

    if not features or not target_col:
        st.info("ℹ️ Please select both a target and one or more feature columns.")
        return

    try:
        X = data[features]
        y = data[target_col]
        X = pd.get_dummies(X)
        y = pd.to_numeric(y, errors='coerce')
        y = y.dropna()
        X = X.loc[y.index]
    except Exception as e:
        st.error(f"❌ Data processing error: {e}")
        return

    # Train/test split
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        st.success("Train-test split successful!")
    except ValueError as e:
        st.error(f"❌ Not enough rows or mismatched column types: {e}")
        return

    # Determine classification or regression
    is_classification = y.nunique() <= 10 and y.dtype in [int, 'int64']

    st.subheader("📊 Model Performance")
    if is_classification:
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        st.success("✅ Classification Model Trained (Random Forest)")
        st.text("📄 Classification Report:")
        st.text(classification_report(y_test, predictions))
        st.metric("🔍 Accuracy", f"{accuracy_score(y_test, predictions) * 100:.2f}%")
    else:
        model = RandomForestRegressor()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        st.success("✅ Regression Model Trained (Random Forest)")
        mse = mean_squared_error(y_test, predictions)
        st.metric("📉 Mean Squared Error", f"{mse:.2f}")

    # Feature importance
    st.subheader("📌 Feature Importance")
    importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    st.bar_chart(importances.head(10))

    # Prediction Preview
    st.subheader("🔍 Sample Predictions")
    pred_df = pd.DataFrame({
        "Actual": y_test,
        "Predicted": predictions
    }).reset_index(drop=True)
    st.dataframe(pred_df.head(10))
