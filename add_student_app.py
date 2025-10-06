import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import date
import os

# --- File setup ---
CSV_FILE = "controlled_attendance.csv"

# Load or create the file
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["student_id", "name", "date", "attended"])
    df.to_csv(CSV_FILE, index=False)

# --- Function to add student ---
def add_student():
    student_id = entry_id.get().strip()
    name = entry_name.get().strip()

    if not student_id or not name:
        messagebox.showerror("Error", "Please fill out both ID and Name.")
        return

    try:
        student_id = int(student_id)
    except ValueError:
        messagebox.showerror("Error", "Student ID must be a number.")
        return

    # Reload latest CSV
    df = pd.read_csv(CSV_FILE)

    # Check for duplicates
    if student_id in df["student_id"].values:
        messagebox.showerror("Error", f"Student ID {student_id} already exists.")
        return

    # Add new student
    new_row = pd.DataFrame([{
        "student_id": student_id,
        "name": name,
        "date": str(date.today()),
        "attended": 0
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    # Clear input fields
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)

    messagebox.showinfo("Success", f"Student '{name}' (ID: {student_id}) added successfully!")

# --- Tkinter setup ---
root = tk.Tk()
root.title("Add New Student")
root.geometry("400x300")

ttk.Label(root, text="Add a New Student", font=("Arial", 16)).pack(pady=15)

frame = ttk.Frame(root)
frame.pack(pady=10)

ttk.Label(frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_id = ttk.Entry(frame, width=25)
entry_id.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_name = ttk.Entry(frame, width=25)
entry_name.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(root, text="Add Student", command=add_student).pack(pady=20)

root.mainloop()
