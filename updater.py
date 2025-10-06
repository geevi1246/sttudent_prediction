import streamlit as st
import pandas as pd
from datetime import date
import os

# --- CSV file ---
CSV_FILE = "controlled_attendance.csv"

# Load or create CSV
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["student_id", "name", "date", "attendance"])
    df.to_csv(CSV_FILE, index=False)

st.title("Student Attendance Database")

# --- Show database ---
st.subheader("Current Student Data")
st.dataframe(df)

# --- Attendance form ---
st.subheader("Update Attendance")

student_id = st.number_input("Student ID:", min_value=0, step=1)
name = st.text_input("Student Name")
attendance = st.selectbox("Attendance", [1, 0])
attendance_date = st.date_input("Date", value=date.today())

if st.button("Update Attendance"):
    # Check if student already exists for that date
    exists = ((df["student_id"] == student_id) & (df["date"] == str(attendance_date))).any()
    
    if exists:
        df.loc[(df["student_id"] == student_id) & (df["date"] == str(attendance_date)), "attendance"] = attendance
        st.success(f"Updated attendance for {name} on {attendance_date}")
    else:
        # Add new row
        df = pd.concat([df, pd.DataFrame([{
            "student_id": student_id,
            "name": name,
            "date": attendance_date,
            "attendance": attendance
        }])], ignore_index=True)
        st.success(f"Added attendance for {name} on {attendance_date}")
    
    # Save CSV
    df.to_csv(CSV_FILE, index=False)

# --- Search student ---
st.subheader("Search Student Attendance")
search_id = st.number_input("Enter Student ID to search:", min_value=0, step=1, key="search")
if st.button("Search"):
    student_records = df[df["student_id"] == search_id]
    if not student_records.empty:
        st.dataframe(student_records)
    else:
        st.warning("No records found for this student ID")
