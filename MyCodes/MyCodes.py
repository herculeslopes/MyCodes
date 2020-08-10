import tkinter as tk
from PIL import ImageTk, Image
from time import sleep
from tkinter import filedialog
import sqlite3

class MainProgram():
    def __init__(self, master):
        self.root = master
        self.root.title('MyCodes')
        self.root.geometry('950x500')
        self.root.resizable(False, False)
        self.root.configure(background='#121212')

        self.ChooseProfile()


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

                ProfileButton = tk.Button(ProfileFrame, image=ProfileImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=lambda a = Button_id: Login(a))
                ProfileButton.image = ProfileImage
                ProfileButton.pack(side=tk.LEFT, padx=10)
        
        elif ProfileCounter < 3:

            AddImage = ImageTk.PhotoImage(Image.open('Icons/add.png'))
            AddButton = tk.Button(ProfileFrame, image=AddImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=self.AddProfile_Username)
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


    def AddProfile_Username(self):
        pass

def Main():
    root = tk.Tk()
    MainProgram(root)
    root.mainloop()


if __name__ == '__main__':
    Main()
