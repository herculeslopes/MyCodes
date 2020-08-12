import tkinter as tk
from tkinter.font import Font
from PIL import ImageTk, Image
import sys
import sqlite3

Data = sys.argv[1:]

class MainProgram():
    def __init__(self, master):
        self.root = master
        self.root.title('MyCodes')
        self.root.state('zoomed')
        self.root.configure(background='#121212')

        self.MainView()


    def InitialWindow(self):
        from os import system

        self.root.destroy()

        system(f'''python MyCodes.py''')


    def CreateImage(self, path):
        ImageFile = Image.open(path)
        TkImage = ImageTk.PhotoImage(ImageFile)

        return TkImage


    def ConnectToDB(self):
        self.MyCodesDB = sqlite3.connect('MyCodesDB.db')
        self.DB_Cursor = self.MyCodesDB.cursor()

        self.DB_Cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS CodeList_{Data[3]} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT DEAFULT "Give It A Title",
            txt TEXT,
            language TEXT
        )
        ''')


    def CloseConnectionToDB(self):
        self.MyCodesDB.commit()
        self.DB_Cursor.close()
        self.MyCodesDB.close()


    def AddCard(self):
        pass


    def MainView(self):

        SideBar = tk.Frame(self.root, width=250, bg='#242424', bd=0)
        SideBar.pack(side=tk.LEFT, fill=tk.Y)


        TopBar = tk.Frame(self.root, height=30, bg='#242424', bd=0)
        TopBar.pack(side=tk.TOP, fill=tk.X)

        def PackTopBar():
            NewCard = tk.Button(TopBar, text='New', bg='#303030', activebackground='#999999', fg='#ffffff', bd=0, command=self.AddCard)
            NewCard.pack(padx=2, pady=2, side=tk.LEFT)

        PackTopBar()

        CentralSpace = tk.Frame(self.root, bg='#121212', bd=0)
        CentralSpace.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ProfileBar = tk.Frame(SideBar, height=70, width=250, bg='#303030', bd=0)
        ProfileBar.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        ProfileBar.pack_propagate(0)

        ProfileFrame = tk.Frame(ProfileBar, bg='#303030')
        ProfileFrame.pack(side=tk.LEFT, padx=10)

        IconFile = Image.open(Data[2])
        IconImage = ImageTk.PhotoImage(IconFile.resize((60, 60), Image.ANTIALIAS))
        ProfileButton = tk.Button(ProfileFrame, image=IconImage, bg='#303030', activebackground='#303030', bd=0, command=self.InitialWindow)
        ProfileButton.image = IconImage
        ProfileButton.pack(side=tk.LEFT)

        ProfileFont = Font(size=25)

        UsernameLabel = tk.Label(ProfileFrame, text=Data[0], font=ProfileFont, bg='#303030', fg='#969696')
        UsernameLabel.pack(side=tk.RIGHT, padx=(10, 0))

        self.ListBar = tk.Frame(SideBar, bg='#242424', bd=0)
        self.ListBar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.PackCodeList()



    def PackCodeList(self):
        def ClearList():
            for widget in self.ListBar.winfo_children():
                widget.destroy()

        ClearList()

        def OpenCode():
            pass

        self.ConnectToDB()

        self.DB_Cursor.execute(f'''SELECT COUNT(*) FROM CodeList_{Data[3]}''')
        CodeCounter = self.DB_Cursor.fetchone()[0]

        if CodeCounter != 0:
            for code in range(1, CodeCounter + 1):
                self.DB_Cursor.execute(f'''SELECT title FROM CodeList_{Data[3]} WHERE id = {code}''')
                Title = self.DB_Cursor.fetchone()[0]
                
                Code = tk.Button(self.ListBar, text=Title, anchor='w', bg='#616161',  fg='#121212', activebackground='#999999', bd=0, command=lambda iden = code: OpenCode(iden))
                Code.pack(padx=5, pady=1, fill=tk.BOTH)


def Main():
    root = tk.Tk()
    MainProgram(root)
    root.mainloop()

Main()
