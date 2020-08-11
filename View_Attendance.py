"""
view attendance by ID, date, subject.
"""
from datetime import datetime
from tkinter import *
from tkinter import messagebox as ms
import sqlite3


class Main:
    def __init__(self, master):
        self.master = master
        self.Search_ID = StringVar()
        self.Search_By_Date = StringVar()
        self.Search_By_Subject = StringVar()
        self.Date_Today = datetime.now().strftime("%d-%m-%Y").replace("-", "_")
        self.widgets()

    def View_Today_Attendance(self):
        datetoday = datetime.now().strftime("%d-%m-%Y").replace("-", "_")
        with sqlite3.connect('Facia_Info.db') as db:
            cr = db.cursor()
        srch = '''SELECT * FROM Main_Attendance_{} WHERE ID = ?'''.format(datetoday)
        cr.execute(srch, [self.Search_ID.get()])
        result = cr.fetchall()
        if not result:
            ms.showwarning('Oops!', 'ID ' + self.Search_ID.get() + ' is absent today')
        else:
            print(result[0])
            Result = result[0]
            ms.showinfo('Found', 'ID :  %s\n\nName :  %s\nEntry_Time :  %s\nExit_Time :  %s' % (Result[0], Result[1], Result[2], Result[3]))

    def View_Old_Attendance(self):
        date = self.Search_By_Date.get()
        DateOld = date.translate({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
        DateOldPrint = date.translate({ord(c): "-" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
        with sqlite3.connect('Facia_Info.db') as db:
            c = db.cursor()
        s1 = '''SELECT * FROM Main_Attendance_{} WHERE ID = ?'''.format(DateOld)
        c.execute(s1, [self.Search_ID.get()])
        result = c.fetchall()
        if not result:
            ms.showwarning('Oops!', 'ID ' + self.Search_ID.get() + ' was absent on ' + DateOldPrint)
        else:
            print(result[0])
            Result = result[0]
            ms.showinfo('Found', 'For Date ' + DateOldPrint + '\nID :  %s\n\nName :  %s\nEntry_Time :  %s\nExit_Time :  %s' % (Result[0], Result[1], Result[2], Result[3]))

    def View_Attendance_Subject(self):
        subjects = ['IT501', 'IT502', 'IT503', 'IT504', 'HU501']
        subject = self.Search_By_Subject.get()
        with sqlite3.connect('Facia_IT_Class.db') as db:
            c = db.cursor()
        for sub in subjects:
            if sub in subject:
                # print(sub)
                q1 = '''SELECT * FROM {} WHERE ID = ?'''.format(sub)
                c.execute(q1, [self.Search_ID.get()])
                result = c.fetchall()
                if not result:
                    ms.showwarning('Oops!', 'ID not found')
                else:
                    print(result[0])
                    Result = result[0]
                    #ms.showinfo('Found', '\nID :  %s\n\nName :  %s\nEntry_Time :  %s\nExit_Time :  %s' % (Result[0], Result[1], Result[2], Result[3]))
                    ms.showinfo(sub, Result)
            else:
                pass
                # print(subject + ' Not Found !')


    def widgets(self):
        self.crf = Frame(self.master, padx=10, pady=10)
        Label(self.crf, text=" ", bd=3, font=('', 15), padx=5, pady=5).grid(row=0, column=0)
        Label(self.crf, text='Enter ID:', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.crf, textvariable=self.Search_ID, bd=5, font=('', 15)).grid(row=1, column=1)
        Button(self.crf, text="Search Today's Attendance", bd=3, font=('', 15), padx=5, pady=5, command=self.View_Today_Attendance).grid(row=2, column=1)

        Label(self.crf, text='Enter Date:', font=('', 20), pady=5, padx=5).grid(row=3, column=0, sticky=W)
        Entry(self.crf, textvariable=self.Search_By_Date, bd=5, font=('', 15)).grid(row=3, column=1)
        Button(self.crf, text='Search Attendance by Date', bd=3, font=('', 15), padx=5, pady=5, command=self.View_Old_Attendance).grid(row=4, column=1)

        Label(self.crf, text='Enter Subject:', font=('', 20), pady=5, padx=5).grid(row=5, column=0, sticky=W)
        Entry(self.crf, textvariable=self.Search_By_Subject, bd=5, font=('', 15)).grid(row=5, column=1)
        Button(self.crf, text='Subjectwise Attendance', bd=3, font=('', 15), padx=5, pady=5, command=self.View_Attendance_Subject).grid(row=6, column=1)
        self.crf.pack()


def view_attendance_main():
    root = Tk()
    root.title("View Attendance")
    Main(root)
    root.mainloop()
