import sqlite3
import cv2
import numpy
import os
from datetime import datetime

'''
def put_attendance_entry(name):
    with sqlite3.connect('Facia_Info.db') as db:
        cr = db.cursor()
    s1 = 'SELECT ID FROM Student_Employee_Details WHERE Name = ?'
    cr.execute(s1, [name])
    Result = cr.fetchall()
    if not Result:
        print('Oops!', 'This ID not Found')
    else:
        result = Result[0]
        localID = result[0]
        now = datetime.now()
        entry_time = now.strftime("%H:%M:%S")
        print('Attendance given for ID : ' + localID + ' Name : ' + name)
        attendance_insert = 'INSERT OR IGNORE INTO Main_Attendance(ID, Name, Entry_Time) VALUES(?, ?, ?)'
        cr.execute(attendance_insert, [localID, name, entry_time])
        db.commit()
        print('Attendance given for ID : ' + localID + ' Name : ' + name)
'''


def put_attendance_exit(name):
    with sqlite3.connect('Facia_Info.db') as db:
        cr = db.cursor()
    s1 = 'SELECT ID FROM Student_Employee_Details WHERE Name = ?'
    cr.execute(s1, [name])
    Result = cr.fetchall()
    if not Result:
        print('Oops!', 'ID not Found')
    else:
        result = Result[0]
        localID = result[0]
        # now = datetime.now()
        exit_time = datetime.now().strftime("%H:%M:%S")
        datetoday = datetime.now().strftime("%d-%m-%Y").replace("-", "_")
        attendance_insert = ('''UPDATE or REPLACE Main_Attendance_{} SET Exit_Time =? WHERE ID =?'''.format(datetoday))
        cr.execute(attendance_insert, [exit_time, localID])
        db.commit()
        print('Exit Attendance Recorded for ID : ' + localID + ' Name : ' + name)


def live_attendance_exit():
    print(datetime.now())
    width, height = 1440, 1080
    # URL = 'http://192.168.31.27:47474/video'
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    haar_file = 'data/haarcascades/haarcascade_frontalface_default.xml'
    datasets = 'datasets'
    # Part 1: Create fisherRecognizer
    print('Recognizing Face Please Be in sufficient Lights...')
    # Create a list of images and a list of corresponding names
    (images, lables, names, id) = ([], [], {}, 0)
    for (subdirs, dirs, files) in os.walk(datasets):
        for subdir in dirs:
            names[id] = subdir
            subjectpath = os.path.join(datasets, subdir)
            for filename in os.listdir(subjectpath):
                path = subjectpath + '/' + filename
                lable = id
                images.append(cv2.imread(path, 0))
                lables.append(int(lable))
            id += 1
    (width, height) = (130, 100)
    (images, lables) = [numpy.array(lis) for lis in [images, lables]]
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(images, lables)
    # Part 2: Use fisherRecognizer on camera stream
    face_cascade = cv2.CascadeClassifier(haar_file)
    cam = cv2.VideoCapture(0)  # change the camera id each camera
    # URL = 'https://192.168.43.131:47477/video'
    # cam = cv2.VideoCapture(URL)
    if not cam.isOpened():
        print('External Camera Cannot be Opened')
    while True:
        (_, frame) = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            # Try to recognize the face
            prediction = model.predict(face_resize)
            name = names[prediction[0]]
            put_attendance_exit(name)

            if prediction[1] < 500:
                if name == 'UNKNOWN':
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(frame, 'UNKNOWN', (x + 10, y + 250), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    # cv2.putText(frame, '% s - %.0f' % (names[prediction[0]], prediction[1]), (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                    cv2.putText(frame, '% s ' % (names[prediction[0]]), (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(frame, 'Not Recognised', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

        cv2.imshow('Exit Recognition', frame)

        if cv2.waitKey(27) & 0xFF == 27:
            break
    cam.release()
    cv2.destroyAllWindows()
    print('\nFacia Live Exit Attendance Ended \nTHANK YOU for using Facia')
