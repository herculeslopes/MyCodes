import tkinter as tk
from PIL import ImageTk, Image
from time import sleep
from tkinter import filedialog
import sqlite3

ProfileWindow = tk.Tk()
ProfileWindow.title('MyCodes')
ProfileWindow.geometry('950x500')
ProfileWindow.resizable(False, False)
ProfileWindow.configure(background='#121212')

def ConnectToDB():
    global MyCodesDB, DB_Cursor

    MyCodesDB = sqlite3.connect('MyCodesDB.db')
    DB_Cursor = MyCodesDB.cursor()

    DB_Cursor.execute('''CREATE TABLE IF NOT EXISTS Profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    imagepath TEXT DEFAULT "Icons/default.png")''')   


def CloseConnectionToDB():

    MyCodesDB.commit()
    DB_Cursor.close()
    MyCodesDB.close()


def CleanScreen():

    for widget in ProfileWindow.winfo_children():

        widget.destroy()


def Confirm():

    ChooseProfile()


def NewProfileStatus(path):

    CleanScreen()

    Welcome = tk.Label(ProfileWindow, text='WELCOME', font='OpenSans 30', bg='#121212', fg='#808080')
    Welcome.pack(pady=20)

    StatusWidgetFrame = tk.Frame(ProfileWindow, bg='#121212', bd=0)
    StatusWidgetFrame.pack(pady=20)

    ProfileLabel = tk.Label(StatusWidgetFrame, image=ToChangeImage, bg='#121212', bd=0, relief=tk.FLAT)
    ProfileLabel.pack(side=tk.LEFT, padx=30)

    LabelFrame = tk.Label(StatusWidgetFrame, bg='#121212', bd=0)
    LabelFrame.pack(side=tk.RIGHT)

    UsernameLabel = tk.Label(LabelFrame, text=UsernameGiven, font='OpenSans 30', bg='#121212', fg='#808080')
    UsernameLabel.grid(sticky='w')

    PasswordLabel = tk.Label(LabelFrame, text='•' * len(PasswordGiven), font='OpenSans 30', bg='#121212', fg='#808080')
    PasswordLabel.grid(sticky='w')

    ChoiceFrame = tk.Frame(ProfileWindow, bg='#121212', bd=0)
    ChoiceFrame.pack(side=tk.BOTTOM, pady=(0, 40))

    SaveImage = ImageTk.PhotoImage(Image.open('Icons/save.png'))
    SaveButton = tk.Button(ChoiceFrame, image=SaveImage, bg='#121212', activebackground='#121212', bd=0, command=Confirm)
    SaveButton.image = SaveImage
    SaveButton.pack(side=tk.RIGHT, padx=10)

    '''DiscartImage = ImageTk.PhotoImage(Image.open('Icons/discart.png'))
    DiscartButton = tk.Button(ChoiceFrame, image=DiscartImage, bg='#121212', activebackground='#121212',bd=0, command=DiscartProfile)
    DiscartButton.image = DiscartImage
    DiscartButton.pack(side=tk.LEFT, padx=10)'''


def SaveProfile():
    
    ConnectToDB()

    DB_Cursor.execute('''
    
    INSERT INTO Profile (username, password, imagepath) VALUES (?, ?, ?)
    
    ''', (UsernameGiven, PasswordGiven, FilePath))

    CloseConnectionToDB()

    '''ProfileWindow.update()

    for i in range(0, 10):
        print(i)
        sleep(1)'''

    NewProfileStatus(FilePath)


def SearchImage():
    global FilePath

    FilePath = filedialog.askopenfilename(initialdir='/', title='Select A File', filetypes=(("PNG", "*.png"), ("JPEG", "*.jpg"), ("All Files", "*.*")))
    print(FilePath)

    if FilePath != '':

        ChangeImage(FilePath)


