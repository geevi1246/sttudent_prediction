import streamlit as st
import pandas as pd
from datetime import date
import os

# --- File setup ---
CSV_FILE = "controlled_attendance.csv"

# Load or create CSV
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["student_id", "name", "date", "attended"])
    df.to_csv(CSV_FILE, index=False)

# --- Streamlit UI ---
st.title("Add a New Student")

with st.form("add_student_form"):
    student_id = st.text_input("Student ID")
    name = st.text_input("Name")
    submitted = st.form_submit_button("Add Student")

    if submitted:
        if not student_id or not name:
            st.error("Please fill out both ID and Name.")
        else:
            try:
                student_id_int = int(student_id)
            except ValueError:
                st.error("Student ID must be a number.")
            else:
                # Reload latest CSV
                df = pd.read_csv(CSV_FILE)

                # Check for duplicates
                if student_id_int in df["student_id"].values:
                    st.error(f"Student ID {student_id_int} already exists.")
                else:
                    # Add new student
                    new_row = pd.DataFrame([{
                        "student_id": student_id_int,
                        "name": name,
                        "date": str(date.today()),
                        "attended": 0
                    }])
                    df = pd.concat([df, new_row], ignore_index=True)
                    df.to_csv(CSV_FILE, index=False)

                    st.success(f"Student '{name}' (ID: {student_id_int}) added successfully!")

# Optional: Display current students
if st.checkbox("Show all students"):
    st.dataframe(pd.read_csv(CSV_FILE))
