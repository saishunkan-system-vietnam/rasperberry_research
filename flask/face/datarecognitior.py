import time
import cv2
import os
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
#Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier(dir_path + '/xml/haarcascade_frontalface_default.xml')

#use Local Binary Patterns Histograms
recognizer = cv2.face.LBPHFaceRecognizer_create()

if os.path.exists(dir_path + '/trainer/trainer.yml'):
        #Load a trainer file
    recognizer.read(dir_path + '/trainer/trainer.yml')


def recognition(frame):
    id = None
    ids = []
    font = cv2.FONT_HERSHEY_SIMPLEX
    # convert frame to array
    image = frame.copy()
    #Convert to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #Look for faces in the image using the loaded cascade file
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5, minSize = (100, 100), flags = cv2.CASCADE_SCALE_IMAGE)
    #Draw a rectangle around every found face
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            ids.append(id)
        else:
            ids.append(0)

    return np.unique(ids), image