def ChangeImage(path='Icons/template.png'):
    global ProfileImage, ToChangeImage

    CleanScreen()

    TitleLabel = tk.Label(ProfileWindow, text='Choose Your Own Image', font='OpenSans 30', bg='#121212', fg='#808080')
    TitleLabel.pack(pady=20)

    FunctionFrame = tk.Frame(ProfileWindow, bg='#121212', bd=0)
    FunctionFrame.pack(pady=20)

    ProfileImage = ImageTk.PhotoImage(ImageFile)
    DefaultImage = tk.Label(FunctionFrame, image=ProfileImage, bg='#121212', bd=0, relief=tk.FLAT)
    DefaultImage.image = ProfileImage
    DefaultImage.pack(side=tk.LEFT, padx=30)

    LineImage = ImageTk.PhotoImage(Image.open('Icons/line.png'))
    RoundLine = tk.Label(FunctionFrame, image=LineImage, bg='#121212')
    RoundLine.image = LineImage
    RoundLine.pack(side=tk.LEFT)

    ToChangeImage = ImageTk.PhotoImage(Image.open(path).resize((250, 250), Image.ANTIALIAS))
    ChangeImageButton = tk.Button(FunctionFrame, image=ToChangeImage, bg='#121212', activebackground='#121212', bd=0, command=SearchImage)
    ChangeImageButton.image = ToChangeImage
    ChangeImageButton.pack(side=tk.RIGHT, padx=30)

    SaveButton = tk.Button(ProfileWindow, text='Save Profile',font='OpenSans 20', bg='#333333', activebackground='#333333', fg='#999999', bd=0, command=SaveProfile)
    SaveButton.pack(side=tk.BOTTOM, pady=(0, 50))


def SignUp(event=None):
    global PasswordGiven, FilePath

    FilePath = 'Icons/default.png'

    PasswordGiven1 = PasswordSignUp1.get()
    PasswordGiven2 = PasswordSignUp2.get()

    if PasswordGiven1 == '' and PasswordGiven2 == '':

        PasswordSignUp1.delete(0, tk.END)
        PasswordSignUp2.delete(0, tk.END)

    elif PasswordGiven1 != PasswordGiven2:

        PasswordSignUp1.delete(0, tk.END)
        PasswordSignUp2.delete(0, tk.END)

    elif PasswordGiven1 == PasswordGiven2:

        PasswordGiven = PasswordGiven1

        # NewProfileStatus()
        ChangeImage()


def AddProfile_Password(event=None):
    global PasswordSignUp1, PasswordSignUp2

    CleanScreen()

    IconFile = ImageFile.resize((75, 80), Image.ANTIALIAS)
    IconImage = ImageTk.PhotoImage(IconFile)
    IconButton = tk.Button(ProfileWindow, image=IconImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=ChooseProfile)
    IconButton.image = IconImage
    IconButton.pack(side=tk.TOP, anchor='w', padx=10, pady=10)

    PasswordLabel = tk.Label(ProfileWindow, text='Password: ', font='OpenSans 30', bg='#121212', fg='#808080')
    PasswordLabel.pack(pady=(20, 5))

    PasswordSignUp1 = tk.Entry(ProfileWindow, font='OpenSans 20', bg='#333333', fg='#999999', bd=0, justify=tk.CENTER, show='•')
    PasswordSignUp1.pack(ipady=7, ipadx=70, pady=5)

    PasswordSignUp2 = tk.Entry(ProfileWindow, font='OpenSans 20', bg='#333333', fg='#999999', bd=0, justify=tk.CENTER, show='•')
    PasswordSignUp2.pack(ipady=7, ipadx=70, pady=5)

    SubmitImage = ImageTk.PhotoImage(Image.open('Icons/submit.png'))
    SubmitButton = tk.Button(ProfileWindow, image=SubmitImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=SignUp)
    SubmitButton.image = SubmitImage
    SubmitButton.pack(pady=5)

    ProfileWindow.bind('<Return>', SignUp)


def CheckUsername(event=None):

    global UsernameGiven

    UsernameGiven = UsernameSignUp.get()

    if UsernameGiven != '':

        AddProfile_Password()


