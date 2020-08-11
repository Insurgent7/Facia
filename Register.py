from tkinter import *
from tkinter import messagebox as ms
import sqlite3
import cv2
import os

face_detector = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')
with sqlite3.connect('Facia_Info.db') as db:
    c = db.cursor()
c.execute(
    '''CREATE TABLE IF NOT EXISTS Student_Employee_Details (ID TEXT NOT NULL UNIQUE, Name TEXT NOT NULL, Department TEXT, Email TEXT, PRIMARY KEY(ID));''')
db.commit()
db.close()


def show():
    cap = cv2.VideoCapture(0)
    cap.set(3, 300)
    cap.set(4, 200)
    '''_, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    self.imgtk = imgtk
    self.configure(image=imgtk)
    self.after(1, self.show) '''
    while True:
        ret, frame = cap.read()
        ret = (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if ret:
            live = cv2.imshow('Live Feed', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break


class Main:
    def __init__(self, master):
        self.choose = StringVar()
        self.master = master
        self.ID = StringVar()
        self.Name = StringVar()
        self.Department = StringVar()
        self.Email = StringVar()
        self.widgets()

# registers a new students and employees to the system.

    def insert_face(self):
        with sqlite3.connect('Facia_Info.db') as db:
            cr = db.cursor()
        face = 'SELECT ID FROM Student_Employee_Details WHERE ID = ?'
        cr.execute(face, [(self.ID.get())])
        result = cr.fetchall()
        if result:
            ms.showerror('Oops!', 'This ID already exists.')
        else:
            student_insert = 'INSERT INTO Student_Employee_Details(ID, Name, Department, Email) VALUES(?, ?, ?, ?)'
            cr.execute(student_insert, [self.ID.get(), self.Name.get(), self.Department.get(), self.Email.get()])
            db.commit()
            ms.showinfo('Success!', 'Face Data Registered!')
        db.close()

    def widgets(self):
        self.head = Label(self.master, text='New Registration', font=('', 32), pady=10)
        self.head.pack()
        self.logf = Frame(self.master, padx=20, pady=20)

        Label(self.logf, text='Set ID: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.ID, bd=5, font=('', 15)).grid(row=0, column=1)

        Label(self.logf, text='Set Name: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.Name, bd=5, font=('', 15)).grid(row=1, column=1)

        Label(self.logf, text='Set Department: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.Department, bd=5, font=('', 15)).grid(row=2, column=1)

        Label(self.logf, text='Set Email ID: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.Email, bd=5, font=('', 15)).grid(row=3, column=1)

        Button(self.logf, text=' Save ', bd=3, font=('', 15), padx=5, pady=5, command=self.insert_face).grid(row=4, column=1)

        options = ['WebCam', 'External 1', 'External 2']
        self.choose.set(options[0])
        Label(self.logf, text=' Select Image Acquisition Camera ', font=('', 12), pady=5, padx=5).grid(row=5, column=0, sticky=W)
        dropdown_menu = OptionMenu(self.logf, self.choose, *options).grid(row=5, column=1)

        frame = Frame(self.logf, bg='white').grid(row=6, column=0, sticky=W)
        # lmain = Label(frame).grid()
        Button(self.logf, text=' Show Camera Feed ', bd=3, font=('', 15), padx=5, pady=5, command=show).grid(row=6, column=1)

        Button(self.logf, text=' Capture ', bd=3, font=('', 15), padx=5, pady=5, command=self.get_face).grid(row=7, column=1)

        self.logf.pack()

    @staticmethod
    def face_extractor(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        if faces is ():
            return None
        for (x, y, w, h) in faces:
            return img[y:y + h, x:x + w]

    def get_face(self):
        face_id = self.ID.get()
        face_name = self.Name.get()
        # URL = 'https://192.168.43.131:47477/video'
        cam = cv2.VideoCapture(0)
        # cam = cv2.VideoCapture(URL)
        if not cam.isOpened():
            ms.showerror('Oops!', 'External Camera Cannot be Opened.')
        cam.set(3, 640)  # set video width
        cam.set(4, 480)  # set video height

        print("\n [INFO] Initializing face capture. Look the camera and wait ...")
        count = 0
        newpath = 'datasets'
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        path = os.path.join(newpath, face_name)
        if not os.path.isdir(path):
            os.mkdir(path)
        while True:
            ret, img = cam.read()
            if self.face_extractor(img) is not None:
                count += 1
                face = cv2.resize(self.face_extractor(img), (300, 300))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                cv2.imwrite('% s/% s.jpg' % (path, face_id + '.' + str(count)), face)
                cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Capture - Face detection', face)
            else:
                print('Face Not Found')
                pass
            if cv2.waitKey(1) & 0xFF == 27 or count == 100:
                break
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()
        ms.showinfo('Success!', 'Photo Capturing Completed')


def register():
    root = Tk()
    root.title("New Face Registration")
    Main(root)
    root.mainloop()
