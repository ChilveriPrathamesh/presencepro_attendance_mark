# # import face_recognition
# # import cv2
# # import numpy as np
# # import pandas as pd
# # import mysql.connector
# # from datetime import datetime
# # from io import BytesIO
# # from PIL import Image

# # def face_confidence(face_distance, face_match_threshold=0.6):
# #     range_val = (1.0 - face_match_threshold)   
# #     linear_val = (1.0 - face_distance) / (range_val * 2.0)

# #     if face_distance > face_match_threshold:
# #         return f"{round(linear_val * 100, 2)}%"
# #     else:
# #         value = (linear_val + ((1.0 - linear_val) * pow((linear_val - 0.5) * 2, 0.2))) * 100
# #         return f"{round(value, 2)}%"

# # class FaceRecognition:
# #     def __init__(self, db_config, class_name):
# #         self.db_config = db_config
# #         self.class_name = class_name
# #         self.known_face_encodings = []
# #         self.known_face_names = []
# #         self.load_known_faces()

# #     def load_known_faces(self):
# #         try:
# #             connection = mysql.connector.connect(**self.db_config)
# #             cursor = connection.cursor()
# #             cursor.execute("SELECT fullName, imageDb FROM images WHERE className = %s", (self.class_name,))
# #             for name, image_data in cursor.fetchall():
# #                 image = Image.open(BytesIO(image_data))
# #                 face_image = np.array(image)
# #                 face_encoding = face_recognition.face_encodings(face_image)[0]
# #                 self.known_face_encodings.append(face_encoding)
# #                 self.known_face_names.append(name)
# #             cursor.close()
# #             connection.close()
# #             print("Known faces loaded.")
# #         except mysql.connector.Error as err:
# #             print(f"Error: {err}")
    
# #     def fetch_unknown_faces(self):
# #         try:
# #             connection = mysql.connector.connect(**self.db_config)
# #             cursor = connection.cursor()
# #             cursor.execute("SELECT id, imageDb FROM unknown_photos WHERE className = %s", (self.class_name,))
# #             unknown_faces = cursor.fetchall()
# #             cursor.close()
# #             connection.close()
# #             return unknown_faces
# #         except mysql.connector.Error as err:
# #             print(f"Error: {err}")
# #             return []

# #     def mark_attendance(self, present_names):
# #         now = datetime.now()
# #         date_str = now.strftime("%Y-%m-%d")
# #         time_str = now.strftime("%H:%M:%S")

# #         try:
# #             connection = mysql.connector.connect(**self.db_config)
# #             cursor = connection.cursor()

# #             for name in present_names:
# #                 cursor.execute(
# #                     "INSERT INTO attendance (fullName, time, attendance_status, className) VALUES (%s, %s, %s, %s)",
# #                     (name, time_str, 'Present', self.class_name)
# #                 )
            
# #             connection.commit()
# #             cursor.close()
# #             connection.close()
# #         except mysql.connector.Error as err:
# #             print(f"Error: {err}")

# #     def mark_absent(self, detected_names):
# #         undetected_names = set(self.known_face_names) - set(detected_names) - {"Unknown"}
# #         now = datetime.now()
# #         date_str = now.strftime("%Y-%m-%d")
# #         time_str = now.strftime("%H:%M:%S")

# #         try:
# #             connection = mysql.connector.connect(**self.db_config)
# #             cursor = connection.cursor()

# #             for name in undetected_names:
# #                 cursor.execute(
# #                     "INSERT INTO attendance (fullName, time, attendance_status, className) VALUES (%s, %s, %s, %s)",
# #                     (name, time_str, 'Absent', self.class_name)
# #                 )
            
# #             connection.commit()
# #             cursor.close()
# #             connection.close()
# #         except mysql.connector.Error as err:
# #             print(f"Error: {err}")

# #     def detect_faces(self):
# #         detected_names = set()  # Use a set to avoid duplicates
# #         unknown_faces = self.fetch_unknown_faces()

# #         for id, image_data in unknown_faces:
# #             image = Image.open(BytesIO(image_data))
# #             face_image = np.array(image)
# #             face_locations = face_recognition.face_locations(face_image)
# #             face_encodings = face_recognition.face_encodings(face_image, face_locations)

# #             for face_encoding in face_encodings:
# #                 matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
# #                 name = "Unknown"
# #                 face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
# #                 best_match_index = np.argmin(face_distances)

