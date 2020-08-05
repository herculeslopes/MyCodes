from PIL import ImageTk, Image
import tkinter as tk
from tkinter.font import Font
import sys
import sqlite3

data = sys.argv[1:]

# print(args)

MainWindow = tk.Tk()
MainWindow.title('MyCodes')
MainWindow.state('zoomed')
# MainWindow.resizable(False, False)
MainWindow.configure(background='#121212')

def ConnectToDB():
    global MyCodesDB, DB_Cursor

    MyCodesDB = sqlite3.connect('MyCodesDB.db')
    DB_Cursor = MyCodesDB.cursor()

    DB_Cursor.execute(f'''CREATE TABLE IF NOT EXISTS CodeList_{data[3]} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT DEAFULT "Give It A Title",
    txt TEXT,
    language TEXT
    )''')


def CloseConnectionToDB():

    MyCodesDB.commit()
    DB_Cursor.close()
    MyCodesDB.close()


def ClearList():

    for widget in ListBar.winfo_children():

        widget.destroy()


def ClearCentralSpace():

    for widget in CentralSpace.winfo_children():

        widget.destroy()


def SaveCard():

    ConnectToDB()

    Title = EntryTitle.get()
    Text = TextBox.get('1.0', tk.END)
    print(f'Title: {Title}\nText: {Text}')

    DB_Cursor.execute(f'''INSERT INTO CodeList_{data[3]} (title, txt) VALUES (?, ?)''', (Title, Text))

    CloseConnectionToDB()

    ClearCentralSpace()

    CodeList()


def OpenCode(iden):

    # global TextBox

    ConnectToDB()

    DB_Cursor.execute(f'''SELECT title, txt FROM CodeList_{data[3]} WHERE id = {iden}''')
    CodeInfo = DB_Cursor.fetchone()

    ClearCentralSpace()

    LabelFont = Font(size=30)
    TitleLabel = tk.Label(CentralSpace, text=CodeInfo[0], font=LabelFont, fg='#999999', bg='#121212')
    TitleLabel.pack(padx=50, pady=25, anchor='w')
    # TitleLabel.grid(row=0, column=0, padx=50, pady=25, sticky='w')

    TextFrame = tk.Frame(CentralSpace, bg='#333333', bd=0)
    TextFrame.pack(padx=(50, 320), pady=(0, 145), anchor='w', fill=tk.BOTH, expand=True)
    # TextFrame.grid(row=1, column=0, padx=50, sticky='w')

    TextFont = Font(family='Square721 BT', size=18)
    TxtBox = tk.Message(TextFrame, text=CodeInfo[1], font=TextFont, bg='#333333', fg='#999999', width=9999, bd=0, padx=10, pady=10)
    TxtBox.pack(side=tk.TOP, anchor='w')
    # TxtBox.pack(fill=tk.BOTH, expand=True)

    # SaveButton = tk.Button(CentralSpace, text='Save Card', font='Default 15', bg='#333333', activebackground='#333333', fg='#999999', activeforeground='#999999', bd=0, command=lambda: SaveCard(iden))
    # SaveButton.grid(row=2, column=0, padx=50, pady=25, sticky='w')


def CodeList():

    ClearList()

    ConnectToDB()

    DB_Cursor.execute(f'''SELECT COUNT(*) FROM CodeList_{data[3]}''')
    CodeCounter = DB_Cursor.fetchone()[0]

    if CodeCounter != 0:

        for code in range(1, CodeCounter + 1):  

            DB_Cursor.execute(f'''SELECT title FROM CodeList_{data[3]} WHERE id = {code}''')
            title = DB_Cursor.fetchone()[0]

            button = tk.Button(ListBar, text=title, anchor='w', bg='#616161', fg='#121212', activebackground='#999999', bd=0, command=lambda iden = code: OpenCode(iden)) #808080
            button.pack(padx=5, pady=1, fill=tk.BOTH)


def AddCard():

    global EntryTitle, TextBox

    ClearCentralSpace()

    EntryFont = Font(family='Square721 BT', size=30)
    EntryTitle = tk.Entry(CentralSpace, font=EntryFont, bg='#333333', fg='#999999', bd=0)
    EntryTitle.pack(padx=50, pady=25, anchor='w')
    # EntryTitle.grid(row=0, column=0, padx=50, pady=25, sticky='w')

    TextFont = Font(family='Square721 BT', size=18)
    TextBox = tk.Text(CentralSpace, font=TextFont, bg='#333333', fg='#999999', bd=0, padx=10, pady=10)
    TextBox.pack(padx=50, anchor='w')
    # TextBox.grid(row=1, column=0, padx=50)

    SaveButton = tk.Button(CentralSpace, text='Save Card', font='Default 15', bg='#333333', activebackground='#333333', fg='#999999', activeforeground='#999999', bd=0, command=SaveCard)
    SaveButton.pack(padx=50, pady=25, anchor='w')
    # SaveButton.grid(row=2, column=0, padx=50, pady=25, sticky='w')


def TopBarPacking():

    MenuText = Font(family='Arial')

    NewCard = tk.Button(TopBar, text='New Card', font=MenuText, bg='#303030', fg='#ffffff', bd=0, command=AddCard)
    NewCard.pack(padx=2, pady=2, side=tk.LEFT)


def ChooseProfile():

    MainWindow.destroy()

    import MyCodes

def MainView(argv1=1):

    global ListBar, CentralSpace, TopBar

    SideBar = tk.Frame(MainWindow, width=250, bg='#242424', bd=0) #212121
    SideBar.pack(side=tk.LEFT, fill=tk.Y)

    TopBar = tk.Frame(MainWindow, height=30, bg='#242424', bd=0) #303030 262626
    TopBar.pack(side=tk.TOP, fill=tk.X)

    TopBarPacking()

    CentralSpace = tk.Frame(MainWindow, bg='#121212', bd=0)
    CentralSpace.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    ProfileBar = tk.Frame(SideBar, height=70, width=250, bg='#303030', bd=0)
    ProfileBar.pack(side=tk.TOP, fill=tk.X)
    ProfileBar.pack_propagate(0)

    ProfileFrame = tk.Frame(ProfileBar, bg='#303030')
    ProfileFrame.pack(side=tk.LEFT, padx=10)

    IconFile = Image.open(data[2])
    IconImage = ImageTk.PhotoImage(IconFile.resize((60, 60), Image.ANTIALIAS))
    ProfileButton = tk.Button(ProfileFrame, image=IconImage, bg='#303030', activebackground='#303030', bd=0, command=ChooseProfile)
    ProfileButton.image = IconImage
    ProfileButton.pack(side=tk.LEFT)

    UsernameLabel = tk.Label(ProfileFrame, text=data[0], font='OpenSans 25', bg='#303030', fg='#969696')
    UsernameLabel.pack(side=tk.RIGHT, padx=(10, 0))

    ListBar = tk.Frame(SideBar, bg='#242424', bd=0)
    ListBar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    CodeList()


MainView()

MainWindow.mainloop()

# if __name__ == "__main__":
    # main(sys.argv[0])