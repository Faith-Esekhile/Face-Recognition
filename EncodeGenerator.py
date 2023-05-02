import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://facialrecognition-b216d-default-rtdb.firebaseio.com/",
                                     "storageBucket": "facialrecognition-b216d.appspot.com"})

# importing students images
folderPath = "Images"
pathList = os.listdir(folderPath)
# print(pathList)
imgList = []
studentIDs = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    # print(path)
    studentIDs.append(os.path.splitext(path)[0])

    fileNames = f"{folderPath}/{path}"
    bucket = storage.bucket()
    blob = bucket.blob(fileNames)
    blob.upload_from_filename(fileNames)

    # print((os.path.splitext(path)[0]))
#print(studentIDs)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

#print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
#print(encodeListKnown)
encodeListKnownWithIds = [encodeListKnown,studentIDs]
#print("Encoding Complete")

file = open("EncodeFile.p","wb")
pickle.dump(encodeListKnownWithIds,file)
file.close()
#print("File Saved")

