import time
import cv2
import os
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
#Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier(dir_path + '/xml/haarcascade_frontalface_default.xml')

def data_generate_face(frame, count, face_id, savetitem = True):

	# convert frame to array
	image = frame.copy()
	#Convert to grayscale
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	#Look for faces in the image using the loaded cascade file
	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)
	#Draw a rectangle around every found face
	for (x,y,w,h) in faces:
		roi_gray = gray[y:y + h, x:x + w]
		cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
	#Save the result image
	if len(faces):
		if savetitem:
			pathdir = dir_path + "/dataSet/" + str(face_id)
			if os.path.isdir(pathdir) == False:
				os.mkdir(pathdir)
			img_item = pathdir + "/" + str(count).zfill(5) + ".jpg"
			cv2.imwrite(img_item,frame)
			count = count + 1
	return count, image