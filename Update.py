"""
Search, update and delete  student/employee data and images.
"""
from tkinter import *
from tkinter import messagebox as ms
import sqlite3
import cv2
import os
from Register import show

face_detector = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')


class Main:
    def __init__(self, master):
        self.choose = StringVar()
        self.master = master
        self.SearchID = StringVar()
        self.OldName = StringVar()
        self.Name = StringVar()
        self.Department = StringVar()
        self.Email = StringVar()
        self.widgets()

    def search_data(self):
        with sqlite3.connect('Facia_Info.db') as db:
            cr = db.cursor()
        face = 'SELECT * FROM Student_Employee_Details WHERE ID = ?'
        cr.execute(face, [self.SearchID.get()])
        result = cr.fetchall()
        if not result:
            ms.showerror('Oops!', 'This ID not Found')
        else:
            print(result[0])
            Result = result[0]
            ms.showinfo('Found', 'ID :  %s\n\nName :  %s\nDepartment :  %s\nEmail ID :  %s' % (Result[0], Result[1], Result[2], Result[3]))
        db.close()

    def update_face(self):
        with sqlite3.connect('Facia_Info.db') as db:
            c = db.cursor()
        face = 'SELECT ID FROM Student_Employee_Details WHERE ID = ?'
        c.execute(face, [self.SearchID.get()])
        result = c.fetchall()
        if not result:
            ms.showerror('Oops!', 'This ID not Found')
        else:
            student_insert = 'UPDATE Student_Employee_Details SET (Name, Department, Email) = ( ?, ?, ?) WHERE ID = ?;'
            c.execute(student_insert, [self.Name.get(), self.Department.get(), self.Email.get(), self.SearchID.get()])
            db.commit()
            ms.showinfo('Success!', 'Face Data Updated!')
        db.close()

    def delete_face(self):
        with sqlite3.connect('Facia_Info.db') as db:
            cr = db.cursor()
        face = 'DELETE FROM Student_Employee_Details WHERE ID = ?'
        cr.execute(face, [self.SearchID.get()])
        db.commit()
        ms.showinfo('Success !', 'Data of ID ' + self.SearchID.get() + ' deleted')

    def widgets(self):
        self.head = Label(self.master, text='Update Face Data', font=('', 32), pady=10).pack()
        self.logf = Frame(self.master, padx=20, pady=20)

        Label(self.logf, text='Enter ID: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.SearchID, bd=5, font=('', 15)).grid(row=0, column=1)
        Button(self.logf, text=' Search ', bd=3, font=('', 15), padx=5, pady=5, command=self.search_data).grid(row=1, column=1)
        Button(self.logf, text=' Delete Face', bd=3, font=('', 15), padx=5, pady=5, command=self.delete_face).grid(row=1, column=2)

        Label(self.logf, text='Modify Face Name: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.Name, bd=5, font=('', 15)).grid(row=2, column=1)

        Label(self.logf, text='Modify Department: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.Department, bd=5, font=('', 15)).grid(row=3, column=1)

        Label(self.logf, text='Modify Email ID: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.Email, bd=5, font=('', 15)).grid(row=4, column=1)

        Button(self.logf, text=' Update Face ', bd=3, font=('', 15), padx=5, pady=5, command=self.update_face).grid(row=5, column=1)

        options = ['WebCam', 'External 1', 'External 2']
        self.choose.set(options[0])
        Label(self.logf, text=' Select Image Acquisition Camera ', font=('', 12), pady=5, padx=5).grid(row=6, column=0, sticky=W)
        dropdown_menu = OptionMenu(self.logf, self.choose, *options).grid(row=6, column=1)

        frame = Frame(self.logf, bg='white').grid(row=7, column=0, sticky=W)

        # lmain = Label(frame).grid()
        Button(self.logf, text=' Show Camera Feed ', bd=3, font=('', 15), padx=5, pady=5, command=show).grid(row=7, column=1)
        '''
        root = Tk()
        lmain = Label(root)
        lmain.pack()
        def show_frame():
            import PIL
            from PIL import Image, ImageTk
            cam = cv2.VideoCapture(0)
            _, frame = cam.read()
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = PIL.Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)

        show_frame()
        '''
        Button(self.logf, text=' Capture ', bd=3, font=('', 15), padx=5, pady=5, command=self.get_face).grid(row=8, column=1)
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
        # os.rename(rt,face_name)
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


def update():
    root = Tk()
    root.title("Update Face Data")
    Main(root)
    root.mainloop()