# #                 if matches[best_match_index]:
# #                     name = self.known_face_names[best_match_index]

# #                 if name not in detected_names:
# #                     detected_names.add(name)

# #         detected_names = list(detected_names)
# #         self.mark_attendance(detected_names)
# #         self.mark_absent(detected_names)
# #         return detected_names

# # if __name__ == "__main__":
# #     import sys
# #     import json

# #     if len(sys.argv) < 2:
# #         print("Usage: python face_reco.py <class_name>")
# #         sys.exit(1)

# #     class_name = sys.argv[1]
# #     db_config = {
# #         'host': "localhost",
# #         'user': "root",
# #         'password': "Pratham2807@",
# #         'database': "presencepro"
# #     }

# #     try:
# #         fr = FaceRecognition(db_config, class_name)
# #         detected_names = fr.detect_faces()
# #         print(f"Detected names: {detected_names}")
# #     except Exception as e:
# #         print(f"An error occurred: {e}")



# import face_recognition
# import numpy as np
# import pandas as pd
# import mysql.connector
# from datetime import datetime
# from io import BytesIO
# from PIL import Image

# class FaceRecognition:
#     def __init__(self, db_config, class_name):
#         self.db_config = db_config
#         self.class_name = class_name
#         self.known_face_encodings = []
#         self.known_face_names = []
#         self.load_known_faces()

#     def load_known_faces(self):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()
#             cursor.execute("SELECT fullName, imageDb FROM images WHERE className = %s", (self.class_name,))
#             for name, image_data in cursor.fetchall():
#                 image = Image.open(BytesIO(image_data))
#                 face_image = np.array(image)
#                 face_encoding = face_recognition.face_encodings(face_image)[0]
#                 self.known_face_encodings.append(face_encoding)
#                 self.known_face_names.append(name)
#             cursor.close()
#             connection.close()
#             print("Known faces loaded.")
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
    
#     def fetch_unknown_faces(self):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()
#             cursor.execute("SELECT id, imageDb FROM unknown_photos WHERE className = %s", (self.class_name,))
#             unknown_faces = cursor.fetchall()
#             cursor.close()
#             connection.close()
#             return unknown_faces
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
#             return []

#     def mark_attendance(self):
#         detected_names = set()  # Use a set to avoid duplicates
#         unknown_faces = self.fetch_unknown_faces()

#         for id, image_data in unknown_faces:
#             image = Image.open(BytesIO(image_data))
#             face_image = np.array(image)
#             face_locations = face_recognition.face_locations(face_image)
#             face_encodings = face_recognition.face_encodings(face_image, face_locations)

#             for face_encoding in face_encodings:
#                 matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
#                 name = "Unknown"
#                 face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
#                 best_match_index = np.argmin(face_distances)

#                 if matches[best_match_index]:
#                     name = self.known_face_names[best_match_index]

#                 if name not in detected_names:
#                     detected_names.add(name)

#         detected_names = list(detected_names)
#         absentees = self.mark_absent(detected_names)
#         self.save_attendance_to_db(detected_names, absentees)
#         self.print_attendance(detected_names, absentees)  # Print attendance details

#     def mark_absent(self, detected_names):
#         undetected_names = set(self.known_face_names) - set(detected_names) - {"Unknown"}
#         return list(undetected_names)

#     def save_attendance_to_db(self, detected_names, absentees):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()

#             now = datetime.now()
#             date_str = now.strftime("%Y-%m-%d")
#             time_str = now.strftime("%H-%M-%S")

#             # Insert attendance data into 'attendance' table
#             for name in detected_names:
#                 cursor.execute("INSERT INTO attendance (className, fullName, attendance_status, time) VALUES (%s, %s, %s, %s)",
#                                (self.class_name, name, 'Present', time_str))
#             for name in absentees:
#                 cursor.execute("INSERT INTO attendance (className, fullName, attendance_status, time) VALUES (%s, %s, %s, %s)",
#                                (self.class_name, name, 'Absent', time_str))

#             connection.commit()
#             cursor.close()
#             connection.close()
#             print("Attendance details saved to database.")

#         except mysql.connector.Error as err:
#             print(f"Error saving attendance to database: {err}")

