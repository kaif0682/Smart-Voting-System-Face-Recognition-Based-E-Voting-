import cv2
import pickle
import numpy as np
import os


# ---------------- CREATE DATA FOLDER ----------------
if not os.path.exists('data'):
    os.makedirs('data')


# ---------------- CAMERA ----------------
video = cv2.VideoCapture(0)

if not video.isOpened():
    print("Camera not detected")
    exit()


# ---------------- FACE DETECTOR ----------------
facedetect = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)


faces_data = []
sample_count = 0

name = input("Enter your Aadhar number: ")


# ---------------- CAPTURE LOOP ----------------
while True:
    ret, frame = video.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # faster detection
    faces = facedetect.detectMultiScale(gray, 1.2, 3)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]

        resized_img = cv2.resize(crop_img, (50, 50))

        faces_data.append(resized_img)
        sample_count += 1

        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)

        cv2.putText(frame,
                    f"Samples: {sample_count}/100",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2)

    cv2.imshow('Register Face', frame)

    key = cv2.waitKey(1)

    # stop when 100 samples collected or q pressed
    if key == ord('q') or sample_count >= 100:
        break


# ---------------- CLEANUP ----------------
video.release()
cv2.destroyAllWindows()


# ---------------- CHECK MINIMUM DATA ----------------
if len(faces_data) == 0:
    print("No face captured. Try again.")
    exit()


# ---------------- PROCESS DATA ----------------
faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape((len(faces_data), -1))


# ---------------- SAVE NAMES ----------------
names_path = 'data/names.pkl'
faces_path = 'data/faces_data.pkl'

names = [name] * len(faces_data)

if os.path.exists(names_path):
    with open(names_path, 'rb') as f:
        old_names = pickle.load(f)
    names = old_names + names

with open(names_path, 'wb') as f:
    pickle.dump(names, f)


# ---------------- SAVE FACE DATA ----------------
if os.path.exists(faces_path):
    with open(faces_path, 'rb') as f:
        old_faces = pickle.load(f)
    faces_data = np.append(old_faces, faces_data, axis=0)

with open(faces_path, 'wb') as f:
    pickle.dump(faces_data, f)


print("✅ Face registered successfully!")
print("Total samples saved:", len(faces_data))
