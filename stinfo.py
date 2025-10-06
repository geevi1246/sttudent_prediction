import pandas as pd
import random
from datetime import datetime, timedelta
import os

# -----------------------------
# CONFIGURATION
# -----------------------------
num_days = 1000  # <-- change this to control number of days
attendance_prob = 0.75# probability that a student attends (0.75 = 75%)
output_folder = os.getcwd()  # current folder
csv_filename = os.path.join(output_folder, "controlled_attendance.csv")

# -----------------------------
# STUDENTS
# -----------------------------
student_names = ["SUHADA", "GEEVINDA", "CHENUL", "SANUTH", "VIDULA", "SUBASHINI", "JANIDI", "INUKA", "BIHAN", "PRABATH","CHINTHAKA"]
student_ids = list(range(1, len(student_names)+1))

# -----------------------------
# GENERATE DATES
# -----------------------------
start_date = datetime.today() - timedelta(days=num_days)
dates = [start_date + timedelta(days=i) for i in range(num_days)]

# -----------------------------
# GENERATE DATASET
# -----------------------------
data = []
for date in dates:
    for sid, name in zip(student_ids, student_names):
        # Attendance: most attend, few absent
        attended = 1 if random.random() < attendance_prob else 0
        data.append([sid, name, date.strftime("%Y-%m-%d"), attended])

# -----------------------------
# CREATE DATAFRAME AND SAVE
# -----------------------------
df = pd.DataFrame(data, columns=["student_id", "name", "date", "attended"])
df.to_csv(csv_filename, index=False)

print(f"CSV generated successfully at: {csv_filename}")
print(df.head())
print(f"Total records: {len(df)}")
