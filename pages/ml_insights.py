import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import classification_report, mean_squared_error, accuracy_score

def ml_insights_page():
    st.title("🤖 ML Insights - Automated Machine Learning Analysis")

    if "uploaded_data" not in st.session_state or st.session_state.uploaded_data is None:
        st.warning("⚠️ Please upload your dataset on the Home page first.")
        return

    df = st.session_state.uploaded_data.copy()

    st.sidebar.header("⚙️ Model Settings")

    all_columns = df.columns.tolist()
    target = st.sidebar.selectbox("🎯 Select Target Column", options=all_columns)

    features = st.sidebar.multiselect(
        "🧮 Select Feature Columns (independent variables)",
        options=[col for col in all_columns if col != target]
    )

    if not features or not target:
        st.info("ℹ️ Please select both a target and one or more feature columns.")
        return

    X = df[features]
    y = df[target]

    try:
        X = pd.get_dummies(X)
        y = pd.to_numeric(y, errors='coerce')
        y = y.dropna()
        X = X.loc[y.index]
    except Exception as e:
        st.error(f"❌ Data processing error: {e}")
        return

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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
