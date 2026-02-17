import cv2
import os
import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import time

# ---------------------------------------------------
# BASE DIRECTORY
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
CSV_FILE = os.path.join(BASE_DIR, "student_details.csv")

# Create dataset folder if not exists
os.makedirs(DATASET_DIR, exist_ok=True)

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# ---------------------------------------------------
# REGISTRATION FUNCTION
# ---------------------------------------------------
def register_student_gui(student_name, department, student_id, semester,
                         num_samples=15):

    if not student_name.strip():
        messagebox.showerror("Error", "Please enter a student name.")
        return

    # Create student folder inside dataset
    student_path = os.path.join(DATASET_DIR, student_name)
    os.makedirs(student_path, exist_ok=True)

    # Write student details safely
    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(['Name', 'ID', 'Department',
                             'Semester', 'Registration Time'])

        writer.writerow([
            student_name,
            student_id,
            department,
            semester,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ])

    cap = cv2.VideoCapture(0)
    count = 0
    last_capture_time = 0
    capture_interval = 0.6  # Slower capture (adjust if needed)

    messagebox.showinfo(
        "Info",
        f"Starting capture for {student_name}.\nMove your head slowly.\nPress 'q' to stop."
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        current_time = time.time()

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y),
                          (x + w, y + h), (0, 255, 0), 2)

            if current_time - last_capture_time > capture_interval:
                face_img = frame[y:y + h, x:x + w]
                img_path = os.path.join(
                    student_path,
                    f"{student_name}_{count}.jpg"
                )
                cv2.imwrite(img_path, face_img)
                count += 1
                last_capture_time = current_time

        # Show progress
        cv2.putText(frame, f"Captured: {count}/{num_samples}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)

        cv2.imshow("Capturing Faces - Press 'q' to quit", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or count >= num_samples:
            break

    cap.release()
    cv2.destroyAllWindows()

    messagebox.showinfo(
        "Done",
        f"Captured {count} face images.\nStored in:\n{student_path}"
    )


# ---------------------------------------------------
# GUI
# ---------------------------------------------------
def open_registration_gui():

    def on_register():
        student_name = name_entry.get().strip()
        department = department_entry.get().strip()
        student_id = id_entry.get().strip()
        semester = semester_entry.get().strip()

        if not student_name or not department or not student_id or not semester:
            messagebox.showerror(
                "Error", "Please fill all fields before registering.")
        else:
            register_student_gui(student_name,
                                 department,
                                 student_id,
                                 semester)

    window = tk.Tk()
    window.title("Student Face Registration")
    window.geometry("400x350")

    tk.Label(window, text="Student Name").pack(pady=5)
    name_entry = tk.Entry(window, width=30)
    name_entry.pack(pady=5)

    tk.Label(window, text="Student ID").pack(pady=5)
    id_entry = tk.Entry(window, width=30)
    id_entry.pack(pady=5)

    tk.Label(window, text="Department").pack(pady=5)
    department_entry = tk.Entry(window, width=30)
    department_entry.pack(pady=5)

    tk.Label(window, text="Semester").pack(pady=5)
    semester_entry = tk.Entry(window, width=30)
    semester_entry.pack(pady=5)

    tk.Button(window,
              text="Start Registration",
              command=on_register).pack(pady=20)

    window.mainloop()


# ---------------------------------------------------
# START
# ---------------------------------------------------
open_registration_gui()
