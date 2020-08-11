import tkinter as tk
from PIL import ImageTk, Image
from time import sleep
from tkinter import filedialog
from tkinter.font import Font
import sqlite3

class MainProgram():
    def __init__(self, master):
        self.root = master
        self.root.title('MyCodes')
        self.root.geometry('950x500')
        self.root.resizable(False, False)
        self.root.configure(background='#121212')

        self.LabelFont = Font(family='Arial', size=30)

        self.ChooseProfile()

    
    def CreateImage(self, path):
        ImageFile = Image.open(path)
        TkImage = ImageTk.PhotoImage(ImageFile)

        return TkImage


    def ChooseProfile(self):
        self.CleanMainWindow()

        ProfileFrame = tk.Frame(self.root, bg='#121212', bd=0)
        ProfileFrame.pack(expand=True)

        self.ConnectToDB()

        self.DB_Cursor.execute('''SELECT COUNT(*) FROM Profile''')
        ProfileCounter = self.DB_Cursor.fetchone()[0]

        if ProfileCounter != 0:

            for Profile in range(1, ProfileCounter + 1):

                self.DB_Cursor.execute(f'''SELECT id, imagepath FROM Profile WHERE id ={Profile}''')
                
                data = self.DB_Cursor.fetchone()
                Button_id = data[0]
                ProfileImagePath = data[1]

                ImageFile = Image.open(ProfileImagePath)

                if ProfileImagePath == 'Icons/default.png':

                    ProfileImage = ImageTk.PhotoImage(ImageFile)

                else:

                    ProfileImage = ImageTk.PhotoImage(ImageFile.resize((250, 250), Image.ANTIALIAS))

                ProfileButton = tk.Button(ProfileFrame, image=ProfileImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=lambda a = Button_id: self.Login(a))
                ProfileButton.image = ProfileImage
                ProfileButton.pack(side=tk.LEFT, padx=10)
        
        elif ProfileCounter < 3:

            AddImage = ImageTk.PhotoImage(Image.open('Icons/add.png'))
            AddButton = tk.Button(ProfileFrame, image=AddImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=self.CreateProfile)
            AddButton.image = AddImage
            AddButton.pack(side=tk.RIGHT, padx=5)    


    def CleanMainWindow(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    def ConnectToDB(self):
        self.MyCodesDB = sqlite3.connect('MyCodesDB.db')
        self.DB_Cursor = self.MyCodesDB.cursor()

        self.DB_Cursor.execute('''CREATE TABLE IF NOT EXISTS Profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        imagepath TEXT DEFAULT "Icons/default.png")''')


    def CloseConnectionToDB(self):
        self.MyCodesDB.commit()
        self.DB_Cursor.close()
        self.MyCodesDB.close()


    def CreateProfile(self):
        def AddUsername():
            self.CleanMainWindow()

            

        pass


    def Login(self, Button_id):
        self.CleanMainWindow()

        self.DB_Cursor.execute(f'''SELECT imagepath, username FROM Profile WHERE id = {Button_id}''')
        Data = self.DB_Cursor.fetchone()

        UpFrame = tk.Frame(self.root, bg='#121212', bd=0)
        UpFrame.pack(side=tk.TOP, anchor='w', padx=10, pady=10)

        ImageFile = Image.open(Data[0])
        IconFile = ImageFile.resize((75, 75), Image.ANTIALIAS)
        IconImage = ImageTk.PhotoImage(IconFile)
        IconButton = tk.Button(UpFrame, image=IconImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=self.ChooseProfile)
        IconButton.image = IconImage
        IconButton.pack(side=tk.LEFT)

        EditImage = self.CreateImage('Icons/edit.png')
        EditButton = tk.Button(UpFrame, image=EditImage, bg='#121212', activebackground='#121212', bd=0, command=self.EditProfile)
        EditButton.image = EditImage
        EditButton.pack(side=tk.RIGHT, padx=5)

        Username = Data[1]
        UsernameLabel = tk.Label(self.root, text=Username, font=self.LabelFont, bg='#121212', fg='#999999')
        UsernameLabel.pack(pady=(30, 5))

        PasswordEntry = tk.Entry(self.root, font=self.LabelFont, bg='#333333', fg='#999999', bd=0, justify=tk.CENTER, show='•')
        PasswordEntry.pack(pady=5)

        def Submit(Button_id):
            from os import system

            self.DB_Cursor.execute(f'''SELECT username, password, imagepath FROM Profile WHERE id = {Button_id}''')
            Data = self.DB_Cursor.fetchone()

            Password = Data[1]

            PasswordGiven = PasswordEntry.get()

            if PasswordGiven == Password:
                self.root.destroy()

                system(f'''python MainWindow.py "{Data[0]}" "{Data[1]}" "{Data[2]}" {Button_id}''')

            else:
                PasswordEntry.delete(0, tk.END)


        SubmitImage = self.CreateImage('Icons/submit.png')
        SubmitButton = tk.Button(self.root, image=SubmitImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=lambda: Submit(Button_id))
        SubmitButton.image = SubmitImage
        SubmitButton.pack(pady=5)


        self.root.bind('<Return>', lambda event: Submit(Button_id))


    def EditProfile(self):
        pass


def Main():
    root = tk.Tk()
    MainProgram(root)
    root.mainloop()


if __name__ == '__main__':
    Main()