#     def print_attendance(self, detected_names, absentees):
#         print("\nAttendance Details:")
#         print("===================")
#         print(f"Class Name: {self.class_name}")
#         now = datetime.now()
#         date_str = now.strftime("%Y-%m-%d")
#         time_str = now.strftime("%H:%M:%S")
#         print(f"Date: {date_str}")
#         print(f"Time: {time_str}\n")

#         print("Present:")
#         for name in detected_names:
#             print(f"- {name}")

#         print("\nAbsent:")
#         for name in absentees:
#             print(f"- {name}")

# if __name__ == "__main__":
#     import sys

#     if len(sys.argv) < 2:
#         print("Usage: python face_reco.py <class_name>")
#         sys.exit(1)

#     class_name = sys.argv[1]
#     db_config = {
#         'host': "localhost",
#         'user': "root",
#         'password': "Pratham2807@",
#         'database': "presencepro"
#     }

#     try:
#         fr = FaceRecognition(db_config, class_name)
#         fr.mark_attendance()
#         print("\nAttendance marking complete.")
#     except Exception as e:
#         print(f"An error occurred: {e}")


# import face_recognition
# import cv2
# import numpy as np
# import pandas as pd
# import mysql.connector
# from datetime import datetime
# from io import BytesIO
# from PIL import Image

# def face_confidence(face_distance, face_match_threshold=0.6):
#     range_val = (1.0 - face_match_threshold)   
#     linear_val = (1.0 - face_distance) / (range_val * 2.0)

#     if face_distance > face_match_threshold:
#         return f"{round(linear_val * 100, 2)}%"
#     else:
#         value = (linear_val + ((1.0 - linear_val) * pow((linear_val - 0.5) * 2, 0.2))) * 100
#         return f"{round(value, 2)}%"

# class FaceRecognition:
#     def _init_(self, db_config, class_name):
#         self.db_config = db_config
#         self.class_name = class_name
#         self.known_face_encodings = []
#         self.known_face_names = []
#         self.load_known_faces()

#     def load_known_faces(self):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()
#             cursor.execute("SELECT fullName, imageDb FROM images WHERE className = %s", (self.class_name,))
#             for name, image_data in cursor.fetchall():
#                 image = Image.open(BytesIO(image_data))
#                 face_image = np.array(image)
#                 face_encoding = face_recognition.face_encodings(face_image)[0]
#                 self.known_face_encodings.append(face_encoding)
#                 self.known_face_names.append(name)
#             cursor.close()
#             connection.close()
#             print("Known faces loaded.")
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
    
#     def fetch_unknown_faces(self):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()
#             cursor.execute("SELECT id, imageDb FROM unknown_photos WHERE className = %s", (self.class_name,))
#             unknown_faces = cursor.fetchall()
#             cursor.close()
#             connection.close()
#             return unknown_faces
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
#             return []

#     def mark_attendance(self, present_names):
#         now = datetime.now()
#         date_str = now.strftime("%Y-%m-%d")
#         time_str = now.strftime("%H:%M:%S")

#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()

#             for name in present_names:
#                 cursor.execute(
#                     "INSERT INTO attendance (fullName, time, attendance_status, className) VALUES (%s, %s, %s, %s)",
#                     (name, time_str, 'Present', self.class_name)
#                 )
            
#             connection.commit()
#             cursor.close()
#             connection.close()
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")

#     def mark_absent(self, detected_names):
#         undetected_names = set(self.known_face_names) - set(detected_names) - {"Unknown"}
#         now = datetime.now()
#         date_str = now.strftime("%Y-%m-%d")
#         time_str = now.strftime("%H:%M:%S")

#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()

#             for name in undetected_names:
#                 cursor.execute(
#                     "INSERT INTO attendance (fullName, time, attendance_status, className) VALUES (%s, %s, %s, %s)",
#                     (name, time_str, 'Absent', self.class_name)
#                 )
            
#             connection.commit()
#             cursor.close()
#             connection.close()
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")

#     def detect_faces(self):
#         detected_names = []
#         unknown_faces = self.fetch_unknown_faces()

#         for id, image_data in unknown_faces:
#             image = Image.open(BytesIO(image_data))
#             face_image = np.array(image)
#             face_locations = face_recognition.face_locations(face_image)
#             face_encodings = face_recognition.face_encodings(face_image, face_locations)

#             for face_encoding in face_encodings:
#                 matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
#                 name = "Unknown"
#                 face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
#                 best_match_index = np.argmin(face_distances)

#                 if matches[best_match_index]:
#                     name = self.known_face_names[best_match_index]

