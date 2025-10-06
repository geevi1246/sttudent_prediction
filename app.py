import pandas as pd
import joblib
import streamlit as st

# Load model and data
model = joblib.load("attendance_model.pkl")
df = pd.read_csv("controlled_attendance.csv")
valid_ids = df['student_id'].tolist()

st.title("Attendance Predictor")

student_id = st.number_input("Enter Student ID:", min_value=0, step=1)

if st.button("Predict Attendance"):
    if student_id not in valid_ids:
        st.error(f"Student ID {student_id} not found.")
    else:
        new_data = pd.DataFrame({'student_id': [student_id]})
        prediction = model.predict(new_data)[0]
        probability = model.predict_proba(new_data)[0][1]
        probability=probability*100
        st.success(f"Predicted Attendance: {prediction}")
        st.info(f"Probability of attending: {probability:.2f}%")
