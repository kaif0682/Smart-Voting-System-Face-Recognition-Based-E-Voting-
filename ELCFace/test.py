from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch


# ---------------- SPEAK FUNCTION ----------------
def speak(text):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)


# ---------------- CAMERA SETUP ----------------
video = cv2.VideoCapture(0)

if not video.isOpened():
    print("Camera not detected")
    exit()


# ---------------- FACE DETECTOR ----------------
facedetect = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)


# ---------------- LOAD DATA ----------------
with open('data/names.pkl', 'rb') as f:
    LABELS = pickle.load(f)

with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)


# ---------------- TRAIN KNN ----------------
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)


# ---------------- BACKGROUND ----------------
imgBackground = cv2.imread("background.png")

# if image missing → create blank
if imgBackground is None:
    imgBackground = np.zeros((800, 1200, 3), dtype=np.uint8)


COL_NAMES = ['NAME', 'VOTE', 'DATE', 'TIME']


# ---------------- CHECK CSV ----------------
def check_if_exists(value):
    try:
        with open("Votes.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0] == value:
                    return True
    except FileNotFoundError:
        return False
    return False


# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = video.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Faster detection
    faces = facedetect.detectMultiScale(gray, 1.2, 3)

    output = None   # safe

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]

        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)

        name = output[0]

        # draw rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)

        cv2.putText(frame, name, (x, y-10),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

    # place camera on background
    imgBackground[370:370 + 480, 225:225 + 640] = frame

    cv2.imshow('Smart Election System', imgBackground)

    key = cv2.waitKey(1)

    # ---------------- SAFE EXIT ----------------
    if key == ord('q'):
        break

    # ---------------- IF FACE FOUND ----------------
    if output is not None:

        name = output[0]

        # already voted check
        if check_if_exists(name):
            speak("YOU HAVE ALREADY VOTED")
            time.sleep(2)
            break

        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")

        vote_map = {
            ord('1'): "BJP",
            ord('2'): "CONGRESS",
            ord('3'): "AAP",
            ord('4'): "NOTA"
        }

        if key in vote_map:
            party = vote_map[key]

            speak("YOUR VOTE HAS BEEN RECORDED")

            file_exists = os.path.isfile("Votes.csv")

            with open("Votes.csv", "a", newline='') as csvfile:
                writer = csv.writer(csvfile)

                if not file_exists:
                    writer.writerow(COL_NAMES)

                writer.writerow([name, party, date, timestamp])

            speak("THANK YOU FOR PARTICIPATING IN THE ELECTIONS")
            time.sleep(2)
            break


# ---------------- CLEANUP ----------------
video.release()
cv2.destroyAllWindows()