#                 detected_names.append(name)

#         self.mark_attendance(detected_names)
#         self.mark_absent(detected_names)
#         return detected_names

# if __name__ == "_main_":
#     import sys
#     import json

#     if len(sys.argv) < 2:
#         print("Usage: python face_reco.py <class_name>")
#         sys.exit(1)

#     class_name = sys.argv[1]
#     db_config = {
#         'host': "localhost",
#         'user': "root",
#         'password': "Pratham2807@",
#         'database': "presencepro"
#     }

#     try:
#         fr = FaceRecognition(db_config, class_name)
#         detected_names = fr.detect_faces()
#         print(f"Detected names: {detected_names}")
#     except Exception as e:
#         print(f"An error occurred: {e}")


# import mysql.connector
# from datetime import datetime
# from io import BytesIO
# from PIL import Image
# import face_recognition
# import numpy as np
# import pandas as pd
# import sys
# import json

# class FaceRecognition:
#     def __init__(self, db_config, class_name):
#         self.db_config = db_config
#         self.class_name = class_name
#         self.known_face_encodings = []
#         self.known_face_names = []
#         self.load_known_faces()

#     def load_known_faces(self):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()
#             cursor.execute("SELECT fullName, imageDb FROM images WHERE className = %s", (self.class_name,))
#             for name, image_data in cursor.fetchall():
#                 image = Image.open(BytesIO(image_data))
#                 face_image = np.array(image)
#                 face_encoding = face_recognition.face_encodings(face_image)[0]
#                 self.known_face_encodings.append(face_encoding)
#                 self.known_face_names.append(name)
#             cursor.close()
#             connection.close()
#             print("Known faces loaded.")
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")

#     def fetch_unknown_faces(self):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()
#             cursor.execute("SELECT id, imageDb FROM unknown_photos WHERE className = %s", (self.class_name,))
#             unknown_faces = cursor.fetchall()
#             cursor.close()
#             connection.close()
#             return unknown_faces
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
#             return []

#     def mark_attendance(self):
#         detected_names = set()  # Use a set to avoid duplicates
#         unknown_faces = self.fetch_unknown_faces()

#         for id, image_data in unknown_faces:
#             image = Image.open(BytesIO(image_data))
#             face_image = np.array(image)
#             face_locations = face_recognition.face_locations(face_image)
#             face_encodings = face_recognition.face_encodings(face_image, face_locations)

#             for face_encoding in face_encodings:
#                 matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
#                 name = "Unknown"
#                 face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
#                 best_match_index = np.argmin(face_distances)

#                 if matches[best_match_index]:
#                     name = self.known_face_names[best_match_index]

#                 if name not in detected_names:
#                     detected_names.add(name)

#         detected_names = list(detected_names)
#         absentees = self.mark_absent(detected_names)
#         self.save_attendance_to_db(detected_names, absentees)
#         return detected_names, absentees

#     def mark_absent(self, detected_names):
#         undetected_names = set(self.known_face_names) - set(detected_names) - {"Unknown"}
#         return list(undetected_names)

#     def save_attendance_to_db(self, detected_names, absentees):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()

#             now = datetime.now()
#             date_str = now.strftime("%Y-%m-%d")
#             time_str = now.strftime("%H-%M-%S")

#             # Insert attendance data into 'attendance' table
#             for name in detected_names:
#                 cursor.execute("INSERT INTO attendance (className, fullName, attendance_status, time) VALUES (%s, %s, %s, %s)",
#                                (self.class_name, name, 'Present', time_str))
#             for name in absentees:
#                 cursor.execute("INSERT INTO attendance (className, fullName, attendance_status, time) VALUES (%s, %s, %s, %s)",
#                                (self.class_name, name, 'Absent', time_str))

#             connection.commit()
#             cursor.close()
#             connection.close()
#             print("Attendance details saved to database.")

#         except mysql.connector.Error as err:
#             print(f"Error saving attendance to database: {err}")

#     def save_attendance_to_excel(self, detected_names, absentees):
#         try:
#             now = datetime.now()
#             date_str = now.strftime("%Y-%m-%d")
#             time_str = now.strftime("%H-%M-%S")
#             file_name = f"{self.class_name}_{date_str}_{time_str}.xlsx"

