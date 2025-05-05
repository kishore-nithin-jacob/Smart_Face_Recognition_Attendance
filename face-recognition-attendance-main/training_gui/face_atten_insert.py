import cv2
import json
import numpy as np
from pymongo import MongoClient
from datetime import datetime
import pytz

# Get the current date and time
now = datetime.now()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Update if needed
db = client["attendance"]
collection = db["students"]
periods=db["periods"]
allperiods = periods.find({}, {'_id': 0, 'time.start': 1, 'time.end': 1,'period':1})

# Initialize an empty list to store the extracted times and comparisons
records = []
# Get the current system time in UTC
current_time_utc = datetime.utcnow()

# Convert UTC time to IST (Indian Standard Time)
ist_time_zone = pytz.timezone('Asia/Kolkata')
current_time_ist = current_time_utc.replace(tzinfo=pytz.utc).astimezone(ist_time_zone)
subject=''
# Loop through all documents and extract start_time and end_time
for doc in allperiods:
    start_time_str = doc.get('time', {}).get('start')
    end_time_str = doc.get('time', {}).get('end')
    period = doc.get('period')
    # Convert start_time string from 'T10:45:33Z' to a time object
    start_time = datetime.strptime(start_time_str, "T%H:%M:%SZ").time()
    end_time = datetime.strptime(end_time_str, "T%H:%M:%SZ").time()
    # Compare current system time (in IST) with the start time
    if current_time_ist.time() > start_time and current_time_ist.time()<end_time:
        subject=period
        break

# Load names from a JSON file
with open("names.json", "r") as f:
    names = json.load(f)
    # Convert keys to integers since JSON stores them as strings
    names = {int(k): v for k, v in names.items()}

# Load face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# Load Haar cascade
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Start webcam
cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        if confidence < 70:
            name = names.get(id_, "Unknown")
            label = f"{name} ({round(100 - confidence)}%)"
            color = (0, 255, 0)
            print(f"{name} ({round(100 - confidence)}%)")
            print(id_)
            print(subject)
            if confidence < 80:
                print(id_)
                # Data to insert/update
                data = {
                    "student_id": id_,
                    "course_id": 201,
                    "date": "2025-04-29",
                    "period": 2,
                    "time": {
                        "start": start_time_str,
                        "end": end_time_str
                    },
                    "status": "Present"
                }

                # Define a composite filter to uniquely identify the document
                filter_query = {
                    "student_id": data["student_id"],
                    "course_id": data["course_id"],
                    "date": data["date"],
                    "time": data["time"],
                    "period": data["period"]
                }

                # Define update operation (replace or update fields)
                update_data = {"$set": data}

                # Perform upsert (insert if not exists, update if exists)
                result = collection.update_one(filter_query, update_data, upsert=True)

                # Feedback
                if result.matched_count > 0:
                    print("Document updated.")
                elif result.upserted_id:
                    print(f"New document inserted with _id: {result.upserted_id}")
                else:
                    print("No changes made.")
        else:
            label = "Unknown"
            color = (0, 0, 255)
            
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y-10), font, 0.8, color, 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(10) & 0xFF == 27:  # ESC to quit
        break

cam.release()
cv2.destroyAllWindows()
