""" webcam """

import os
import cv2
import pickle
import numpy as np
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://facialrecognition-b216d-default-rtdb.firebaseio.com/",
                                     "storageBucket": "facialrecognition-b216d.appspot.com"})

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # GRAPHICS DESCRIPTION
cap.set(4, 480)

'''load the encoding file'''

file = open("Encodefile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
encodeListKnown, studentIds = encodeListKnownWithIds
file.close()
# print(studentIds)
counter = 0
id = -1

while True:
    '''webcam show simultaneously with attendance system'''
    success, img = cap.read()

    imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    faceCurrFrame = face_recognition.face_locations(imgs)  # location of the face
    encodeCurrFrame = face_recognition.face_encodings(imgs, faceCurrFrame)  # Encoding of the face

    if faceCurrFrame:
        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("match Index", matchIndex)

            if matches[matchIndex]:
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 10 + x1, 20 + y1, x2 - x1, y2 - y1
                img = cvzone.cornerRect(img, bbox, rt=0)

                id = studentIds[matchIndex]
                if counter == 0:
                    counter = 1

            else:
                print("Not eligible to take cafteria food")

        if counter != 0:
            if counter == 1:
                # Get the Data
                studentInfo = db.reference(f'Students/{id}').get()
                # print("Eligible to take cafteria food")
                # print(studentInfo)
                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                # print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    counter = 0
                counter += 1

    else:
        counter = 0
    print("Eligible to take cafteria food")
    print(studentInfo)

    cv2.imshow("Face Recognition", img)
    cv2.waitKey(1)