#             # Create DataFrame
#             df = pd.DataFrame({
#                 'Name': detected_names + absentees,
#                 'Status': ['Present'] * len(detected_names) + ['Absent'] * len(absentees),
#                 'Time': [time_str] * (len(detected_names) + len(absentees))
#             })

#             # Save to BytesIO object instead of saving to local file
#             excel_data = BytesIO()
#             df.to_excel(excel_data, index=False)
#             excel_data.seek(0)  # Move the pointer to the start of the stream

#             return excel_data

#         except Exception as e:
#             print(f"Error saving attendance to Excel: {e}")
#             return None

# # Main execution block
# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python face_reco.py <class_name>")
#         sys.exit(1)

#     class_name = sys.argv[1]
#     db_config = {
#         'host': "localhost",
#         'user': "root",
#         'password': "Pratham2807@",
#         'database': "presencepro"
#     }

#     try:
#         fr = FaceRecognition(db_config, class_name)
#         detected_names, absentees = fr.mark_attendance()
#         print(f"Detected names: {detected_names}")
#         print(f"Absentees: {absentees}")
#     except Exception as e:
#         print(f"An error occurred: {e}")



#Here is the code which is to work when i click on the markattendance button excel sheet is saved.

# import face_recognition
# import numpy as np
# import pandas as pd
# import mysql.connector
# from datetime import datetime
# from io import BytesIO
# from PIL import Image
# import os

# # Function to calculate face match confidence
# def face_confidence(face_distance, face_match_threshold=0.6):
#     range_val = (1.0 - face_match_threshold)   
#     linear_val = (1.0 - face_distance) / (range_val * 2.0)

#     if face_distance > face_match_threshold:
#         return f"{round(linear_val * 100, 2)}%"
#     else:
#         value = (linear_val + ((1.0 - linear_val) * pow((linear_val - 0.5) * 2, 0.2))) * 100
#         return f"{round(value, 2)}%"

# # Class for Face Recognition and Attendance
# class FaceRecognition:
#     def __init__(self, db_config, class_name):
#         self.db_config = db_config
#         self.class_name = class_name
#         self.known_face_encodings = []
#         self.known_face_names = []
#         self.load_known_faces()

#     # Method to load known faces from database
#     def load_known_faces(self):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()
#             cursor.execute("SELECT fullName, imageDb FROM images WHERE className = %s", (self.class_name,))
#             for name, image_data in cursor.fetchall():
#                 image = Image.open(BytesIO(image_data))
#                 face_image = np.array(image)
#                 face_encoding = face_recognition.face_encodings(face_image)[0]
#                 self.known_face_encodings.append(face_encoding)
#                 self.known_face_names.append(name)
#             cursor.close()
#             connection.close()
#             print("Known faces loaded.")
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
    
#     # Method to fetch unknown faces from database
#     def fetch_unknown_faces(self):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()
#             cursor.execute("SELECT id, imageDb FROM unknown_photos WHERE className = %s", (self.class_name,))
#             unknown_faces = cursor.fetchall()
#             cursor.close()
#             connection.close()
#             return unknown_faces
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
#             return []

#     # Method to mark attendance in Excel sheet
#     def mark_attendance(self, present_names, absentees):
#         now = datetime.now()
#         date_str = now.strftime("%Y-%m-%d")
#         time_str = now.strftime("%H-%M-%S")
#         file_name = f"{self.class_name}_{date_str}_{time_str}.xlsx"

#         # Create DataFrame
#         df = pd.DataFrame({
#             'Name': present_names + absentees,
#             'Status': ['Present'] * len(present_names) + ['Absent'] * len(absentees),
#             'Time': [time_str] * (len(present_names) + len(absentees))
#         })

#         # Save to Excel
#         df.to_excel(file_name, index=False)
#         print(f"Attendance marked and saved to {file_name}")
#         return file_name  # Return the filename for later use

#     # Method to mark absentees based on detected names
#     def mark_absent(self, detected_names):
#         undetected_names = set(self.known_face_names) - set(detected_names) - {"Unknown"}
#         return list(undetected_names)

#     # Method to detect faces and mark attendance
#     def detect_faces(self):
#         detected_names = set()  # Use a set to avoid duplicates
#         unknown_faces = self.fetch_unknown_faces()

#         for id, image_data in unknown_faces:
#             image = Image.open(BytesIO(image_data))
#             face_image = np.array(image)
#             face_locations = face_recognition.face_locations(face_image)
#             face_encodings = face_recognition.face_encodings(face_image, face_locations)

