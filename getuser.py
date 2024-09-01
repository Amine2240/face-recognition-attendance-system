import firebase_admin
from firebase_admin import credentials
import pickle

cred = credentials.Certificate("attendance-system-fef55-firebase-adminsdk-glzwh-1464dda069.json")
firebase_admin.initialize_app(cred , {
  
  'databaseURL' : 'https://attendance-system-fef55-default-rtdb.firebaseio.com/'
})



# encodedimages , students_ids = pickle.load(open('encodedFirebaseFile.p' , "rb"))

