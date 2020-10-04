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
        self.CodeFont = Font(family='Consolas', size=18)

        self.ActiveCard = None

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
            language TEXT
        )
        ''')


    def CloseConnectionToDB(self):
        self.MyCodesDB.commit()
        self.DB_Cursor.close()
        self.MyCodesDB.close()

    def DeleteTable(self):
        self.DB_Cursor.execute(f'''DROP TABLE CodeList_{Data[3]}''')
        self.CloseConnectionToDB()

    def ResetDB(self):

        self.ConnectToDB()

        Select = self.DB_Cursor.execute(f'''SELECT * FROM CodeList_{Data[3]}''')
        TableData = Select.fetchall()

        self.DeleteTable()
        self.ConnectToDB()

        for i in range(0, len(TableData)):
            self.DB_Cursor.execute(f'''INSERT INTO CodeList_{Data[3]} (title, txt) VALUES (?, ?)''', (TableData[i][1], TableData[i][2]))

        self.CloseConnectionToDB()


    def SaveCard(self):
        self.ConnectToDB()

        Title = self.TitleEntry.get()

        # self.DB_Cursor.execute(f'''INSERT INTO CodeList_{Data[3]} (title, txt) VALUES (?, ?)''', (Title, Text))

        # TODO: Save Title   
        self.DB_Cursor.execute(f'''INSERT INTO CodeList_{Data[3]} (title) VALUES (?)''', (Title,))

        self.DB_Cursor.execute(f'''SELECT COUNT(*) FROM CodeList_{Data[3]}''')
        
        CardIndex = self.DB_Cursor.fetchone()[0]

        # TODO: Save All Tabs
        for index, code in enumerate(self.TabCode):
            self.DB_Cursor.execute(f'''ALTER TABLE CodeList_{Data[3]} ADD code_{index + 1} TEXT''')
            self.DB_Cursor.execute(f'''UPDATE CodeList_{Data[3]} SET (code_{index + 1}) = (?) WHERE id = {CardIndex}''', (code,))

        self.CloseConnectionToDB()
        
        self.CleanCentralSpace()

        self.PackCodeList()

    
    def DeleteCard(self):
        pass

    '''def ResetId(self):
        self.ConnectToDB() 

        self.DB_Cursor.execute(f"""UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='CodeList_{Data[3]}'""")

        self.CloseConnectionToDB()'''


    def MainView(self):

        SideBar = tk.Frame(self.root, width=250, bg='#242424', bd=0)
        SideBar.pack(side=tk.LEFT, fill=tk.Y)


        TopBar = tk.Frame(self.root, height=30, bg='#242424', bd=0)
        TopBar.pack(side=tk.TOP, fill=tk.X)

        def PackTopBar():
            
            # TODO: Build a 'Programming Language' Tab Frame

            def AddCard():
                self.CleanCentralSpace()
                EntryFont = Font(family='Square721 BT', size=30)

                self.TitleEntry = tk.Entry(self.CentralSpace, font=EntryFont, bg='#333333', fg='#999999', bd=0)
                self.TitleEntry.pack(padx=50, pady=25, anchor='w')

                # TODO: Add Tabs To Text Box 

                TextBoxFrame = tk.Frame(self.CentralSpace, bg='lightblue', height=800, width=1500)
                TextBoxFrame.propagate(0)
                TextBoxFrame.pack(padx=50, anchor='w')

                TextTabFrame = tk.Frame(TextBoxFrame, bg='#121212') #525252
                TextTabFrame.pack(side=tk.TOP, fill=tk.X)

                TabList = []
                self.TabCode = []

                self.ActiveTab = 0
                
                def SwitchTab(iden):
                    print(f'iden = {iden}')
                    print(f'Antigo {self.ActiveTab}')

                    if self.ActiveTab != None:
                        TabList[self.ActiveTab].configure(background='#242424')
                        print(f'Mudando o antigo de cor: {self.ActiveTab}')

                    # TabList[iden].configure(background='#242424') # 333333
                    self.TabCode[self.ActiveTab] = self.TextBox.get('1.0', tk.END)
                    print(f'Previous Code: {self.TabCode[self.ActiveTab]}')

                    # self.DB_Cursor.execute(f'''INSERT INTO CodeList_{Data[3]} (code_{self.ActiveTab + 1}) VALUES (?)''', (self.TabCode[self.ActiveTab],))
                    
                    self.TextBox.delete('1.0', tk.END)

                    # Until This Point, The Code Is Working With The Previous Active Tab

                    self.ActiveTab = iden
                    print(f'Novo {self.ActiveTab}')
                    TabList[iden].configure(background='#303030')

                    self.TextBox.insert('1.0', self.TabCode[self.ActiveTab])
                    print(f'Current Code: {self.TabCode[self.ActiveTab]}')

                    # self.DB_Cursor.execute(f'SELECT code_{self.ActiveTab + 1} FROM CodeList_{Data[3]} ')
                    # code = self.DB_Cursor.fetchone()

                    # self.TextBox.insert('1.0', code)
 

                def NewCodeTab(): 
                    Tab = tk.Button(TabsFrame, text=str(len(self.TabCode) + 1), bd=0, fg='#999999', bg='#242424', activebackground='#121212', activeforeground='#999999', command=lambda iden = len(self.TabCode): SwitchTab(iden))
                    Tab.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 1))
                    self.TabCode.append('')
                    TabList.append(Tab)

                    print()
                    print('New Code Tab')
                    print(f'len(self.TabCode) = {len(self.TabCode)}')
                    print(f'len(TabList) = {len(TabList)}')
                    print(f'CodeList_{Data[3]}')
                    print(f'cod')
                    print()

                    # self.DB_Cursor.execute(f'ALTER TABLE CodeList_{Data[3]} ADD code_{len(self.TabCode) - 1} TEXT')
                    SwitchTab(len(self.TabCode) - 1)



                TabsFrame = tk.Frame(TextTabFrame, bg='#121212')
                TabsFrame.pack(side=tk.LEFT)

                NewTabImage = self.CreateImage(r'Images\Buttons\NewTab.png')
                NewTabButton = tk.Button(TextTabFrame, image=NewTabImage, bg='#121212', activebackground='#121212', bd=0, command=NewCodeTab)
                NewTabButton.image = NewTabImage
                NewTabButton.pack(side=tk.LEFT)

                self.TextBox = tk.Text(TextBoxFrame, font=self.CodeFont, bg='#333333', fg='#999999', bd=0, padx=10, pady=10)
                self.TextBox.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

                SaveButton = tk.Button(self.CentralSpace, text='Save Card', font='Default 15', bg='#333333', activebackground='#333333', fg='#999999', activeforeground='#999999', bd=0, command=self.SaveCard)
                SaveButton.pack(padx=50, pady=25, anchor='w')

                NewCodeTab()




            NewCard = tk.Button(TopBar, text='New', bg='#303030', activebackground='#999999', fg='#ffffff', bd=0, command=AddCard)
            NewCard.pack(padx=2, pady=2, side=tk.LEFT)

            def DeleteCard():
                if self.ActiveCard == None:
                    return

                else:
                    self.ConnectToDB()

                    self.DB_Cursor.execute(f'''DELETE FROM CodeList_{Data[3]} WHERE id = {self.ActiveCard}''')
                    self.CloseConnectionToDB()
                    
                    self.ResetDB()

                    self.CleanCentralSpace()
                    self.PackCodeList()


            DelCard = tk.Button(TopBar, text='Del', bg='#303030', activebackground='#999999', fg='#ffffff', bd=0, command=DeleteCard)
            DelCard.pack(padx=2, pady=2, side=tk.LEFT)


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
            self.ActiveTab = 0

            TextFont = Font(family='Arial', size=18) #Square721 BT            

            def SwitchTab(iden):
                if self.ActiveTab != None:
                    TabList[self.ActiveTab]. configure(background='#242424')
                
                TxtBox['text'] = TabCode[iden]

            '''AINDA FALTA FAZER 
            
            A PARTE DE MOSTRAR OS O CARD
            COM AS TABS
            '''

            self.CleanCentralSpace()

            self.DB_Cursor.execute(f'''SELECT title FROM CodeList_{Data[3]} WHERE id = {iden}''')
            CodeInfo = self.DB_Cursor.fetchone()

            TitleFont = Font(size=30)
            TitleLabel = tk.Label(self.CentralSpace, text=CodeInfo[0], font=TitleFont, fg='#999999', bg='#121212')
            TitleLabel.pack(padx=50, pady=25, anchor='w')

            self.ActiveCard = iden

            self.ConnectToDB()

            # self.DB_Cursor.execute(f'''SELECT title, code_1 FROM CodeList_{Data[3]} WHERE id = {iden}''')

            # TODO: Count How Many Columns Are There

            self.DB_Cursor.execute(f'''PRAGMA TABLE_INFO(CodeList_1);''')
            RowCount = len(self.DB_Cursor.fetchall())

            TextBoxFrame = tk.Frame(self.CentralSpace, bg='lightblue', height=800, width=1500)
            TextBoxFrame.propagate(0)
            TextBoxFrame.pack(padx=50, anchor='w')

            TextTabFrame = tk.Frame(TextBoxFrame, bg='#121212')
            TextTabFrame.pack(side=tk.TOP, fill=tk.X)

            TabsFrame = tk.Frame(TextTabFrame, bg='#121212')
            TabsFrame.pack(side=tk.LEFT)

            TabList = []
            TabCode = []

            for tab in range(0, RowCount - 3):
                Tab = tk.Button(TabsFrame, text=str(tab + 1), bd=0, fg='#999999', bg='#242424', activebackground='#121212', activeforeground='#999999', command=lambda iden = tab: SwitchTab(iden))
                TabList.append(Tab)
                Tab.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 1))

                # TODO: Get Text From Tab
                self.DB_Cursor.execute(f'''SELECT code_{tab + 1} FROM CodeList_{Data[3]} WHERE ID = {iden}''')
                TabCode.append(self.DB_Cursor.fetchone()[0])

            TxtBox = tk.Message(TextBoxFrame, font=TextFont, bg='#333333', fg='#999999', bd=0, padx=10, pady=10)
            TxtBox.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

            SwitchTab(0)
            
            # TextFrame = tk.Frame(self.CentralSpace, bg='#333333', bd=0)
            # TextFrame.pack(padx=(50, 320), pady=(0, 145), anchor='w', fill=tk.BOTH, expand=True)



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