#             for face_encoding in face_encodings:
#                 matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
#                 name = "Unknown"
#                 face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
#                 best_match_index = np.argmin(face_distances)

#                 if matches[best_match_index]:
#                     name = self.known_face_names[best_match_index]

#                 if name not in detected_names:
#                     detected_names.add(name)

#         detected_names = list(detected_names)
#         absentees = self.mark_absent(detected_names)
#         attendance_file = self.mark_attendance(detected_names, absentees)
#         return attendance_file

# # Main execution block
# if __name__ == "__main__":
#     import sys
#     import json

#     if len(sys.argv) < 2:
#         print("Usage: python face_reco.py <class_name>")
#         sys.exit(1)

#     class_name = sys.argv[1]
#     db_config = {
#         'host' : 'aws-attendance.cz608aw60ypw.eu-north-1.rds.amazonaws.com',
#         'user': 'admin',
#         'password' : 'Pratham2807',
#         'database' : 'presencepro'
#     }

#     try:
#         fr = FaceRecognition(db_config, class_name)
#         attendance_file = fr.detect_faces()
#         print(f"Attendance marked successfully. Excel file: {attendance_file}")
#     except Exception as e:
#         print(f"An error occurred: {e}")


# import face_recognition
# import numpy as np
# import mysql.connector
# from datetime import datetime
# from io import BytesIO
# from PIL import Image
# import json

# # Class for Face Recognition and Attendance
# class FaceRecognition:
#     def __init__(self, db_config, class_name):
#         self.db_config = db_config
#         self.class_name = class_name
#         self.known_face_encodings = []
#         self.known_face_names = []
#         self.load_known_faces()

#     # Method to load known faces from database
#     def load_known_faces(self):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()
#             cursor.execute("SELECT fullName, imageDb FROM images WHERE className = %s", (self.class_name,))
#             for name, image_data in cursor.fetchall():
#                 image = Image.open(BytesIO(image_data))
#                 face_image = np.array(image)
#                 face_encoding = face_recognition.face_encodings(face_image)[0]
#                 self.known_face_encodings.append(face_encoding)
#                 self.known_face_names.append(name)
#             cursor.close()
#             connection.close()
#             print("Known faces loaded.")
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")

#     # Method to fetch unknown faces from database
#     def fetch_unknown_faces(self):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()
#             cursor.execute("SELECT id, imageDb FROM unknown_photos WHERE className = %s", (self.class_name,))
#             unknown_faces = cursor.fetchall()
#             cursor.close()
#             connection.close()
#             return unknown_faces
#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
#             return []

#     # Method to mark attendance in database
#     def mark_attendance(self, present_names, absentees):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()
#             now = datetime.now()

#             for name in present_names:
#                 cursor.execute("INSERT INTO attendance (fullName, time, attendance_status, className) VALUES (%s, %s, %s, %s)",
#                                (name, now, 'Present', self.class_name))

#             for name in absentees:
#                 cursor.execute("INSERT INTO attendance (fullName, time, attendance_status, className) VALUES (%s, %s, %s, %s)",
#                                (name, now, 'Absent', self.class_name))

#             connection.commit()
#             cursor.close()
#             connection.close()
#             print("Attendance marked in database.")
#             return True
#         except mysql.connector.Error as err:
#             print(f"Error marking attendance: {err}")
#             return False

#     # Method to mark absentees based on detected names
#     def mark_absent(self, detected_names):
#         try:
#             connection = mysql.connector.connect(**self.db_config)
#             cursor = connection.cursor()
#             cursor.execute("SELECT fullName FROM images WHERE className = %s", (self.class_name,))
#             known_names = [row[0] for row in cursor.fetchall()]
#             cursor.close()
#             connection.close()

#             undetected_names = set(known_names) - set(detected_names)
#             return list(undetected_names)
#         except mysql.connector.Error as err:
#             print(f"Error marking absentees: {err}")
#             return []

#     # Method to detect faces and mark attendance
#     def detect_faces(self):
#         detected_names = set()  # Use a set to avoid duplicates
#         unknown_faces = self.fetch_unknown_faces()

#         for id, image_data in unknown_faces:
#             image = Image.open(BytesIO(image_data))
#             face_image = np.array(image)
#             face_locations = face_recognition.face_locations(face_image)
#             face_encodings = face_recognition.face_encodings(face_image, face_locations)