def AddProfile_Username():
    global UsernameSignUp, ImageFile

    CleanScreen()

    ImageFile = Image.open('Icons/default.png')
    IconFile = ImageFile.resize((75, 80), Image.ANTIALIAS)
    IconImage = ImageTk.PhotoImage(IconFile)
    IconButton = tk.Button(ProfileWindow, image=IconImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=ChooseProfile)
    IconButton.image = IconImage
    IconButton.pack(side=tk.TOP, anchor='w', padx=10, pady=10)

    UsernameLabel = tk.Label(ProfileWindow, text='Username: ', font='OpenSans 30', bg='#121212', fg='#808080')
    UsernameLabel.pack(pady=(30, 5))

    UsernameSignUp = tk.Entry(ProfileWindow, font='OpenSans 20', bg='#333333', fg='#999999', bd=0, justify=tk.CENTER)
    UsernameSignUp.pack(ipady=7, ipadx=70, pady=5)

    SubmitImage = ImageTk.PhotoImage(Image.open('Icons/submit.png'))
    SubmitButton = tk.Button(ProfileWindow, image=SubmitImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=CheckUsername)
    SubmitButton.image = SubmitImage
    SubmitButton.pack(pady=5)

    ProfileWindow.bind('<Return>', CheckUsername)


def EditProfile():

    CleanScreen()

    TopFrame = tk.Frame(ProfileWindow, bg='#121212')
    TopFrame.pack(side=tk.LEFT, anchor='w', padx=10, pady=10)

    IconButton = tk.Button(TopFrame, image=IconImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=ChooseProfile)
    IconButton.pack(side=tk.LEFT)
    # IconButton.pack(side=tk.TOP, anchor='nw', padx=10, pady=10)

    Atributes = tk.Frame(ProfileWindow, bg='#121212', bd=0)
    Atributes.pack(side=tk.RIGHT, fill=tk.Y)

    UserLabel = tk.Label(Atributes, text='New Username', font='Arial 20', bg='#121212', fg='#999999')
    UserLabel.pack(side=tk.TOP, anchor='w', padx=10, pady=5)

    NewUsername = tk.Entry(Atributes, font='Default 20', bg='#333333', fg='#999999', bd=0)
    NewUsername.pack(side=tk.TOP, ipady=5, ipadx=70, padx=10, pady=5)

    PasswordLabel = tk.Label(Atributes, text='New Password', font='Arial 20', bg='#121212', fg='#999999')
    PasswordLabel.pack(side=tk.TOP, anchor='w', padx=10, pady=(20, 5))

    NewPassword = tk.Entry(Atributes, font='Default 20', bg='#333333', fg='#999999', bd=0)
    NewPassword.pack(side=tk.TOP, ipady=5, ipadx=70, padx=10, pady=5)

    ConfNewPassword = tk.Entry(Atributes, font='Default 20', bg='#333333', fg='#999999', bd=0)
    ConfNewPassword.pack(side=tk.TOP, ipady=5, ipadx=70, padx=10, pady=5)

    CurrentLabel = tk.Label(Atributes, text='Current Password', font='Arail 20', bg='#121212', fg='#999999')
    CurrentLabel.pack(side=tk.TOP, anchor='w', padx=10, pady=(20, 5))

    Password = tk.Entry(Atributes, font='Default 20', bg='#333333', fg='#999999', bd=0)
    Password.pack(side=tk.TOP, ipady=5, ipadx=70, padx=10, pady=(5, 0))

    Options = tk.Frame(Atributes)
    Options.pack(side=tk.BOTTOM, padx=10, expand=True)

    TrashFile = Image.open('Icons/trash.png')
    TrashImage = ImageTk.PhotoImage(TrashFile)
    TrashButton = tk.Button(Options, image=TrashImage, bg='#121212', activebackground='#121212', bd=0)
    TrashButton.image = TrashImage
    TrashButton.pack()

    '''UsernameLabel = tk.Label(TopFrame, text=Username, font='Arial 40', bg='#121212')
    UsernameLabel.pack(side=tk.LEFT, anchor='e')
    # UsernameLabel.pack(side=tk.TOP, anchor='ne')'''


def Submit(Button_id):

    from os import system

    DB_Cursor.execute(f'''SELECT username, password, imagepath FROM Profile WHERE id = {Button_id}''')
    data = DB_Cursor.fetchone()
    password = data[1]

    PasswordGiven = PasswordEntry.get()

    if PasswordGiven == password:

        ProfileWindow.destroy()

        # system(f'python MainWindow.py {Button_id}')
        system(f'''python MainWindow.py "{data[0]}" "{data[1]}" "{data[2]}" {Button_id}''')

    else:

        PasswordEntry.delete(0, tk.END)


