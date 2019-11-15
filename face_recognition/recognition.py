#from picamera.array import PiRGBArray
#from picamera import PiCamera
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import cv2
import sqlite3
import face_recognition
import time
import pickle
import imutils
from collections import defaultdict
import _thread
from sensor.ledSensor import *
from imutils import face_utils
import dlib

FACIAL_LANDMARKS_IDXS = OrderedDict([
	("mouth", (48, 68)),
	("right_eyebrow", (17, 22)),
	("left_eyebrow", (22, 27)),
	("right_eye", (36, 42)),
	("left_eye", (42, 48)),
	("nose", (27, 36)),
	("jaw", (0, 17))
])

def turn_aspect_ratio(x1,x2,x3):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(x1, x2)
	B = dist.euclidean(x2, x3)

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	#C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	# ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return A/B

def open_mouth_detection(x1,x2,x3,x4):
	A = dist.euclidean(x1, x2)
	B = dist.euclidean(x3, x4)

	return A/B

def rect_to_bb(rect):
	# take a bounding predicted by dlib and convert it
	# to the format (x, y, w, h) as we would normally do
	# with OpenCV
	x = rect.left()
	y = rect.top()
	w = rect.right() - x
	h = rect.bottom() - y

	# return a tuple of (x, y, w, h)
	return (x, y, w, h)

def shape_to_np(shape, dtype="int"):
	# initialize the list of (x, y)-coordinates
	coords = np.zeros((68, 2), dtype=dtype)

	# loop over the 68 facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for i in range(0, 68):
		coords[i] = (shape.part(i).x, shape.part(i).y)

	# return the list of (x, y)-coordinates
	return coords
 
def getProfile(id):
    #connecting to the db
    conn =sqlite3.connect("face_base.db")
    #check if id already exists
    query = "SELECT * FROM people WHERE ID="+str(id)
    #returning the data in rows
    cursor = conn.execute(query)
    profile=None
    for row in cursor:
        profile = row
    conn.close()
    return profile 



#recognizer = cv2.face.LBPHFaceRecognizer_create()
#recognizer.setThreshold(3000)
#Load a trainer file
#recognizer.read('/home/pi/Desktop/face/face_recognition/trainer/trainer.yml')
#Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/face/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
data = pickle.loads(open("encodings.pickle", "rb").read())

font = cv2.FONT_HERSHEY_SIMPLEX
#iniciate id counter
id = 0
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

predictor  = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def detectFace(faces,frame,gray,rect,key_pattern):
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in faces]
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []
    name = "Unknown"
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],encoding)
        name = "Unknown"
        #check to see if we have found a match
        """if True in matches:
        # find the indexes of all matched faces then initialize a
        # dictionary to count the total number of times each face
        # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            print("matchedIdxs: ")
            print(matchedIdxs)
            counts = {}

        # loop over the matched indexes and maintain a count for
        # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

        # determine the recognized face with the largest number
        # of votes (note: in the event of an unlikely tie Python
        # will select first entry in the dictionary)
            name = max(counts, key=counts.get)"""
        face_distances = face_recognition.face_distance(data["encodings"], encoding)
        #best_match_index = np.argmin(face_distances)
        #if matches[best_match_index]:
          #name = data["names"][best_match_index]
        if np.any(face_distances <= 0.4):
          best_match_idx = np.argmin(face_distances)
          if matches[best_match_idx]:
            name = data["names"][best_match_idx]
        else:
          name = "Unknown"
        names.append(name)
        #Draw a rectangle around every found face
    #similarity, max_similarity = update_and_verify_blink_pattern(face_shape_predictor, frame, gray, rect, key_pattern)
    #print("similarity: " + str(similarity) + "max_similarity: " + str(max_similarity))
    for ((top, right, bottom, left), name) in zip(boxes, names):
      # draw the predicted face name on the image
        if(name != "Unknown"):
          cv2.rectangle(frame, (left, top), (right, bottom),(0, 255, 0), 2)
          y = top - 15 if top - 15 > 15 else top + 15
          cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
        else:
          cv2.rectangle(frame, (left, top), (right, bottom),(0,0 , 255), 2)
          y = top - 15 if top - 15 > 15 else top + 15
          cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 0, 255), 2)

# start the FPS throughput estimator
fps = FPS().start()
liveliness_pattern = list("x")
unique = np.unique(liveliness_pattern)
idx = np.array(liveliness_pattern) == 'x'
key = np.zeros(shape=(len(liveliness_pattern),))
key[idx] = 1
key_pattern = KeyPattern(key, 20)
while True:
    # convert frame to array
    #image = frame.array
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    #Convert to grayscale
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #Look for faces in the image using the loaded cascade file
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5,minSize=(100, 100),flags=cv2.CASCADE_SCALE_IMAGE)
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)
    lips_ratio = open_mouth_detection(shape[62],shape[66],shape[49],shape[59])
    if lips_ratio>0.32:
      print("Mouth Open")
    else:
      print("Mouth Close")
    #if len(faces) > 0:
      #rect_sizes = np.array(map(lambda x: x[2] * x[3], faces))
      #rect = faces[rect_sizes.argmax()]
      #detectFace(faces,frame,gray,rect,key_pattern)
    #setColor(len(faces))
    # deep learning 
          
        
    """for (x,y,w,h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        id, confidence = recognizer.predict(roi_gray)
        print("confidence: " + str(confidence) + "ID: " + str(id) + "Names: " + str(name))
        profile = None
        if (confidence < 75 and name != 'Unknown'):
            profile = getProfile(id)
        if(profile!=None):
            cv2.putText(frame, str(profile[1]), (x+5,y-5), font, 1, (255,255,255), 2)
        else:
            cv2.putText(frame, "UnKnowed", (x+5,y-5), font, 1, (255,255,255), 2)"""
    # display a frame    
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xff == ord("q"):
      destroy()
      exit()
      
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()