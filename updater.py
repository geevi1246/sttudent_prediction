import streamlit as st
import pandas as pd
from datetime import date, datetime
import re
import os

st.set_page_config(page_title="RFID Attendance", layout="centered")

# -----------------------
# CONFIG
# -----------------------
CSV_FILE = "controlled_attendance.csv"

# -----------------------
# UTILITIES
# -----------------------
def load_attendance():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, dtype=str)  # load all as string
        # Keep only relevant columns
        df = df[["student_id", "card_id", "name", "date", "attended"]]
    else:
        st.error(f"{CSV_FILE} not found!")
        df = pd.DataFrame(columns=["student_id", "card_id", "name", "date", "attended"])
    return df

def save_attendance(df):
    df.to_csv(CSV_FILE, index=False)

def normalize_id(raw):
    """Clean scanned input: keep digits only."""
    if raw is None:
        return ""
    s = str(raw).strip()
    digits = re.sub(r"\D", "", s)
    return digits

def mark_attendance(card_id, df):
    today = date.today().isoformat()
    cid = str(card_id).zfill(10)  # ensure leading zeros (10 digits)

    # Check if card exists in database
    if cid not in df["card_id"].values:
        return False, df, "Card ID not found in database!"

    # Prevent double check-in
    existing = df[(df["card_id"] == cid) & (df["date"] == today)]
    if not existing.empty:
        return False, df, "Already checked in today."

    # Get student info
    student_row = df[df["card_id"] == cid].iloc[0]
    name = student_row["name"]
    student_id = student_row["student_id"]

    # Add attendance row
    new_row = {"student_id": student_id, "card_id": cid, "name": name, "date": today, "attended": "1"}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_attendance(df)
    return True, df, f"Marked present: {name} ({cid})"

# -----------------------
# PAGE LAYOUT
# -----------------------
st.title("RFID Attendance")
st.markdown(
    """
    Scan an RFID card with your USB reader into the **Scan** box below.
    Make sure the cursor is in the box, then scan your card.
    """
)

# Load CSV
attendance_df = load_attendance()

# Show today's summary
today = date.today().isoformat()
today_df = attendance_df[attendance_df["date"] == today]
present_count = today_df["attended"].astype(int).sum() if not today_df.empty else 0
st.subheader(f"Today's attendance ({today}) — Present: {int(present_count)} / {attendance_df['student_id'].nunique()}")

# Scan input
if "last_scan" not in st.session_state:
    st.session_state["last_scan"] = ""

def _on_scan():
    raw = st.session_state.scan_input
    st.session_state["last_scan"] = normalize_id(raw)

st.text_input(
    "Scan RFID card here",
    key="scan_input",
    on_change=_on_scan,
    placeholder="Click here and scan a card"
)

# Process scan
if st.session_state["last_scan"]:
    scanned = st.session_state["last_scan"]
    st.session_state["last_scan"] = ""  # clear to avoid reprocessing
    success, attendance_df, msg = mark_attendance(scanned, attendance_df)
    if success:
        st.success(msg)
    else:
        st.warning(msg)

# Show today's attendance
st.write("---")
st.subheader("Today's Attendance")
display_df = attendance_df[attendance_df["date"] == today].sort_values(by="name")
st.dataframe(display_df.reset_index(drop=True))

# Export CSV
st.write("---")
st.download_button(
    "Download attendance.csv",
    data=attendance_df.to_csv(index=False).encode("utf-8"),
    file_name="controlled_attendance.csv",
    mime="text/csv"
)
