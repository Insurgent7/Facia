from tkinter import *
from tkinter import messagebox as ms
import sqlite3
from datetime import datetime
from Main_Menu import menu


class Main:
    def __init__(self, master):
        self.master = master
        self.ID = StringVar()
        self.Password = StringVar()
        # self.Email = StringVar()
        self.widgets()

    def login(self):
        with sqlite3.connect('Facia_Info.db') as db:
            c = db.cursor()
        find_admin = 'SELECT ID, Password FROM Admin_Details WHERE ID = ? and Password = ?'
        c.execute(find_admin, [(self.ID.get()), (self.Password.get())])
        result = c.fetchall()
        if result:
            Result = result[0]
            ID = Result[0]
            print('Admin ' + ID + ' has Logged In;' + ' Time : ' + datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
            db.close()
            menu()
            # self.logf.destroy()
        else:
            ms.showerror('Oops!', 'ID or Password is Incorrect !')
            db.close()

    @staticmethod
    def forget():
        ms.showinfo('Temporary', 'Contact Administrator to Get New Password(for Now)')

    def widgets(self):
        Label(self.master, text='Facia', font=('', 32), pady=10).pack()
        self.logf = Frame(self.master, padx=20, pady=20)

        Label(self.logf, text='Admin ID: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.ID, bd=5, font=('', 15)).grid(row=0, column=1)

        Label(self.logf, text='Password: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.Password, bd=5, font=('', 15), show='*').grid(row=1, column=1)

        Button(self.logf, text=' Login ', bd=3, font=('', 15), padx=5, pady=5, command=self.login).grid(row=2, column=1)

        Button(self.logf, text='Forget Password?', fg="Red", bd=3, font=('', 12), padx=5, pady=5, command=self.forget).grid(row=2, column=2)
        self.logf.pack()


# create window and application object
root = Tk()
root.title("Facia Login")
Main(root)
root.mainloop()