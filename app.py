import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
from datetime import datetime

# -------------------------
# Load model + feature columns
# -------------------------
try:
    rf_model = joblib.load("rf_model.pkl")
    scaler = joblib.load("scaler.pkl")
    feature_columns = joblib.load("feature_columns.pkl")
except FileNotFoundError:
    st.error("❌ Missing model files (rf_model.pkl, scaler.pkl, feature_columns.pkl). Please run the training notebook first.")
    st.stop()

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Sleep Quality Predictor 💤",
    page_icon="💤",
    layout="wide",
)

# -------------------------
# Init session state
# -------------------------
if "history" not in st.session_state:
    st.session_state["history"] = []

# -------------------------
# Title with custom SVG-style emoji
# -------------------------
st.markdown(
    """
    <h1 style="text-align:center; font-size:2.5rem;">
        💤 AI Sleep Quality Predictor
    </h1>
    <p style="text-align:center; font-size:1.2rem; color:gray;">
        Predict your sleep quality from your daily habits and lifestyle
    </p>
    <hr>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Tabs
# -------------------------
tab1, tab2, tab3 = st.tabs(
    ["🏠 Home", "📊 History", "🔮 What-If Simulator"]
)

# -------------------------
# Tab 1: Home / Prediction
# -------------------------
with tab1:
    st.header("🛌 Enter Your Daily Stats")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 10, 80, 25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        occupation = st.selectbox("Occupation", ["Software Engineer", "Doctor", "Sales Representative", "Teacher", "Nurse", "Engineer", "Accountant", "Scientist", "Lawyer", "Salesperson", "Manager", "Healthcare Representative"])
        sleep_duration = st.slider("Sleep Duration (hrs)", 3.0, 12.0, 7.0, step=0.5)
        physical_activity = st.slider("Physical Activity Level", 0, 100, 60)

    with col2:
        stress_level = st.slider("Stress Level", 1, 10, 5)
        bmi_category = st.selectbox("BMI Category", ["Overweight", "Normal", "Obese", "Underweight"])
        blood_pressure = st.selectbox("Blood Pressure", ["126/83", "125/80", "140/90", "132/87", "130/85", "131/86", "128/85", "130/86", "120/80", "118/76", "121/79", "128/84", "125/82", "129/84", "115/78", "135/88", "139/91", "140/95", "142/92", "117/76", "118/75", "135/90"])
        heart_rate = st.slider("Resting Heart Rate", 40, 120, 70)
        steps = st.slider("Daily Steps", 0, 30000, 7000, step=500)


    # Build input dataframe
    input_data = pd.DataFrame([[
        age, gender, occupation, sleep_duration, physical_activity,
        stress_level, bmi_category, blood_pressure, heart_rate, steps
    ]], columns=["Age", "Gender", "Occupation", "Sleep Duration", "Physical Activity Level", "Stress Level", "BMI Category", "Blood Pressure", "Heart Rate", "Daily Steps"])

    if st.button("🔍 Predict Sleep Quality"):
        # One-Hot Encode categorical columns
        cat_cols = input_data.select_dtypes(include="object").columns.tolist()
        input_encoded = pd.get_dummies(input_data, columns=cat_cols, drop_first=True)

        # Reindex to match training data columns
        input_encoded = input_encoded.reindex(columns=feature_columns, fill_value=0)

        # Scale numeric features
        input_scaled = scaler.transform(input_encoded)

        pred = rf_model.predict(input_scaled)[0]
        result = "😴 Good Sleep" if pred == 1 else "🥱 Poor Sleep"

        st.success(f"Prediction: **{result}**")

        # Save to history
        st.session_state["history"].append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Age": age,
            "Gender": gender,
            "Occupation": occupation,
            "Sleep Duration": sleep_duration,
            "Physical Activity Level": physical_activity,
            "Stress Level": stress_level,
            "BMI Category": bmi_category,
            "Blood Pressure": blood_pressure,
            "Heart Rate": heart_rate,
            "Daily Steps": steps,
            "Prediction": result
        })

# -------------------------
# Tab 2: History
# -------------------------
with tab2:
    st.header("📊 Prediction History")

    if len(st.session_state["history"]) > 0:
        df_hist = pd.DataFrame(st.session_state["history"])
        st.dataframe(df_hist, use_container_width=True)

        # Chart: Sleep Duration vs Stress
        fig = px.scatter(
            df_hist, x="Sleep Duration", y="Stress Level",
            color="Prediction", size="Daily Steps",
            title="Sleep Duration vs Stress Level"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No predictions made yet.")

# -------------------------
# Tab 3: What-If Simulator
# -------------------------
with tab3:
    st.header("🔮 What-If Simulator")
    st.write("Adjust your daily habits to see how it could affect your sleep quality.")

    # Use the last input from history or default values
    if st.session_state["history"]:
        last_input = st.session_state["history"][-1]
        sim_age = last_input["Age"]
        sim_gender = last_input["Gender"]
        sim_occupation = last_input["Occupation"]
        sim_sleep_duration = st.slider("Sleep Duration (hrs)", 3.0, 12.0, float(last_input["Sleep Duration"]), step=0.5)
        sim_physical_activity = st.slider("Physical Activity Level", 0, 100, last_input["Physical Activity Level"])
        sim_stress = st.slider("Stress Level", 1, 10, last_input["Stress Level"])
        sim_bmi_category = last_input["BMI Category"]
        sim_blood_pressure = last_input["Blood Pressure"]
        sim_heart_rate = last_input["Heart Rate"]
        sim_steps = st.slider("Daily Steps", 0, 30000, last_input["Daily Steps"], step=500)

    else:
        sim_age = 25
        sim_gender = "Male"
        sim_occupation = "Software Engineer"
        sim_sleep_duration = st.slider("Sleep Duration (hrs)", 3.0, 12.0, 7.0, step=0.5)
        sim_physical_activity = st.slider("Physical Activity Level", 0, 100, 60)
        sim_stress = st.slider("Stress Level", 1, 10, 5)
        sim_bmi_category = "Normal"
        sim_blood_pressure = "120/80"
        sim_heart_rate = 70
        sim_steps = st.slider("Daily Steps", 0, 30000, 7000, step=500)


    sim_input = pd.DataFrame([[
        sim_age, sim_gender, sim_occupation, sim_sleep_duration, sim_physical_activity,
        sim_stress, sim_bmi_category, sim_blood_pressure, sim_heart_rate, sim_steps
    ]], columns=["Age", "Gender", "Occupation", "Sleep Duration", "Physical Activity Level", "Stress Level", "BMI Category", "Blood Pressure", "Heart Rate", "Daily Steps"])

    # One-Hot Encode categorical columns
    sim_cat_cols = sim_input.select_dtypes(include="object").columns.tolist()
    sim_encoded = pd.get_dummies(sim_input, columns=sim_cat_cols, drop_first=True)

    # Reindex to match training data columns
    sim_encoded = sim_encoded.reindex(columns=feature_columns, fill_value=0)

    # Scale numeric features
    sim_scaled = scaler.transform(sim_encoded)

    sim_pred = rf_model.predict(sim_scaled)[0]
    sim_result = "😴 Good Sleep" if sim_pred == 1 else "🥱 Poor Sleep"

    st.metric("Simulated Prediction", sim_result)
