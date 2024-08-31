import cv2
import pickle
import os
import face_recognition

imagesPath = './Images'
pathList = os.listdir(imagesPath)
print(pathList)
imagesList = []
studentIds = []

for path in pathList:
  imagesList.append(cv2.imread(os.path.join(imagesPath , path)))
  studentIds.append(os.path.splitext(path)[0])
  

def encodeImgs(imagesList):
  encodedImgs = []
  for img in imagesList:
    image = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(image)
    if encodings:
      encodedImgs.append(encodings[0])
    else:
      print("no face detected")
    
  return encodedImgs

print("encoding start ...")
encodedimages = encodeImgs(imagesList)
encodedimagesWithIds = [encodedimages , studentIds]
print(encodedimages)
print("encoding complete")

pickle.dump(encodedimagesWithIds , open('encodedfile.p',"wb"))
print("file saved")