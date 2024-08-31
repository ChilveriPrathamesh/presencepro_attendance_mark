
import face_recognition
import numpy as np
import pandas as pd
import mysql.connector
from datetime import datetime
from io import BytesIO
from PIL import Image
import os
import json

# Function to calculate face match confidence
def face_confidence(face_distance, face_match_threshold=0.6):
    range_val = (1.0 - face_match_threshold)   
    linear_val = (1.0 - face_distance) / (range_val * 2.0)

    if face_distance > face_match_threshold:
        return f"{round(linear_val * 100, 2)}%"
    else:
        value = (linear_val + ((1.0 - linear_val) * pow((linear_val - 0.5) * 2, 0.2))) * 100
        return f"{round(value, 2)}%"

# Class for Face Recognition and Attendance
class FaceRecognition:
    def __init__(self, db_config, class_name):
        self.db_config = db_config
        self.class_name = class_name
        self.known_face_encodings = []
        self.known_face_names = []
        self.attendance_df = None
        self.load_known_faces()

    # Method to load known faces from database
    def load_known_faces(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT fullName, imageDb FROM images WHERE className = %s", (self.class_name,))
            for name, image_data in cursor.fetchall():
                image = Image.open(BytesIO(image_data))
                face_image = np.array(image)
                face_encoding = face_recognition.face_encodings(face_image)[0]
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(name)
            cursor.close()
            connection.close()
            print("Known faces loaded.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
    # Method to fetch unknown faces from database
    def fetch_unknown_faces(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT id, imageDb FROM unknown_photos WHERE className = %s", (self.class_name,))
            unknown_faces = cursor.fetchall()
            cursor.close()
            connection.close()
            return unknown_faces
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    # Method to mark attendance and print to console
    def mark_attendance(self, present_names, absentees):
        now = datetime.now()
        time_str = now.strftime("%H-%M-%S")

        # Create DataFrame
        df = pd.DataFrame({
            'Name': present_names + absentees,
            'Status': ['Present'] * len(present_names) + ['Absent'] * len(absentees),
            'Time': [time_str] * (len(present_names) + len(absentees))
        })

        # Print to console
        print(df)
        return df  # Return the DataFrame for later use

    # Method to mark absentees based on detected names
    def mark_absent(self, detected_names):
        undetected_names = set(self.known_face_names) - set(detected_names) - {"Unknown"}
        return list(undetected_names)

    # Method to detect faces and mark attendance
    def detect_faces(self):
        detected_names = set()  # Use a set to avoid duplicates
        unknown_faces = self.fetch_unknown_faces()

        for id, image_data in unknown_faces:
            image = Image.open(BytesIO(image_data))
            face_image = np.array(image)
            face_locations = face_recognition.face_locations(face_image)
            face_encodings = face_recognition.face_encodings(face_image, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

                if name not in detected_names:
                    detected_names.add(name)

        detected_names = list(detected_names)
        absentees = self.mark_absent(detected_names)
        self.attendance_df = self.mark_attendance(detected_names, absentees)
        return self.attendance_df

    # Method to save attendance DataFrame to an Excel file
    def save_attendance_to_excel(self, filename):
        if self.attendance_df is not None:
            self.attendance_df.to_excel(filename, index=False)
            print(f"Attendance saved to {filename}")
        else:
            print("No attendance data to save.")

# Main execution block
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python face_reco.py <class_name> <output_excel_file>")
        sys.exit(1)

    class_name = sys.argv[1]
    output_excel_file = sys.argv[2]
    db_config = {
        'host' : 'aws-attendance.cz608aw60ypw.eu-north-1.rds.amazonaws.com',
        'user': 'admin',
        'password' : 'Pratham2807',
        'database' : 'presencepro'
    }

    try:
        fr = FaceRecognition(db_config, class_name)
        fr.detect_faces()
        fr.save_attendance_to_excel(output_excel_file)
        print(f"Attendance marked successfully. Excel file: {output_excel_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
