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

        self.EntryFont = Font(family='Square721 BT', size=30)
        self.TextFont = Font(family='Square721 BT', size=18)

        self.MainView()


    def InitialWindow(self):
        from os import system

        self.root.destroy()

        system(f'''python MyCodes.py''')

    
    def CleanCentralSpace(self):
        for widget in self.CentralSpace.winfo_children():
            widget.destroy()


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


    def SaveCard(self):
        self.ConnectToDB()

        Title = self.TitleEntry.get()
        Text = self.TextBox.get('1.0', tk.END)

        self.DB_Cursor.execute(f'''INSERT INTO CodeList_{Data[3]} (title, txt) VALUES (?, ?)''', (Title, Text))

        self.CloseConnectionToDB()
        
        self.CleanCentralSpace()

        self.PackCodeList()


    def MainView(self):

        SideBar = tk.Frame(self.root, width=250, bg='#242424', bd=0)
        SideBar.pack(side=tk.LEFT, fill=tk.Y)


        TopBar = tk.Frame(self.root, height=30, bg='#242424', bd=0)
        TopBar.pack(side=tk.TOP, fill=tk.X)

        def PackTopBar():
            def AddCard():
                self.CleanCentralSpace()
                EntryFont = Font(family='Square721 BT', size=30)

                self.TitleEntry = tk.Entry(self.CentralSpace, font=EntryFont, bg='#333333', fg='#999999', bd=0)
                self.TitleEntry.pack(padx=50, pady=25, anchor='w')
        
                self.TextBox = tk.Text(self.CentralSpace, font=self.TextFont, bg='#333333', fg='#999999', bd=0, padx=10, pady=10)
                self.TextBox.pack(padx=50, anchor='w')

                SaveButton = tk.Button(self.CentralSpace, text='Save Card', font='Default 15', bg='#333333', activebackground='#333333', fg='#999999', activeforeground='#999999', bd=0, command=self.SaveCard)
                SaveButton.pack(padx=50, pady=25, anchor='w')


            NewCard = tk.Button(TopBar, text='New', bg='#303030', activebackground='#999999', fg='#ffffff', bd=0, command=AddCard)
            NewCard.pack(padx=2, pady=2, side=tk.LEFT)

        PackTopBar()

        self.CentralSpace = tk.Frame(self.root, bg='#121212', bd=0)
        self.CentralSpace.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

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

        def OpenCode(iden):
            self.CleanCentralSpace()

            self.ConnectToDB()
            self.DB_Cursor.execute(f'''SELECT title, txt FROM CodeList_{Data[3]} WHERE id = {iden}''')
            CodeInfo = self.DB_Cursor.fetchone()

            TitleFont = Font(size=30)
            TitleLabel = tk.Label(self.CentralSpace, text=CodeInfo[0], font=TitleFont, fg='#999999', bg='#121212')
            TitleLabel.pack(padx=50, pady=25, anchor='w')
            
            TextFrame = tk.Frame(self.CentralSpace, bg='#333333', bd=0)
            TextFrame.pack(padx=(50, 320), pady=(0, 145), anchor='w', fill=tk.BOTH, expand=True)

            TextFont = Font(family='Square721 BT', size=18)
            
            TxtBox = tk.Message(TextFrame, text=CodeInfo[1], font=TextFont, bg='#333333', fg='#999999', width=9999, bd=0, padx=10, pady=10)
            TxtBox.pack(side=tk.TOP, anchor='w')


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
