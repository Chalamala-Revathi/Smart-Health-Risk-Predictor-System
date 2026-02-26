import streamlit as st
import pandas as pd
import pickle

# -----------------------------
# Load saved artifacts
# -----------------------------
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

with open("feature_names.pkl", "rb") as f:
    feature_names = pickle.load(f)

# -----------------------------
# App config
# -----------------------------
st.set_page_config(
    page_title="Smart Health Predictor",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Smart Health Lifestyle Prediction")
st.write("Enter the details below to predict health risk level.")

# -----------------------------
# Load dataset (for ranges)
# -----------------------------
df = pd.read_csv("C:\\Users\\User\\OneDrive\\Desktop\\health_lifestyle_dataset.csv")

# -----------------------------
# Config
# -----------------------------
binary_columns = ["smoker", "family_history"]

risk_mapping = {
    0: "Low Risk 🟢",
    1: "Moderate Risk 🟡",
    2: "High Risk 🔴"
}

# -----------------------------
# User Inputs
# -----------------------------
st.subheader("📋 User Inputs")

user_input = {}

for col in feature_names:

    # Binary (Yes / No)
    if col in binary_columns:
        choice = st.selectbox(col.replace("_", " ").title(), ["No", "Yes"])
        user_input[col] = 1 if choice == "Yes" else 0

    # Daily steps slider
    elif col == "daily_steps":
        user_input[col] = st.slider(
            "Daily Steps 👟",
            min_value=0,
            max_value=20000,
            value=int(df["daily_steps"].mean()),
            step=500
        )

    # Categorical
    elif col in label_encoders:
        options = list(label_encoders[col].classes_)
        user_input[col] = st.selectbox(
            col.replace("_", " ").title(),
            options
        )

    # Numerical
    else:
        min_val = float(df[col].min())
        max_val = float(df[col].max())
        mean_val = float(df[col].mean())

        user_input[col] = st.number_input(
            col.replace("_", " ").title(),
            min_value=min_val,
            max_value=max_val,
            value=mean_val
        )

# -----------------------------
# Prediction
# -----------------------------
if st.button("🔍 Predict Health Risk"):
    input_df = pd.DataFrame([user_input])

    # Encode categorical features
    for col, le in label_encoders.items():
        if col in input_df.columns:
            input_df[col] = le.transform(input_df[col])

    # Ensure correct feature order
    input_df = input_df[feature_names]

    prediction = model.predict(input_df)[0]

    st.success(
        f"🧠 Predicted Health Risk Level: **{risk_mapping[prediction]}**"
    )
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:\\Users\\User\\OneDrive\\Desktop\\health_lifestyle_dataset (1).csv")

# Age distribution
plt.hist(df['Age'])
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()

# Correlation analysis
corr = df.corr()
print(corr)