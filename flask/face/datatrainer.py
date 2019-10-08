import time
import cv2
import os
import numpy as np
from PIL import Image

dir_path = os.path.dirname(os.path.realpath(__file__))
#Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier(dir_path + '/xml/haarcascade_frontalface_default.xml')

def training():
    path = dir_path + "/dataSet"
    faces,ids = getImagesAndLabels(path)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(ids))
    # Save the model into trainer/trainer.yml
    recognizer.write(dir_path + '/trainer/trainer.yml') 

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = face_cascade.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids
