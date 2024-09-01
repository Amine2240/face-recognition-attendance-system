import cv2
import os
import pickle
import face_recognition
import numpy as np
from firebase_admin import db
from firebase_admin import credentials
import firebase_admin
from datetime import datetime , timedelta
import time

cred = credentials.Certificate("attendance-system-fef55-firebase-adminsdk-glzwh-1464dda069.json")
firebase_admin.initialize_app(cred , {
  
  'databaseURL' : 'https://attendance-system-fef55-default-rtdb.firebaseio.com/'
})

imgBackground = cv2.imread('./Resources/background.png')

cap = cv2.VideoCapture(0)
cap.set(3 , 640) #width
cap.set(4 , 480) #height

modespath = './Resources/Modes'
modesPathList = os.listdir(modespath)
# print(modesPathList)
imgsModesList = []
for path in modesPathList:
  imgsModesList.append(cv2.imread(os.path.join(modespath , path)))


encodedimagesWithIds = pickle.load(open('encodedFirebaseFile.p' , "rb"))
encodedimages , studentIds = encodedimagesWithIds
# print("encodedimage :" , encodedimages)
# print("studentIds :" , studentIds)

imagesfromDbFolder = './temp'
imagesfromDb = os.listdir(imagesfromDbFolder)
imagesList = []
for path in imagesfromDb:
  imagesList.append(cv2.imread(os.path.join(imagesfromDbFolder , path)))
print( "images from db : ",imagesfromDb)

ref = db.reference("Students")
studentsData = ref.get()
start_time = None
while True:
  markedbool = False
  alreadyMarkedBool = False
  matchindex = -1
  success,frame = cap.read()
  frameS = cv2.resize(frame , (0,0) , None , 0.25 , 0.25 )
  frameS = cv2.cvtColor(frameS , cv2.COLOR_BGR2RGB)
  facesFromframeS = face_recognition.face_locations(frameS) # returns list of face coordinates (if there are multiple faces in the frame ) (top , right , left , bottom)
  encodedfacesFromframeS = face_recognition.face_encodings(frameS , facesFromframeS)
  print("face location : ", facesFromframeS)
  for encodedface , faceLocation in zip(encodedfacesFromframeS , facesFromframeS):
    matches = face_recognition.compare_faces(encodedimages , encodedface)
    faceDist = face_recognition.face_distance(encodedimages , encodedface)
    print(matches)
    print(faceDist)
    matchindex = np.argmin(faceDist)
    
    # matches[matchindex] will be equal to true
    y1 , x2 , y2 , x1 = faceLocation
    y1 , x2 , y2 , x1 = y1*4 , x2*4 , y2*4 , x1*4
    # bbox =  ,  ,  x2-x1, y2-y1   
    pt1 = ( x1, y1)  # Top-left corner
    pt2 = ( x2, y2)  # Bottom-right corner
    
    textposition = (pt1[0] ,pt1[1] - 10 )
    if matches[matchindex]:
      color = (0, 255, 0)  # Green color in BGR format
      frame = cv2.rectangle(frame , pt1 , pt2  ,color , thickness=2)
      frame = cv2.putText(frame , studentsData[studentIds[matchindex]]['name'] , textposition, cv2.FONT_HERSHEY_COMPLEX , 1 , color , 2 , cv2.LINE_AA)
      print("studentsid matchindex",studentsData[studentIds[matchindex]]['name'])
      # studentsData[studentIds[matchindex]]['total_attendance'] += 1
      # Get a reference to the specific node you want to update
      ref2 = db.reference(f'Students/{studentIds[matchindex]}')

      # Update multiple fields
      formatted_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      # Convert the last attendance time from string to datetime
      last_attendance_time_str = studentsData[studentIds[matchindex]]['last_attendance_time']
      last_attendance_time = datetime.strptime(last_attendance_time_str, "%Y-%m-%d %H:%M:%S")
      if datetime.now() - last_attendance_time > timedelta(seconds=15):
        ref2.update({
          'total_attendance' : studentsData[studentIds[matchindex]]['total_attendance'] + 1,
          'last_attendance_time' : formatted_now
        })
        ref = db.reference("Students")
        studentsData = ref.get()
        markedbool = True
        alreadyMarkedBool =False
      else:
        print('not yet 15 seconds since the last attendance')  
        alreadyMarkedBool = True
        
      
    else:
      color = (0, 0, 255)  # red color in BGR format
      frame = cv2.rectangle(frame , pt1 , pt2  ,color , thickness=2)
      frame = cv2.putText(frame , 'unknown' , textposition , cv2.FONT_HERSHEY_COMPLEX , 1 , color , 2 , cv2.LINE_AA)

        
  
  # print("facesfromframes : " , facesFromframeS)
  # print('encodedfacesfromframeS :' , encodedfacesFromframeS)
  imgBackground[162:162 + 480 , 55:55 + 640] = frame
  if  len(facesFromframeS) == 0:
    imgBackground[44:44 + 633 , 808:808 + 414] = imgsModesList[0]
  else:
    if alreadyMarkedBool:
      imgBackground[44:44 + 633 , 808:808 + 414] = imgsModesList[3]
    else:
      imgBackground[44:44 + 633 , 808:808 + 414] = imgsModesList[1]
      if (matchindex != -1):
        imgBackground[170:170 + 220 , 905:905 + 220] = cv2.resize(imagesList[matchindex] , (220,220))
        cv2.putText(imgBackground, str(studentsData[studentIds[matchindex]]['total_attendance']) , (850 , 120) , cv2.FONT_HERSHEY_COMPLEX , 1 , (255 , 255,255) , 2 )
        cv2.putText(imgBackground, str(studentsData[studentIds[matchindex]]['name']) , (920 , 430) , cv2.FONT_HERSHEY_COMPLEX , 1 , (0 , 0,0) , 2 )
        cv2.putText(imgBackground, str(studentIds[matchindex]) , (980 , 500) , cv2.FONT_HERSHEY_COMPLEX , 1 , (255 , 255,255) , 2 )
        cv2.putText(imgBackground, str(studentsData[studentIds[matchindex]]['major']) , (980 , 560) , cv2.FONT_HERSHEY_COMPLEX , 0.5 , (255, 255,255) , 2 )
        cv2.putText(imgBackground, str(studentsData[studentIds[matchindex]]['starting_year']) , (1100 , 620 ) , cv2.FONT_HERSHEY_COMPLEX , 1 , (0 , 0,0) , 2 )
        cv2.putText(imgBackground, str(studentsData[studentIds[matchindex]]['year']) , (1010 , 620) , cv2.FONT_HERSHEY_COMPLEX , 1 , (0 , 0,0) , 2 )
        cv2.putText(imgBackground, str(studentsData[studentIds[matchindex]]['standing']) , (900 , 620) , cv2.FONT_HERSHEY_COMPLEX , 1 , (0 , 0,0) , 2 )

  cv2.imshow("face attendance",imgBackground)
  cv2.waitKey(1)
  
  
  
