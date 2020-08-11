import sqlite3
import cv2
import numpy
import os
from datetime import datetime
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import time

subjects = ['IT501', 'IT502', 'IT503', 'IT504', 'HU501']
date_today = 'Dt_' + datetime.now().strftime('%d-%m-%y').replace("-", "_")

with sqlite3.connect('Facia_IT_Class.db') as db:
    c = db.cursor()
for subject in subjects:
    c.execute('''CREATE TABLE IF NOT EXISTS {} (ID TEXT NOT NULL, Name TEXT NOT NULL, PRIMARY KEY(ID));'''.format(subject))
    db.commit()
    try:
        c.execute('''ALTER TABLE {} ADD COLUMN {} TEXT'''.format(subject, date_today))
        db.commit()
    except:
        pass

# a demo class schedule. Replace it with actual schedule. It records attendance subjectwise.
def all_class(name, emo):
    if '10:10:00' <= datetime.now().strftime("%H:%M:%S") < '10:30:00':
        class_attendance(name, emo, 'IT501')
    if '11:10:00' <= datetime.now().strftime("%H:%M:%S") < '11:30:00':
        class_attendance(name, emo, 'IT502')
    if '12:10:00' <= datetime.now().strftime("%H:%M:%S") < '12:30:00':
        class_attendance(name, emo, 'IT503')
    if '14:10:00' <= datetime.now().strftime("%H:%M:%S") < '14:30:00':
        class_attendance(name, emo, 'IT504')
    if '15:10:00' <= datetime.now().strftime("%H:%M:%S") < '15:30:00':
        class_attendance(name, emo, 'HU501')


def class_attendance(name, emo, sub):
    dateonly = datetime.now().strftime('%d-%m-%y')
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
        with sqlite3.connect('Facia_IT_Class.db') as db1:
            cr1 = db1.cursor()
        attendance_insert = ('''INSERT OR IGNORE INTO {} (ID, Name, {}) VALUES(?, ?, ?) '''.format(sub, date_today))
        cr1.execute(attendance_insert, [localID, name, '1'])
        db1.commit()
        print('Attendance given for ID : ' + localID + ' Name : ' + name + ' Subject : ' + sub)
        with sqlite3.connect('Facia_IT_Emotion.db') as db2:
            cr2 = db2.cursor()
        cr2.execute(
            '''CREATE TABLE IF NOT EXISTS {}_{}_{} (Date TEXT, Angry TEXT, Disgust TEXT, Scared TEXT, Happy TEXT, Sad TEXT, Surprised TEXT, Neutral TEXT);'''.format(
                name, localID, sub))
        db2.commit()
        try:
            time.sleep(30)
            query = '''INSERT INTO {}_{}_{} (Date, Angry, Disgust, Scared, Happy, Sad, Surprised, Neutral) VALUES(?, ?, ?, ?, ?, ?, ?, ?)'''.format(name, localID, sub)
            cr2.execute(query, [dateonly, emo[0], emo[1], emo[2], emo[3], emo[4], emo[5], emo[6]])
            db2.commit()
        except:
            print('Error in Emotion Data Insertion !')


def live_attendance_class():
    print(datetime.now())
    datasets = 'datasets'
    haar_file = 'data/haarcascades/haarcascade_frontalface_default.xml'
    emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'
    emotion_classifier = load_model(emotion_model_path, compile=False)
    EMOTIONS = ["Angry", "Disgust", "Scared", "Happy", "Sad", "Surprised", "Neutral"]
    print('Recognizing Face Please Be in sufficient Lights...')
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
    face_cascade = cv2.CascadeClassifier(haar_file)
    # URL = 'https://192.168.43.131:47477/video'
    cam = cv2.VideoCapture(0)  # URL
    if not cam.isOpened():
        print('External Camera Cannot be Opened')
    while True:
        (_, frame) = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        faces1 = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        emo = []
        if len(faces1) > 0:
            faces1 = sorted(faces1, reverse=True, key=lambda xx: (xx[2] - xx[0]) * (xx[3] - xx[1]))[0]
            (fX, fY, fW, fH) = faces1
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            preds = emotion_classifier.predict(roi)[0]
            for prob in preds:
                emo.append(prob * 100)
        else:
            pass

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            prediction = model.predict(face_resize)
            name = names[prediction[0]]

            all_class(name, emo)

            if prediction[1] < 500:
                if name == 'UNKNOWN':
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(frame, 'UNKNOWN', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    # cv2.putText(frame, '% s - %.0f' % (names[prediction[0]], prediction[1]), (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                    cv2.putText(frame, '% s ' % name, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(frame, 'Not Recognised', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        cv2.imshow('Class Recognition', frame)
        if cv2.waitKey(27) & 0xFF == 27:
            break
    cam.release()
    cv2.destroyAllWindows()
    print('\nFacia Class Attendance Ended.')

