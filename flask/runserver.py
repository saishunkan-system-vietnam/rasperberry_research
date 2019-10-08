# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 8000

# import the necessary packages
from imutils.video import VideoStream
from flask import Flask, render_template, session, request, \
    copy_current_request_context, Response
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import threading
import argparse
import datetime
import imutils
import time
import cv2
import uuid
import sqlite3
import json
from face import datagenerator, datatrainer, datarecognitior
import base64
import numpy as np
from sensorlib import tempandhumldty as temphum

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()
async_mode = None
# initialize a flask object
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
# initialize the video stream and allow the camera sensor to
# warmup
vs = VideoStream(usePiCamera=1).start()
#vs = VideoStream(src=0).start()
time.sleep(2.0)
count = None
ids = None

@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html", async_mode=socketio.async_mode)

@socketio.on('connect')
def connect():
    emit('sid_response', {'data': request.sid, 'count': 0})

@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)

    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/data_generate_face/<sid>/<persion_id>")
def data_generate_face(sid, persion_id):
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate_face(persion_id, sid),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/recognition/<sid>")
def recognition(sid):
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate_recognition(sid),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

@socketio.on('tempandhumldty')
def tempandhumldty():
    while True:
        result = temphum.read_dht11_dat()
        if result:
            humidity, temperature = result
            emit('tempandhumldty_response', {'data': { 'humidity': humidity, 'temperature': temperature}, 'count': 0})
        time.sleep(1)

@socketio.on('persion_add')
def persion_add(message):
    session['receive_count'] = session.get('receive_count', 0) + 1

    con = sqlite3.connect("sensor.db")
    msg = None
    first_name = None
    last_name = None
    persion_id = None
    try:
        data = message['data']
        first_name = data['first_name']
        last_name = data['last_name']
        persion_id = data['persion_id']
        cur = con.cursor()
        if persion_id == '0':
           persion_id = str(uuid.uuid4()).replace('-','')
           cur.execute("INSERT INTO people (persion_id,first_name,last_name) VALUES (?,?,?)",(persion_id,first_name,last_name) )
        else:
           cur.execute("UPDATE people set first_name = ? , last_name = ? WHERE persion_id = ?",(first_name,last_name,persion_id) )
        con.commit()
        msg = "success"
    except:
        con.rollback()
        msg = "error in operation"
    finally:
        con.close()
        emit('persion_add_response',
             {'data': {'persion_id' : persion_id}, 'count': session['receive_count'], 'status': msg})

def detect_motion(frameCount):
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock

    total = 0

    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()
        
def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

def generate_face(persion_id, sid):
    # grab global references to the output frame and lock variables
    global outputFrame, lock, count, socketio
    count = 0
    con = sqlite3.connect("sensor.db")
    cur = con.cursor()
    cur.execute("SELECT id FROM people WHERE persion_id = ?",(persion_id, ) )
    p_data = cur.fetchone()
    (p_id,) = p_data
    con.close()

    while True:
        # wait until the lock is acquired
        with lock:
            count, imageFrame = datagenerator.data_generate_face(outputFrame.copy(), count, p_id, savetitem = True)
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if imageFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", imageFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue
            #wait for 'q' key was pressed and break from the loop
            if cv2.waitKey(1) & 0xff == ord("q"):
                break
            if count == 100:
                break
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')
    datatrainer.training()
    socketio.emit('socket_generate_face_finish',
             {'status': 'finish'}, room = sid)

def generate_recognition(sid):
    # grab global references to the output frame and lock variables
    global outputFrame, lock, socketio
    ids = []
    while True:
        # wait until the lock is acquired
        with lock:
            ids, imageFrame = datarecognitior.recognition(outputFrame.copy())
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if imageFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", imageFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue
            #wait for 'q' key was pressed and break from the loop
            if cv2.waitKey(1) & 0xff == ord("q"):
                break

            if len(np.unique(ids)) > 0:
                break

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')
    rows = find_persion(ids)
    print(rows)
    print(len(rows))
    print(len(ids))
    if len(rows) < len(ids):
        rows.append(("Khách", ""))
    print(len(rows))
    print(rows)
    jsondata = [{"first_name": x[0], "last_name": x[1]} for x in rows]
    socketio.emit('recognition_finish',
        {'data': jsondata, 'status': 'finish'}, room = sid)

def find_persion(ids):

    con = sqlite3.connect("sensor.db")
    cur = con.cursor()
    sql="select first_name, last_name from people where id in ({seq})".format(
    seq=','.join(['?']*len(ids)))

    cur.execute(sql, ids.tolist() )
    rows = cur.fetchall()
    con.close()
    return rows

# check to see if this is the main thread of execution
if __name__ == '__main__':

    try:
        # construct the argument parser and parse command line arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--ip", type=str, required=True,
            help="ip address of the device")
        ap.add_argument("-o", "--port", type=int, required=True,
            help="ephemeral port number of the server (1024 to 65535)")
        ap.add_argument("-f", "--frame-count", type=int, default=32,
            help="# of frames used to construct the background model")
        args = vars(ap.parse_args())
        # start a thread that will perform motion detection
        t = threading.Thread(target=detect_motion, args=(
            args["frame_count"],))
        t.daemon = True
        t.start()

        # start the flask app
        socketio.run(app, host=args["ip"], port=args["port"], debug=True,
            use_reloader=False)
    except KeyboardInterrupt:
        destroy()
        # release the video stream pointer
        vs.stop()