from datetime import datetime
from tkinter import *
from tkinter import messagebox as ms
import sqlite3


class Main:
    def __init__(self, master):
        self.master = master
        self.Edit_ID = StringVar()
        self.Edit_By_Date = StringVar()
        self.Manual_entry = datetime.now().strftime("%H:%M:%S" + '(Edited)')
        self.widgets()

# edit attendance of today
    def Manual_Attendance(self):
        datetoday = datetime.now().strftime("%d-%m-%Y").replace("-", "_")
        with sqlite3.connect('Facia_Info.db') as db:
            c = db.cursor()
        s1 = 'SELECT Name FROM Student_Employee_Details WHERE ID = ?'
        c.execute(s1, [self.Edit_ID.get()])
        Result = c.fetchall()
        if not Result:
            ms.showerror('Oops!', 'This ID not Found')
        else:
            result = Result[0]
            name = result[0]
            q1 = ('''INSERT OR IGNORE INTO Main_Attendance_{} (ID, Name, Entry_Time) VALUES(?, ?, ?) '''.format(datetoday))
            c.execute(q1, [self.Edit_ID.get(), name, self.Manual_entry])
            db.commit()
            ms.showinfo('Success!', 'Attendance Manually Given for\n ID : '+self.Edit_ID.get() + '\n Name : ' + name)

# edit attendance by date
    def Manual_Old_Attendance(self):
        date = self.Edit_By_Date.get()
        DateOld = date.translate({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
        DateOldPrint = date.translate({ord(c): "-" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
        with sqlite3.connect('Facia_Info.db') as db:
            c = db.cursor()
        s1 = 'SELECT Name FROM Student_Employee_Details WHERE ID = ?'
        c.execute(s1, [self.Edit_ID.get()])
        Result = c.fetchall()
        if not Result:
            ms.showerror('Oops!', 'This ID not Found')
        else:
            result = Result[0]
            name = result[0]
            q1 = ('''INSERT OR IGNORE INTO Main_Attendance_{} (ID, Name, Entry_Time) VALUES(?, ?, ?) '''.format(DateOld))
            c.execute(q1, [self.Edit_ID.get(), name, self.Manual_entry])
            db.commit()
            ms.showinfo('Success!', 'Attendance Manually Given for Date : ' + DateOldPrint + '\n ID : ' + self.Edit_ID.get() + '\n Name : ' + name)

    def widgets(self):
        self.crf = Frame(self.master, padx=10, pady=10)
        Label(self.crf, text=" ", bd=3, font=('', 15), padx=5, pady=5).grid(row=0, column=0)
        Label(self.crf, text='Enter ID:', font=('', 20), pady=5, padx=5).grid(row=1, column=0, sticky=W)
        Entry(self.crf, textvariable=self.Edit_ID, bd=5, font=('', 15)).grid(row=1, column=1)
        Button(self.crf, text="Mark Today's Attendance", bd=3, font=('', 15), padx=5, pady=5, command=self.Manual_Attendance).grid(row=2, column=1)

        Label(self.crf, text='Enter Date:', font=('', 20), pady=5, padx=5).grid(row=3, column=0, sticky=W)
        Entry(self.crf, textvariable=self.Edit_By_Date, bd=5, font=('', 15)).grid(row=3, column=1)
        Button(self.crf, text='Mark Attendance', bd=3, font=('', 15), padx=5, pady=5, command=self.Manual_Old_Attendance).grid(row=4, column=1)
        self.crf.pack()


def edit_attendance_main():
    root = Tk()
    root.title("Manual Attendance")
    Main(root)
    root.mainloop()
