import cv2
import pickle
import os
import face_recognition
from firebase_admin import storage 
from firebase_admin import credentials
import firebase_admin 

cred = credentials.Certificate("attendance-system-fef55-firebase-adminsdk-glzwh-1464dda069.json")
firebase_admin.initialize_app(cred , {
  
  'databaseURL' : 'https://attendance-system-fef55-default-rtdb.firebaseio.com/',
  'storageBucket' : 'attendance-system-fef55.appspot.com'
})


def download_and_encode_images():
    encoded_images = []
    student_ids = []
    bucket = storage.bucket()
    blobs = bucket.list_blobs()  # Adjust the prefix as necessary
    print(blobs)
    for blob in blobs:
        if blob.name.endswith(('jpg', 'jpeg', 'png')):
            # Download the image
            local_filename = os.path.join('temp', blob.name.split('/')[-1])
            blob.download_to_filename(local_filename)

            # Read and encode the image
            img = cv2.imread(local_filename)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encoding = face_recognition.face_encodings(img_rgb)[0]

            # Store encoding and student ID (filename without extension)
            encoded_images.append(encoding)
            student_ids.append(os.path.splitext(blob.name.split('/')[-1])[0])

    return encoded_images, student_ids
  
  
  
print("encoding firebase data...")
encoded_images , student_ids = download_and_encode_images()
print("encoded images" , encoded_images)
print("studients id" , student_ids)
encoded_imagesWithStudent_ids = [encoded_images , student_ids]
pickle.dump(encoded_imagesWithStudent_ids , open('encodedFirebaseFile.p' , "wb"))
print("encoding complete")