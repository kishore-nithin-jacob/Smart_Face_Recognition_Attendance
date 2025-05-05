import cv2
import json
import numpy as np

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
