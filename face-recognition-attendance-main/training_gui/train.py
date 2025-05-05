import cv2
import numpy as np
from PIL import Image
import os

def train_model(dataset_path='dataset', model_save_path='trainer.yml'):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    def get_images_and_labels(path):
        image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
        face_samples = []
        ids = []

        for image_path in image_paths:
            # Convert image to grayscale
            PIL_img = Image.open(image_path).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')
            # Extract user ID from filename
            id = int(os.path.split(image_path)[-1].split('.')[1])
            faces = detector.detectMultiScale(img_numpy)

            for (x, y, w, h) in faces:
                face_samples.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)
        return face_samples, ids

    print("[INFO] Training faces. Please wait...")
    faces, ids = get_images_and_labels(dataset_path)
    recognizer.train(faces, np.array(ids))
    recognizer.write(model_save_path)
    print(f"[INFO] Model trained and saved as {model_save_path}")

# Example usage
train_model()