#             for face_encoding in face_encodings:
#                 matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
#                 name = "Unknown"
#                 face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
#                 best_match_index = np.argmin(face_distances)

#                 if matches[best_match_index]:
#                     name = self.known_face_names[best_match_index]

#                 if name not in detected_names:
#                     detected_names.add(name)

#         detected_names = list(detected_names)
#         absentees = self.mark_absent(detected_names)
#         self.mark_attendance(detected_names, absentees)
#         return detected_names, absentees

# # Main execution block
# if __name__ == "__main__":
#     import sys

#     if len(sys.argv) < 2:
#         print("Usage: python face_reco.py <class_name>")
#         sys.exit(1)

#     class_name = sys.argv[1]
#     db_config = {
#         'host': "localhost",
#         'user': "root",
#         'password': "your_mysql_password",
#         'database': "presencepro"
#     }

#     try:
#         fr = FaceRecognition(db_config, class_name)
#         detected_names, absentees = fr.detect_faces()
#         print(json.dumps({"detected_names": detected_names, "absentees": absentees}))
#     except Exception as e:
#         print(f"An error occurred: {e}")


# import face_recognition
# import numpy as np
# from datetime import datetime
# from io import BytesIO
# from PIL import Image
# import pandas as pd
# import json

# class FaceRecognition:
#     def __init__(self, class_name):
#         self.class_name = class_name
#         self.known_face_encodings = []
#         self.known_face_names = []
#         self.load_known_faces()

#     def load_known_faces(self):
#         # Replace with actual database or file loading logic
#         self.known_face_names = ['John Doe', 'Jane Smith']  # Example known names
#         self.known_face_encodings = [
#             np.array([0.1, 0.2, 0.3]),  # Example face encodings
#             np.array([0.4, 0.5, 0.6])
#         ]

#     def fetch_unknown_faces(self):
#         # Replace with actual database or file loading logic
#         unknown_faces = [
#             (1, np.zeros((100, 100, 3), dtype=np.uint8)),  # Example unknown face data
#             (2, np.ones((100, 100, 3), dtype=np.uint8))
#         ]
#         return unknown_faces

#     def mark_attendance_dynamically(self, detected_names, absentees):
#         now = datetime.now()
#         date_str = now.strftime("%Y-%m-%d")
#         time_str = now.strftime("%H:%M:%S")

#         attendance_data = [
#             { 'Name': name, 'Date': date_str, 'Time': time_str, 'Status': 'Present' } if name in detected_names else
#             { 'Name': name, 'Date': date_str, 'Time': time_str, 'Status': 'Absent' }
#             for name in self.known_face_names
#         ]

#         df = pd.DataFrame(attendance_data)
#         excel_file = f"{self.class_name}_attendance.xlsx"
#         df.to_excel(excel_file, index=False)
#         print(f"Attendance marked and saved to {excel_file}")
#         return excel_file

#     def detect_faces(self):
#         detected_names = set()
#         unknown_faces = self.fetch_unknown_faces()

#         for id, image_data in unknown_faces:
#             image = Image.fromarray(image_data)
#             face_image = np.array(image)
#             face_locations = face_recognition.face_locations(face_image)
#             face_encodings = face_recognition.face_encodings(face_image, face_locations)

#             for face_encoding in face_encodings:
#                 matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
#                 name = "Unknown"
#                 face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
#                 best_match_index = np.argmin(face_distances)

#                 if matches[best_match_index]:
#                     name = self.known_face_names[best_match_index]

#                 if name not in detected_names:
#                     detected_names.add(name)

#         detected_names = list(detected_names)
#         absentees = list(set(self.known_face_names) - set(detected_names))
#         attendance_file = self.mark_attendance_dynamically(detected_names, absentees)
#         return attendance_file, detected_names, absentees

# # Main execution block
# if __name__ == "__main__":
#     import sys

#     if len(sys.argv) < 2:
#         print("Usage: python face_reco.py <class_name>")
#         sys.exit(1)

#     class_name = sys.argv[1]

#     try:
#         fr = FaceRecognition(class_name)
#         attendance_file, detected_names, absentees = fr.detect_faces()
#         print(json.dumps({"attendance_file": attendance_file, "detected_names": detected_names, "absentees": absentees}))
#     except Exception as e:
#         print(f"An error occurred: {e}")



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
