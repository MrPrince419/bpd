import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def ml_insights_page():
    st.title("🧠 Machine Learning Insights")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is None:
        st.info("Please upload a CSV file to view ML insights.")
        return

    try:
        data = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return

    if data.empty or len(data.columns) < 2:
        st.warning("Not enough data to build a model.")
        return

    # Sidebar for column selection
    st.sidebar.header("ML Configuration")
    target_col = st.sidebar.selectbox("Select Target Column", options=data.columns)

    feature_cols = st.sidebar.multiselect(
        "Select Feature Columns (X)", 
        [col for col in data.columns if col != target_col],
        default=[col for col in data.columns if col != target_col][:3]
    )

    if not feature_cols:
        st.warning("Please select at least one feature column.")
        return

    try:
        X = data[feature_cols]
        y = data[target_col]

        # Drop missing values
        df = pd.concat([X, y], axis=1).dropna()
        X = df[feature_cols]
        y = df[target_col]

        # Encode target if needed
        if y.dtype == "object":
            y = y.astype("category").cat.codes

        X = pd.get_dummies(X)

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Output
        st.subheader("🔍 Model Evaluation")
        st.write("Accuracy:", accuracy_score(y_test, y_pred))
        st.text("Classification Report:")
        st.text(classification_report(y_test, y_pred))

        # Feature importance
        st.subheader("📊 Feature Importance")
        importances = pd.Series(model.feature_importances_, index=X.columns)
        st.bar_chart(importances.sort_values(ascending=False))

    except Exception as e:
        st.error(f"Error during model training: {e}")
