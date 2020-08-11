import smtplib
import sqlite3
import ssl
from datetime import datetime
from threading import Timer

x = datetime.today()
y = x.replace(day=x.day + 1, hour=19, minute=33, second=0, microsecond=0)
delta_t = y - x
secs = delta_t.seconds + 1


def send(name, receiver):
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender_email = ' '  # <enter the official email here>
    password = ' '  # enter email password here
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)  # secure the connection
        server.login(sender_email, password)
        content = 'Dear ' + name + ',\n\tYou are absent today (' + datetime.now().strftime("%d-%m-%Y") + ') in College. Attend college to learn, prosper and achieve targeted Attendance.'
        signature = '\n\n' + '--' + '\n\t' + ' This is a auto generated e-mail by Facia Attendance System. If you think you received the mail by mistake and you are present in Campus, contact your School / College / Workplace Administrator immediately. Your attendance will be marked only then.'
        header = 'To:' + receiver + '\n' + 'From: ' + sender_email + '\n' + 'Subject:Facia Attendance System \n'
        content = header + content + signature
        server.sendmail(sender_email, receiver, content)
    except Exception as e:
        print(e)
    finally:
        server.quit()


def low_attendance_mail():
    print(datetime.now())  # sends a absence email to everyone absent that day at scheduled time everyday.
    datetoday = datetime.now().strftime("%d-%m-%Y").replace("-", "_")
    with sqlite3.connect('Facia_Info.db') as db:
        c = db.cursor()
    query = ('''SELECT Name, Email FROM Student_Employee_Details as ESD WHERE NOT EXISTS( select ID from  Main_Attendance_{} as MAD where MAD.ID = ESD.ID)'''.format(datetoday))
    c.execute(query)
    result = c.fetchall()
    if result:
        for row in result:
            name = row[0]
            receiver = row[1]
            print(name, receiver)
            send(name, receiver)
    db.close()
