import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {"databaseURL":"https://facialrecognition-b216d-default-rtdb.firebaseio.com/"})


ref = db.reference('Students')

data = {
    "18AG023529":
        {
            "name": "Ajayi Love",
            "major": "Linkedin Influencer",
            "starting_year": 2021,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "18CH024802":
        {
            "name": "Biodun-oyedepo temiloluwa",
            "major": "Business analyst",
            "starting_year": 2020,
            "total_attendance": 12,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "18CH024804":
        {
            "name": "Esekhile Faith",
            "major": "Machine Learning",
            "starting_year": 2020,
            "total_attendance": 6,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "18CH024805":
        {
            "name": " Rwang precious",
            "major": "Data Analytics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)