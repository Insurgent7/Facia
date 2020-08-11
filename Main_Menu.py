from tkinter import *
from threading import Timer
from datetime import datetime

from Register import register
from Update import update
from Recognize_entry import live_attendance_entry
from Absent_Mail import low_attendance_mail
from Recognize_exit import live_attendance_exit
from View_Attendance import view_attendance_main
from Edit_Attendance import edit_attendance_main
from Recognize_Class import live_attendance_class
from Emotion_Report import emotion_report

# initialize the systems and the cameras for monitoring attendance
prog_start_time = datetime.today()
entry_attendance_time = prog_start_time.replace(day=prog_start_time.day + 1, hour=8, minute=00, second=0, microsecond=0)
time_left_entry = entry_attendance_time - prog_start_time
thread = time_left_entry.seconds + 1
t = Timer(thread, live_attendance_entry)
t.start()

# sends out email to everyone absent
daily_mail_time = prog_start_time.replace(day=prog_start_time.day + 1, hour=14, minute=00, second=0, microsecond=0)
time_left_for_mail = daily_mail_time - prog_start_time
thread1 = time_left_for_mail.seconds + 1
t1 = Timer(thread1, low_attendance_mail)
t1.start()

# starts monitoring exit time
exit_attendance_time = prog_start_time.replace(day=prog_start_time.day + 1, hour=12, minute=00, second=0, microsecond=0)
time_left_exit = exit_attendance_time - prog_start_time
thread2 = time_left_exit.seconds + 1
t2 = Timer(thread2, live_attendance_exit)
t2.start()

# starts taking class attendance
class_attendance = prog_start_time.replace(day=prog_start_time.day + 1, hour=9, minute=59, second=0, microsecond=0)
c_a = class_attendance - prog_start_time
thread3 = c_a.seconds + 1
t3 = Timer(thread3, live_attendance_class)
t3.start()

#schedule.every().day.at('08:00').do(live_attendance_entry)
#schedule.every().day.at('14:00').do(low_attendance_mail)
#schedule.every().day.at('12:00').do(live_attendance_exit)


def menu():
    root = Tk()
    root.geometry('500x600')
    root.title("Facia Main Menu")
    Label(root, text="Welcome To Facia", font=('', 35), pady=10).pack()
    Button(root, text="Register New Face", bd=3, font=('', 15), padx=5, pady=5, command=register).pack()
    Button(root, text="Update Face Data", bd=3, font=('', 15), padx=5, pady=5, command=update).pack()
    # Button(root, text="Live Attendance", bd=3, font=('', 15), padx=5, pady=5, command=live_attendance).pack()
    Button(root, text="View Attendance", bd=3, font=('', 15), padx=5, pady=5, command=view_attendance_main).pack()
    Button(root, text="Edit Attendance", bd=3, font=('', 15), padx=5, pady=5, command=edit_attendance_main).pack()
    Button(root, text="Emotion Report", bd=3, font=('', 15), padx=5, pady=5, command=emotion_report).pack()
    Label(root, text=" ", bd=3, font=('', 15), padx=5, pady=5).pack()
    Button(root, text="Entry Attendance", fg="Green", bd=3, font=('', 20), padx=10, pady=5, command=live_attendance_entry).pack()
    Button(root, text="Exit Attendance", fg="Red", bd=3, font=('', 20), padx=10, pady=5, command=live_attendance_exit).pack()
    Button(root, text="Class Attendance", fg="Blue", bd=3, font=('', 20), padx=10, pady=5, command=live_attendance_class).pack()
    root.mainloop()