def Login(Button_id):
    global PasswordEntry, IconImage, Username

    CleanScreen()

    DB_Cursor.execute(f'''SELECT imagepath, username FROM Profile WHERE id = {Button_id}''')
    data = DB_Cursor.fetchone()

    MiniMenu = tk.Frame(ProfileWindow, bg='#121212', bd=0)
    MiniMenu.pack(side=tk.TOP, anchor='w', padx=10, pady=10)

    ImageFile = Image.open(data[0])
    IconFile = ImageFile.resize((75, 75), Image.ANTIALIAS)
    IconImage = ImageTk.PhotoImage(IconFile)
    IconButton = tk.Button(MiniMenu, image=IconImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=ChooseProfile)
    IconButton.image = IconImage
    IconButton.pack(side=tk.LEFT)
    # IconButton.pack(side=tk.TOP, anchor='w', padx=10, pady=10)

    EditFile = Image.open('Icons/edit.png')
    EditImage = ImageTk.PhotoImage(EditFile)
    EditButton = tk.Button(MiniMenu, image=EditImage, bg='#121212', activebackground='#121212', bd=0, command=EditProfile)
    EditButton.image = EditImage 
    EditButton.pack(side=tk.RIGHT, padx=5)
    # EditButton.pack(side=tk.TOP, anchor='nw', pady=10)

    # GetAccount()

    Username = data[1]
    UsernameLabel = tk.Label(ProfileWindow, text=Username, font='OpenSans 30', bg='#121212', fg='#999999')
    UsernameLabel.pack(pady=(30, 5))

    PasswordEntry = tk.Entry(ProfileWindow, font='OpenSans 30', bg='#333333', fg='#999999', bd=0, justify=tk.CENTER, show='•')
    PasswordEntry.pack(pady=5)

    SubmitImage = ImageTk.PhotoImage(Image.open('Icons/submit.png'))
    SubmitButton = tk.Button(ProfileWindow, image=SubmitImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=lambda: Submit(Button_id))
    SubmitButton.image = SubmitImage
    SubmitButton.pack(pady=5)

    ProfileWindow.bind('<Return>', lambda event: Submit(Button_id))


def ChooseProfile():
    # global ProfileImage

    CleanScreen()

    ProfileFrame = tk.Frame(ProfileWindow, bg='#121212', bd=0)
    ProfileFrame.pack(expand=True)

    ConnectToDB()

    DB_Cursor.execute('''SELECT COUNT(*) FROM Profile''')
    ProfileCounter = DB_Cursor.fetchone()[0]

    # ImageFile = Image.open('MainProgram/MyCodes006/Icons/default.png')
    # ProfileImage = ImageTk.PhotoImage(ImageFile)

    if ProfileCounter != 0:

        for Profile in range(1, ProfileCounter + 1):

            DB_Cursor.execute(f'''SELECT id, imagepath FROM Profile
            WHERE id = {Profile}''')

            data = DB_Cursor.fetchone()
            Button_id = data[0]
            FilePath1 = data[1]

            ImageFile = Image.open(FilePath1)

            if FilePath1 == 'Icons/default.png':

                ProfileImage = ImageTk.PhotoImage(ImageFile)

            else:

                ProfileImage = ImageTk.PhotoImage(ImageFile.resize((250, 250), Image.ANTIALIAS))

            ProfileButton = tk.Button(ProfileFrame, image=ProfileImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=lambda a = Button_id: Login(a))
            ProfileButton.image = ProfileImage
            ProfileButton.pack(side=tk.LEFT, padx=10)
    
    else:

        ImageFile = Image.open('Icons/default.png')
        ProfileImage = ImageTk.PhotoImage(ImageFile)

    # ProfileButton = tk.Button(ProfileFrame, image=ProfileImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=Login)
    # ProfileButton.image = ProfileImage
    # ProfileButton.pack(side=tk.LEFT, padx=5)

    if ProfileCounter < 3:

        AddImage = ImageTk.PhotoImage(Image.open('Icons/add.png'))
        AddButton = tk.Button(ProfileFrame, image=AddImage, bg='#121212', activebackground='#121212', bd=0, relief=tk.FLAT, command=AddProfile_Username)
        AddButton.image = AddImage
        AddButton.pack(side=tk.RIGHT, padx=5)


ChooseProfile()

ProfileWindow.mainloop()
