import cv2
import os
import json

def add_name_to_json(file_path, user_id, user_name):
    # Load existing data
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Add or update entry
    data[str(user_id)] = user_name  # use str keys for JSON compatibility

    # Write back to file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"[INFO] Added/Updated: {user_id} → {user_name}")

# Example usage
def capture_faces(user_id, user_name, save_dir='dataset'):
    # Load Haar cascade with error check
    face_cascade_path = 'haarcascade_frontalface_default.xml'
    if not os.path.exists(face_cascade_path):
        print(f"[ERROR] Haar cascade not found at {face_cascade_path}")
        return
    face_cascade = cv2.CascadeClassifier(face_cascade_path)

    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # Set width
    cam.set(4, 480)  # Set height

    count = 0
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print("[INFO] Starting face capture. Look at the camera...")

    while True:
        ret, frame = cam.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Equalize histogram to improve contrast
        gray = cv2.equalizeHist(gray)

        # Adjust scaleFactor and minNeighbors for better accuracy
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,  # Try 1.05 for more sensitive detection
            minNeighbors=5,   # Increase to 6-7 to reduce false positives
            minSize=(100, 100)  # Ignore small detections
        )

        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            filename = f"{save_dir}/User.{user_id}.{count}.jpg"
            cv2.imwrite(filename, face_img)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Capturing Faces', frame)
        if cv2.waitKey(1) & 0xFF == 27 or count >= 300:  # ESC or 100 images
            break

    print(f"[INFO] Collected {count} face images for user: {user_name}")
    cam.release()
    cv2.destroyAllWindows()
    add_name_to_json('names.json', user_id, user_name)


# Example usage
#capture_faces(user_id='21', user_name='name')
