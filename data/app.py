from data.database import Database
import tkinter as tk
from tkinter import filedialog
from data.tools import save_to_file
from data import tools
from data import widgets
from data import objects

class App:
    db = Database()
    user = None
    # user = data.User(1, 'Herkules', 'senha', 'default')

    def __init__(self):
        self.start_login()
        if App.user != None: self.start_home()


    def start_login(self):
        root = tk.Tk()
        App.Login(root)
        root.mainloop()


    def start_home(self):
        root = tk.Tk()
        App.Home(root)
        root.mainloop()


    class Login:
        TITLE = 'Login'
        WIDTH, HEIGHT = 950, 500

        def __init__(self, master):
            self.set_up(master)
            # self.load_data()
            self.main_layout()
            # self.login_layout()

        def set_up(self, master):
            self.root = master
            self.root.title(App.Login.TITLE)
            self.root.iconbitmap('rsc/img/app/logo.ico')
            self.root.geometry(f'{App.Login.WIDTH}x{App.Login.HEIGHT}')
            self.root.resizable(False, False)

            self.background = widgets.RegularFrame(self.root)
            self.background.pack(expand=True, fill=tk.BOTH)


        def load_data(self):
            self.profiles = []
            query = App.db.execute_query('SELECT id, img_path FROM User')

            for line in query:
                profile = {'id':line['id'], 'img_path':line['img_path']}
                self.profiles.append(profile)


        def clear_background(self):
            for widget in self.background.winfo_children():
                widget.destroy()


        def main_layout(self, event=None):
            self.clear_background()
            self.load_data()

            self.root.title(App.Login.TITLE)

            self.background.grid_rowconfigure(index=0, weight=1)
            self.background.grid_rowconfigure(index=1, weight=1)
            self.background.grid_rowconfigure(index=2, weight=1)

            self.background.grid_columnconfigure(index=0, weight=1)
            self.background.grid_columnconfigure(index=1, weight=1)
            self.background.grid_columnconfigure(index=2, weight=1)

            info_text = 'Choose your Profile' if len(self.profiles) != 0 else 'Create a new Profile'

            infoLabel = widgets.InfoLabel(self.background, info_text, 20)
            infoLabel.grid(row=0, column=1)

            profileFrame = widgets.RegularFrame(self.background)
            profileFrame.grid(row=1, column=1)

            for profile in self.profiles:
                self.profileButton = widgets.ProfileButton(profileFrame, profile['img_path'], lambda id = profile['id']: self.login_layout(id))
                self.profileButton.pack(side=tk.LEFT, padx=10)

            if len(self.profiles) < 3:
                self.addProfileButton = widgets.ImageButton(profileFrame, 'rsc/img/buttons/add_pfp.png', self.signup_layout)
                self.addProfileButton.pack(side=tk.RIGHT)

                self.root.bind('<Return>', self.signup_layout)
                self.root.bind('<Escape>', self.main_layout)


        def login_layout(self, id=0):
            self.clear_background()

            self.headerFrame = widgets.RegularFrame(self.background)
            self.headerFrame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(5, 0))

            self.returnButton = widgets.ImageButton(self.headerFrame, 'rsc/img/buttons/return.png', self.main_layout)
            self.returnButton.pack(side=tk.LEFT)

            data = App.db.execute_query('SELECT username, img_path FROM User WHERE id = ?', (str(id)))[0]
            self.username = data['username']
            self.img_path = data['img_path']


            self.loginForm = widgets.RegularFrame(self.background)
            self.loginForm.pack(expand=True, fill=tk.BOTH, padx=200, pady=(0, 20))

            self.profileImage = widgets.ProfileLabel(self.loginForm, self.img_path)
            self.profileImage.pack()

            self.usernameLabel = widgets.FormLabel(self.loginForm, self.username)
            self.usernameLabel.pack(pady=(20, 5))

            # self.usernameEntry = widgets.FormEntry(self.loginForm)
            # self.usernameEntry.pack(fill=tk.X, ipady=7, pady=5)

            # self.passwordLabel = widgets.FormLabel(self.loginForm, 'Password:')
            # self.passwordLabel.pack(pady=(15, 5))

            self.passwordEntry = widgets.PasswordEntry(self.loginForm)
            self.passwordEntry.pack(fill=tk.X, ipady=7, pady=5)

            self.passwordEntry.focus_set()

            self.loginButton = widgets.ImageButton(self.loginForm, 'rsc/img/buttons/submit.png', self.login)
            self.loginButton.pack(pady=20)

            self.root.bind('<Return>', self.login)

        
        def login(self, event=None):
            # username = self.usernameEntry.get()
            username = self.username
            password = self.passwordEntry.get()

            query = App.db.execute_query('SELECT * FROM User WHERE username = ? AND password = ?', (username, password))

            if len(query) != 0:
                user = query[0]
                App.user = objects.User(user['id'], user['username'], user['password'], user['img_path'])
                self.root.destroy()


        def signup_layout(self, event=None):
            self.clear_background()
            self.root.title('Signup')

            self.headerFrame = widgets.RegularFrame(self.background)
            self.headerFrame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(5, 0))
            
            self.returnButton = widgets.ImageButton(self.headerFrame, 'rsc/img/buttons/return.png', self.main_layout)
            self.returnButton.pack(side=tk.LEFT)

            self.signupForm = widgets.RegularFrame(self.background)
            self.signupForm.pack(expand=True, fill=tk.BOTH, padx=200)

            

            def clear_signup():
                for widget in self.signupForm.winfo_children():
                    widget.destroy()


            def show_profile(event=None):
                clear_signup()

                infoLabel = widgets.InfoLabel(self.signupForm, 'Your Profile')
                infoLabel.pack(side=tk.TOP, pady=(0, 20))

                profileFrame = widgets.RegularFrame(self.signupForm)
                profileFrame.pack(pady=(0, 30))

                leftFrame = widgets.RegularFrame(profileFrame)
                leftFrame.pack(side=tk.LEFT, padx=10)

                pfpImage = widgets.ProfileButton(leftFrame, self.file_path, search_image)
                pfpImage.pack()


                rightFrame = widgets.RegularFrame(profileFrame)
                rightFrame.pack(side=tk.RIGHT, padx=10)

                usernameLabel = widgets.FormLabel(rightFrame, self.username)
                usernameLabel.pack(anchor='nw')

                passwordLabel = widgets.PasswordLabel(rightFrame, self.password)
                passwordLabel.pack(anchor='sw')

                self.submitButton = widgets.ImageButton(self.signupForm, 'rsc/img/buttons/submit.png', self.signup)
                self.submitButton.pack()

                self.root.bind('<Return>', pfp_layout)
                self.root.bind('<Return>', self.signup)


            def search_image():
                self.file_path = filedialog.askopenfilename(initialdir='/', title='Select A File', filetypes=(("PNG", "*.png"), ("JPEG", "*.jpg"), ("All Files", "*.*")))

                if self.file_path != '':
                    pfp = tools.create_resized_image(self.file_path, (250, 250))
                    self.pfpButton['image'] = pfp
                    self.pfpButton.image = pfp


            def pfp_layout(event=None): 
                clear_signup()
                self.returnButton['command'] = password_layout
                
                self.file_path = 'rsc/img/buttons/default_pfp.png'

                infoLabel = widgets.InfoLabel(self.signupForm, 'Click on the image to change it')
                infoLabel.pack(pady=(0, 10))

                self.pfpButton = widgets.ImageButton(self.signupForm, 'rsc/img/buttons/default_pfp.png', search_image)
                self.pfpButton.pack()

                self.submitButton = widgets.ImageButton(self.signupForm, 'rsc/img/buttons/submit.png', show_profile)
                self.submitButton.pack(pady=20)

                self.root.bind('<Return>', show_profile)
                self.root.bind('<Return>', show_profile)


            def validate_password(event=None):
                password_1 = self.passwordEntry1.get()
                password_2 = self.passwordEntry2.get()

                if password_1 == password_2:
                    self.password = password_1
                    pfp_layout()


            def password_layout(event=None):
                clear_signup()

                self.returnButton['command'] = username_layout

                self.passwordLabel = widgets.FormLabel(self.signupForm, 'Password:')
                self.passwordLabel.pack(pady=(45, 5))

                self.passwordEntry1 = widgets.PasswordEntry(self.signupForm)
                self.passwordEntry1.pack(fill=tk.X, ipady=7, pady=5)

                self.passwordEntry1.focus_set()

                self.passwordEntry2 = widgets.PasswordEntry(self.signupForm)
                self.passwordEntry2.pack(fill=tk.X, ipady=7, pady=5)

                self.submitButton = widgets.ImageButton(self.signupForm, 'rsc/img/buttons/submit.png', validate_password)
                self.submitButton.pack(pady=20)

                self.root.bind('<Return>', validate_password)
                self.root.bind('<Escape>', username_layout)

            def validate_username(event=None):
                self.username = self.usernameEntry.get()
                if len(self.username) != 0:
                    password_layout()


            def username_layout(event=None):
                clear_signup()
                
                self.returnButton['command'] = self.main_layout

                self.usernameLabel = widgets.FormLabel(self.signupForm, 'Username:')
                self.usernameLabel.pack(pady=(70, 5))

                self.usernameEntry = widgets.FormEntry(self.signupForm)
                self.usernameEntry.pack(fill=tk.X, ipady=7, pady=5)

                self.usernameEntry.focus_set()

                self.submitButton = widgets.ImageButton(self.signupForm, 'rsc/img/buttons/submit.png', validate_username)
                self.submitButton.pack(pady=20)

                self.root.bind('<Return>', validate_username)
                self.root.bind('<Escape>', self.main_layout)

            username_layout()


        def signup(self, event=None):
            App.db.execute_statement('INSERT INTO User (username, password, img_path) VALUES (?, ?, ?)', (self.username, self.password, self.file_path))

            self.main_layout()


    class Home:
        TITLE = 'MyCodes'

        def __init__(self, master):
            self.set_up(master)
            self.load_data()
            self.main_layout()
            self.sidebard_layout()
            self.mainframe_layout()
        
        
        def set_up(self, master):
            self.root = master
            self.root.title(App.Home.TITLE)
            self.root.iconbitmap('rsc/img/app/logo.ico')
            self.root.state('zoomed')


        def load_data(self):
            self.cards = []
            query = App.db.execute_query('SELECT * FROM Card WHERE user_id = ?', (str(App.user.id)))

            for line in query:
                card = objects.Card(line['id'], line['title'], line['language'], line['code'], line['user_id'])
                self.cards.append(card)


        def main_layout(self):
            self.background = tk.Frame(self.root)
            self.background.pack(expand=True, fill=tk.BOTH)

            self.background.grid_columnconfigure(0, weight=3)
            self.background.grid_columnconfigure(1, weight=10)

            self.background.grid_rowconfigure(0, weight=1)

            self.sidebar = widgets.SideBar(self.background)
            self.sidebar.grid(row=0, column=0, sticky='nsew')
            # self.sideBar.pack(side=tk.LEFT, fill=tk.Y)

            self.mainframe = widgets.MainFrame(self.background)
            self.mainframe.grid(row=0, column=1, sticky='nsew')
            # self.mainFrame.pack(expand=True, fill=tk.BOTH)

            # self.sidebar.bind('<Button-1>', self.mainframe_layout)


        def sidebard_layout(self):
            self.sidebarMenu = widgets.SideBar(self.sidebar)
            self.sidebarMenu.pack(fill=tk.X, ipady=5)

            self.addButton = widgets.SidebarButton(self.sidebarMenu, 'rsc/img/buttons/add.png', self.add_card)
            self.addButton.pack(side=tk.LEFT, padx=5)

            self.deleteButton = widgets.SidebarButton(self.sidebarMenu, 'rsc/img/buttons/delete.png', self.delete_card)
            self.deleteButton.pack(side=tk.LEFT, padx=5)

            self.refreshButton = widgets.SidebarButton(self.sidebarMenu, 'rsc/img/buttons/refresh.png', self.refresh_cards)
            self.refreshButton.pack(side=tk.LEFT, padx=5)

            self.cardlistFrame = widgets.SideBar(self.sidebar)
            self.cardlistFrame.pack(fill=tk.BOTH)

            self.card_frames = []
            self.list_cards()


        def list_cards(self):
            for widget in self.cardlistFrame.winfo_children():
                widget.destroy()

            self.last_open_card = None

            for index, card in enumerate(self.cards):
                cardFrame = widgets.CardFrame(self.cardlistFrame, card)
                cardFrame.pack_propagate(0)
                cardFrame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
                cardFrame.bind('<Button-1>', lambda event, i=index: self.open_card(index=i))

                self.card_frames.append(cardFrame)
                self.last_open_card = cardFrame




        def mainframe_layout(self, event=None):
            self.clear_mainframe()

            self.cardForm = widgets.RegularFrame(self.mainframe)
            self.cardForm.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)

            # self.cardForm.grid_rowconfigure(index=0, weight=10)
            # self.cardForm.grid_rowconfigure(index=1, weight=10)

            self.informationFrame = widgets.RegularFrame(self.cardForm)
            self.informationFrame.pack(side=tk.TOP, fill=tk.X)
            # self.informationFrame.grid(row=0, column=0)

            self.informationFrame.grid_columnconfigure(index=1, weight=1)

            self.lblLanguage = widgets.LanguageLabel(self.informationFrame, 'Language: ')
            self.lblLanguage.grid(row=0, column=0, sticky='w')

            self.languageEntry = widgets.LanguageEntry(self.informationFrame, '<LANGUAGE>')
            self.languageEntry.grid(row=0, column=1, sticky='ew')

            self.languageEntry.focus_set()

            self.languageUnderline = widgets.EntryUnderline(self.informationFrame)
            self.languageUnderline.grid(row=0, column=1, sticky='sew')
            
            self.lblTitle = widgets.TitleLabel(self.informationFrame, 'Title: ')
            self.lblTitle.grid(row=1, column=0, sticky='w', pady=(10, 0))

            self.titleEntry = widgets.TitleEntry(self.informationFrame, '<TITLE>')
            self.titleEntry.grid(row=1, column=1, sticky='ew')

            self.titleUnderline = widgets.EntryUnderline(self.informationFrame, 2)
            self.titleUnderline.grid(row=1, column=1, sticky='sew')

            self.codeFrame = widgets.RegularFrame(self.cardForm)
            self.codeFrame.pack(side=tk.TOP, expand=True, fill=tk.BOTH, pady=(10, 0))
            # self.codeFrame.grid(row=1, column=0)

            self.txtCode = widgets.CodeText(self.codeFrame)
            # self.txtCode.grid(row=2, column=0, columnspan=2)
            self.txtCode.pack(expand=True, fill=tk.BOTH)

            self.menuFrame = widgets.RegularFrame(self.cardForm)
            self.menuFrame.pack(fill=tk.X, pady=(20, 0))

            self.saveButton = widgets.ImageButton(self.menuFrame, 'rsc/img/buttons/save.png', self.save_card)
            self.saveButton.pack(side=tk.LEFT)

            self.clearButton = widgets.ImageButton(self.menuFrame, 'rsc/img/buttons/clear.png', self.clear_card)
            self.clearButton.pack(side=tk.LEFT, padx=10)


            if len(self.cards) == 0:
                self.add_card()
                self.open_card()

            else:
                self.open_card(index=self.card_frames.index(self.last_open_card))


        def add_card(self):
            App.db.execute_statement('INSERT INTO Card (title, language, code, user_id) VALUES (?, ?, ?, ?)', ('', '', '', App.user.id))
            card_id = App.db.cursor.lastrowid

            card = objects.Card(card_id, '', '', '', App.user.id)
            self.cards.append(card)

            cardFrame = widgets.CardFrame(self.cardlistFrame, card)
            cardFrame.pack_propagate(0)
            cardFrame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
            cardFrame.bind('<Button-1>', lambda event, i=self.cards.index(card): self.open_card(index=i))
            
            self.card_frames.append(cardFrame)

            if self.last_open_card != None: self.last_open_card.deselect()
            self.last_open_card = cardFrame
            self.open_card(index=self.cards.index(card))

            # self.list_cards()
            # self.refresh_cards()


        def delete_card(self):
            if len(self.card_frames) <= 1: return

            card_frame = self.last_open_card
            id = str(card_frame.card.id)
            App.db.execute_statement('DELETE FROM Card WHERE id = ?', (id,))
            self.card_frames.remove(card_frame)
            self.last_open_card = self.card_frames[-1]
            
            self.refresh_cards()


        def refresh_cards(self):
            to_select = self.card_frames.index(self.last_open_card)

            for widget in self.cardlistFrame.winfo_children():
                widget.destroy()

            self.load_data()

            self.card_frames = []
            for index, card in enumerate(self.cards):

                cardFrame = widgets.CardFrame(self.cardlistFrame, card)
                cardFrame.pack_propagate(0)
                cardFrame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
                cardFrame.bind('<Button-1>', lambda event, i=index: self.open_card(index=i))

                self.card_frames.append(cardFrame)

            self.last_open_card = self.card_frames[to_select]
            self.open_card(index=to_select)


        def open_card(self, event=None, index=0):
            self.last_open_card.deselect()
    
            self.card = self.cards[index]

            for card_frame in self.card_frames:
                if card_frame.card == self.card:
                    card_frame.select()
                    self.last_open_card = card_frame


            # self.languageEntry['text'] = self.card.language
            # self.titleEntry['text'] = self.card.title

            self.languageEntry.delete(0, tk.END)
            self.titleEntry.delete(0, tk.END)

            self.languageEntry.insert(tk.END, self.card.language)
            self.titleEntry.insert(tk.END, self.card.title)

            self.txtCode.delete('1.0', tk.END)
            self.txtCode.insert(tk.END, self.card.code)

            
        def save_card(self):
            id = self.card.id
            language = self.languageEntry.get()
            title = self.titleEntry.get()
            code = self.txtCode.get('1.0', tk.END)
            user_id = self.card.user_id

            # card = objects.Card(0, title, language, code, App.user.id)
            # App.db.execute_statement('INSERT INTO Card (title, language, code, user_id) VALUES (?, ?, ?, ?)', (card.title, card.language, card.code, card.user_id))

            App.db.execute_statement('UPDATE Card SET title = ?, language = ?, code = ? WHERE id = ? AND user_id = ?', (title, language, code, id, user_id))

            self.refresh_cards()
            
        
        def clear_card(self):
            self.languageEntry.delete(0, tk.END)
            self.titleEntry.delete(0, tk.END)
            self.txtCode.delete('1.0', tk.END)

        def clear_mainframe(self):
            for widget in self.mainframe.winfo_children():
                widget.destroy()


def start():
    App()