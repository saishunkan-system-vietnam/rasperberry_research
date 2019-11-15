import cv2
import numpy as np
from PIL import Image
import os
import encode_face as encode
# Path for face image database
path = 'dataSet'
recognizer = cv2.face.LBPHFaceRecognizer_create();
#recognizer.setThreshold(3000)
detector = cv2.CascadeClassifier('/home/pi/Desktop/face/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
# function to get the images and label data
def getImagesAndLabels():
    encode.encode_face()
    """print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    ids = []
    faceSamples = []
    #vector<Mat> images;
    
    for imagePath in imagePaths:
        images= [os.path.join(imagePath,f) for f in os.listdir(imagePath)]
        for image in images:
          #faceImg=Image.open(image).convert('L');
          #faceNp=np.array(faceImg,'uint8')
          #faceSamples.append(faceNp)
          id = int(os.path.split(image)[-1].split(".")[1])
          PIL_img = Image.open(image).convert('L') # convert it to grayscale
          img_numpy = np.array(PIL_img,'uint8')
          id = int(os.path.split(image)[-1].split(".")[1])
          faces = detector.detectMultiScale(img_numpy)
          for (x,y,w,h) in faces:
              faceSamples.append(img_numpy[y:y+h,x:x+w])
              ids.append(id)
            
    #recognizer.train(faceSamples, np.array(ids))
    recognizer.train(faceSamples, np.array(ids))
    recognizer.write('/home/pi/Desktop/face/face_recognition/trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi
    # Print the numer of faces trained and end program
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))"""
    
    
getImagesAndLabels()
