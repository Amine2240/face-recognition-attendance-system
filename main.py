import cv2
import os
import pickle
import face_recognition
import numpy as np

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


encodedimagesWithIds = pickle.load(open('encodedfile.p' , "rb"))
encodedimages , studentIds = encodedimagesWithIds
# print("encodedimage :" , encodedimages)
# print("studentIds :" , studentIds)
while True:
  success,frame = cap.read()
  frameS = cv2.resize(frame , (0,0) , None , 0.25 , 0.25 )
  frameS = cv2.cvtColor(frameS , cv2.COLOR_BGR2RGB)
  facesFromframeS = face_recognition.face_locations(frameS) # returns list of face coordinates (if there are multiple faces in the frame ) (top , right , left , bottom)
  encodedfacesFromframeS = face_recognition.face_encodings(frameS , facesFromframeS)
  
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
    if matches[matchindex]:
      color = (0, 255, 0)  # Green color in BGR format
      frame = cv2.rectangle(frame , pt1 , pt2  ,color , thickness=2)
    else:
      color = (0, 0, 255)  # red color in BGR format
      frame = cv2.rectangle(frame , pt1 , pt2  ,color , thickness=2)
        
  
  # print("facesfromframes : " , facesFromframeS)
  # print('encodedfacesfromframeS :' , encodedfacesFromframeS)
  imgBackground[162:162 + 480 , 55:55 + 640] = frame
  imgBackground[44:44 + 633 , 808:808 + 414] = imgsModesList[2]
  cv2.imshow("face attendance",imgBackground)
  cv2.waitKey(1)
  
  
  
