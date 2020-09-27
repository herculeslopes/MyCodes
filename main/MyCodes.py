import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter.font import Font
import sqlite3

class InitialWindow():
    def __init__(self, master):
        self.root = master
        self.root.title('MyCodes')
        self.root.geometry('950x500')
        self.root.resizable(False, False)
        self.root.configure(background='#121212')

        self.LabelFont = Font(size=30)
        self.EntryFont = Font(size=20)
        self.WarningFont = Font(size=40)

        self.ChooseProfile()

    
    def CreateImage(self, path):
        ImageFile = Image.open(path)
        TkImage = ImageTk.PhotoImage(ImageFile)

        return TkImage


    def ChooseProfile(self):
        self.ClearMainWindow()

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

                if ProfileImagePath == 'Images/Icons/default.png':

                    ProfileImage = ImageTk.PhotoImage(ImageFile)

                else:

                    ProfileImage = ImageTk.PhotoImage(ImageFile.resize((250, 250), Image.ANTIALIAS))

                ProfileButton = tk.Button(ProfileFrame, image=ProfileImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=lambda a = Button_id: self.Login(a))
                ProfileButton.image = ProfileImage
                ProfileButton.pack(side=tk.LEFT, padx=10)
        
        if ProfileCounter < 3:

            AddImage = ImageTk.PhotoImage(Image.open('Images/Buttons/add.png'))
            AddButton = tk.Button(ProfileFrame, image=AddImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=self.CreateProfile)
            AddButton.image = AddImage
            AddButton.pack(side=tk.RIGHT, padx=5)    


    def ClearMainWindow(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    def ConnectToDB(self):
        self.MyCodesDB = sqlite3.connect('MyCodesDB.db')
        self.DB_Cursor = self.MyCodesDB.cursor()

        self.DB_Cursor.execute('''
        CREATE TABLE IF NOT EXISTS Profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            imagepath TEXT DEFAULT "Images/Buttons/default.png"
        )
        ''')


    def CloseConnectionToDB(self):
        self.MyCodesDB.commit()
        self.DB_Cursor.close()
        self.MyCodesDB.close()


    def CreateProfile(self):
        self.ClearMainWindow()


        def SaveProfile():
            self.ConnectToDB()

            self.DB_Cursor.execute('''
            INSERT INTO Profile (username, password, imagepath) VALUES (?, ?, ?)
            ''', (Username, Password, FilePath))

            self.CloseConnectionToDB()

            self.ChooseProfile()


        def ProfileStatus():
            self.ClearMainWindow()

            WelcomeLabel = tk.Label(self.root, text='WELCOME', font=self.LabelFont, bg='#121212', fg='#808080')
            WelcomeLabel.pack(pady=20)

            StatusFrame = tk.Frame(self.root, bg='#121212', bd=0)
            StatusFrame.pack(pady=20)

            ProfileLabel = tk.Label(StatusFrame, image=ToChangeImage, bg='#121212', bd=0, relief=tk.FLAT)
            ProfileLabel.pack(side=tk.LEFT, padx=30)

            LabelFrame = tk.Frame(StatusFrame, bg='#121212', bd=0)
            LabelFrame.pack(side=tk.RIGHT)

            UsernameLabel = tk.Label(LabelFrame, text=Username, font=self.LabelFont, bg='#121212', fg='#808080')
            UsernameLabel.grid(sticky='w')

            PasswordLabel = tk.Label(LabelFrame, text='•' * len(Password), font='OpenSans 30', bg='#121212', fg='#808080')
            PasswordLabel.grid(sticky='w')

            Options = tk.Frame(self.root, bg='#121212', bd=0)
            Options.pack(side=tk.BOTTOM, pady=(0, 40))

            SaveImage = self.CreateImage('Images/Buttons/save.png')
            SaveButton = tk.Button(Options, image=SaveImage, bg='#121212', activebackground='#121212', bd=0, command=SaveProfile)
            SaveButton.image = SaveImage
            SaveButton.pack(side=tk.RIGHT, padx=10)

            DiscartImage = self.CreateImage('Images/Buttons/discart.png')
            DiscartButton = tk.Button(Options, image=DiscartImage, bg='#121212', activebackground='#121212',bd=0, command=self.ChooseProfile)
            DiscartButton.image = DiscartImage
            DiscartButton.pack(side=tk.LEFT, padx=10)


        def AddImage(path='Images/Icons/template.png'):
            global ToChangeImage

            def SearchImage():
                global FilePath

                FilePath = filedialog.askopenfilename(initialdir='/', title='Select A File', filetypes=(("PNG", "*.png"), ("JPEG", "*.jpg"), ("All Files", "*.*")))
                
                if FilePath != '':
                    AddImage(FilePath)


            self.ClearMainWindow()

            TitleLabel = tk.Label(self.root, text='Choose You Own Image', font=self.LabelFont, bg='#121212', fg='#808080')
            TitleLabel.pack(pady=20)

            MainFrame = tk.Frame(self.root, bg='#121212', bd=0)
            MainFrame.pack(pady=20)

            DefaultImage = self.CreateImage('Images/Icons/default.png')
            DefaultLabel = tk.Label(MainFrame, image=DefaultImage, bg='#121212', bd=0)
            DefaultLabel.image = DefaultImage
            DefaultLabel.pack(side=tk.LEFT, padx=30)

            LineImage = self.CreateImage('Images/Icons/line.png')
            LineLabel = tk.Label(MainFrame, image=LineImage, bg='#121212')
            LineLabel.image = LineImage
            LineLabel.pack(side=tk.LEFT)

            ToChangeImage = ImageTk.PhotoImage(Image.open(path).resize((250, 250), Image.ANTIALIAS))
            ChangeImageButton = tk.Button(MainFrame, image=ToChangeImage, bg='#121212', activebackground='#121212', bd=0, command=SearchImage)
            ChangeImageButton.image = ToChangeImage
            ChangeImageButton.pack(side=tk.RIGHT, padx=30)

            SubmitImage = self.CreateImage('Images/Buttons/submit.png')
            SubmitButton = tk.Button(self.root, image=SubmitImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=ProfileStatus)
            SubmitButton.image = SubmitImage
            SubmitButton.pack(side=tk.BOTTOM, pady=(0, 50))

        def AddPassword():
            self.ClearMainWindow()

            def CheckPassword(event=None):
                global Password

                PasswordGiven1 = PasswordSignUp1.get()
                PasswordGiven2 = PasswordSignUp2.get()

                if PasswordGiven1 == '' and PasswordGiven2 == '':

                    PasswordSignUp1.delete(0, tk.END)
                    PasswordSignUp2.delete(0, tk.END)

                elif PasswordGiven1 != PasswordGiven2:

                    PasswordSignUp1.delete(0, tk.END)
                    PasswordSignUp2.delete(0, tk.END)

                elif PasswordGiven1 == PasswordGiven2:

                    Password = PasswordGiven1

                    AddImage()


            ImageFile = Image.open('Images/Icons/default.png')
            IconFile = ImageFile.resize((75, 80), Image.ANTIALIAS)
            IconImage = ImageTk.PhotoImage(IconFile)
            IconButton = tk.Button(self.root, image=IconImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=self.ChooseProfile)
            IconButton.image = IconImage
            IconButton.pack(side=tk.TOP, anchor='w', padx=10, pady=10)

            PasswordLabel = tk.Label(self.root, text='Password: ', font='OpenSans 30', bg='#121212', fg='#808080')
            PasswordLabel.pack(pady=(20, 5))

            PasswordSignUp1 = tk.Entry(self.root, font='OpenSans 20', bg='#333333', fg='#999999', bd=0, justify=tk.CENTER, show='•')
            PasswordSignUp1.pack(ipady=7, ipadx=70, pady=5) 

            PasswordSignUp2 = tk.Entry(self.root, font='OpenSans 20', bg='#333333', fg='#999999', bd=0, justify=tk.CENTER, show='•')
            PasswordSignUp2.pack(ipady=7, ipadx=70, pady=5) 

            SubmitImage = self.CreateImage('Images/Buttons/submit.png')
            SubmitButton = tk.Button(self.root, image=SubmitImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=CheckPassword)
            SubmitButton.image = SubmitImage
            SubmitButton.pack(pady=5)

            self.root.bind('<Return>', CheckPassword)


        def AddUsername():
            def CheckUsername(event=None):
                global Username

                Username = UsernameSignUp.get()

                if Username != '':
                    AddPassword()

            self.ClearMainWindow()

            ImageFile = Image.open('Images/Icons/default.png')
            IconFile = ImageFile.resize((75, 80), Image.ANTIALIAS)
            IconImage = ImageTk.PhotoImage(IconFile)
            IconButton = tk.Button(self.root, image=IconImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=self.ChooseProfile)
            IconButton.image = IconImage
            IconButton.pack(side=tk.TOP, anchor='w', padx=10, pady=10)

            UsernameLabel = tk.Label(self.root, text='Username:', font=self.LabelFont, bg='#121212', fg='#808080')
            UsernameLabel.pack(pady=(30, 5))

            UsernameSignUp = tk.Entry(self.root, font=self.EntryFont, bg='#333333', fg='#999999', bd=0, justify=tk.CENTER)
            UsernameSignUp.pack(ipady=7, ipadx=70, pady=5)

            SubmitImage = self.CreateImage('Images/Buttons/submit.png')
            SubmitButton = tk.Button(self.root, image=SubmitImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=CheckUsername)
            SubmitButton.image = SubmitImage
            SubmitButton.pack(pady=5)

            self.root.bind('<Return>', CheckUsername)

        AddUsername()


    def Login(self, Button_id):
        self.ClearMainWindow()

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

        EditImage = self.CreateImage('Images/Buttons/edit.png')
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

        SubmitImage = self.CreateImage('Images/Buttons/submit.png')
        SubmitButton = tk.Button(self.root, image=SubmitImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=lambda: Submit(Button_id))
        SubmitButton.image = SubmitImage
        SubmitButton.pack(pady=5)

        self.root.bind('<Return>', lambda event: Submit(Button_id))


    def EditProfile(self):
        self.ClearMainWindow()

        MainFrame = tk.Frame(self.root, bg='#121212')
        MainFrame.pack(expand=True)

        WarningLabel = tk.Label(MainFrame, text='Feature In Development', font=self.WarningFont, fg='#808080', bg='#121212')
        WarningLabel.pack()
        
        OkButton = tk.Button(MainFrame, text='ok', font=self.EntryFont, fg='#808080', bg='#333333', activebackground='#242424', bd=0)
        OkButton['command'] = self.ChooseProfile
        OkButton.pack()
        

def Main():
    root = tk.Tk()
    InitialWindow(root)
    root.mainloop()


if __name__ == '__main__':
    Main()