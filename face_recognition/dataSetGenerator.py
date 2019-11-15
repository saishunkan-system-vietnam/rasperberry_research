from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import pickle
import time
import cv2
import os
import train
import sqlite3
def insertOrUpdate(name):
    #connecting to the db
    conn =sqlite3.connect("face_base.db")
    query="INSERT INTO people ( name ) VALUES ('" + str(name) + "')"
    conn.execute(query)
    conn.commit()
    conn.close()
    
def getId():
    conn =sqlite3.connect("face_base.db")
    query="SELECT MAX(id) from people"
    cursor = conn.execute(query)
    id_people = 0
    for row in cursor:
        print(row)
        if row[0] is None:
          id_people = 1
        else:
          id_people = int(row[0]) + 1
    conn.close()
    return id_people
    
def createForderImage(name):
    data = name.split()
    names = []
    for idx, val in enumerate(data):
      if(idx == (len(data) -1 )):
       names.insert(0,val.capitalize())
      else:
        names.append(val.capitalize()[0])
    image_path = "dataSet/" + ''.join(names)
    if not os.path.exists(image_path):
      os.makedirs(image_path)
    return image_path

# initialize the video stream, then allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# start the FPS throughput estimator
fps = FPS().start()
face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/face/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
face_name = input("\n Enter user Name :")
face_id = getId()
count = 0
image_forder = createForderImage(face_name)
# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream
	frame = vs.read()
	# resize the frame to have a width of 600 pixels (while
	# maintaining the aspect ratio), and then grab the image
	# dimensions
	frame = imutils.resize(frame, width=600)
	(h, w) = frame.shape[:2]
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	#Look for faces in the image using the loaded cascade file
	faces = face_cascade.detectMultiScale(frame, scaleFactor = 1.2, minNeighbors = 5, minSize = (100, 100), flags = cv2.CASCADE_SCALE_IMAGE)
	#Draw a rectangle around every found face
	for (x,y,w,h) in faces:
		roi_gray = gray[y:y + h, x:x + w]
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
	#Save the result image
	if len(faces):
		count = count + 1
		img_item = image_forder +"/User."+ str(face_id) + '.' + str(count) + ".jpg"
		cv2.imwrite(img_item,roi_gray)
	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
	if count == 100:
		insertOrUpdate(face_name)
		train.getImagesAndLabels()
		exit();
        
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()