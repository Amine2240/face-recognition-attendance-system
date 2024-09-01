import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("attendance-system-fef55-firebase-adminsdk-glzwh-1464dda069.json")
firebase_admin.initialize_app(cred , {
  
  'databaseURL' : 'https://attendance-system-fef55-default-rtdb.firebaseio.com/'
})

ref = db.reference("Students")

data = {
  "111111" : {
    "last_attendance_time" : "2024-08-31 17:36:50",
    "name" : "amine kadoum",
    "major" : "Computer Science",
    "starting_year" : 2022,
    "standing" : "G",
    "total_attendance" :40,
    "year" : 4
  },
  "321654" : {
    "last_attendance_time" : "2024-08-31 17:36:50",
    "name" : "moutaz hind",
    "major" : "robotics",
    "starting_year" : 2020,
    "standing" : "L",
    "total_attendance" :30,
    "year" : 2
  },
  "852741" : {
    "last_attendance_time" : "2024-08-31 17:36:50",
    "name" : "emly blunt",
    "major" : "action",
    "starting_year" : 2019,
    "standing" : "A",
    "total_attendance" :20,
    "year" : 1
  },
  "963852" : {
    "last_attendance_time" : "2024-08-31 17:36:50",
    "name" : "elon musk",
    "major" : "physics",
    "starting_year" : 2000,
    "standing" : "B",
    "total_attendance" :10,
    "year" : 5
  },
  
}

for key,value in data.items():
  ref.child(key).set(value)
