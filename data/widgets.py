import tkinter as tk
from tkinter.font import Font
from data import tools

# WIDGETS FOR:
# General Use

class RegularFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self['bg'] = '#121212' #121212


class ImageButton(tk.Button):
    def __init__(self, master, img_path, command):
        super().__init__(master)
        img = tools.create_image(img_path)

        self['bd'] = 0
        self['bg'] = '#121212'
        self['activebackground'] = '#121212'
        self['image'] = img
        self.image = img
        self['relief'] = tk.FLAT
        self['command'] = command

# WIDGETS FOR:
# Login

class ProfileButton(tk.Button):
    def __init__(self, master, img_path, command):
        super().__init__(master)
        img = tools.create_resized_image(img_path, (250, 250))

        self['bd'] = 0
        self['bg'] = '#121212'
        self['activebackground'] = '#121212'
        self['image'] = img
        self.image = img
        self['relief'] = tk.FLAT
        self['command'] = command


class FormLabel(tk.Label):
    def __init__(self, master, text):
        super().__init__(master)
        self['text'] = text
        self['bg'] = '#121212'
        self['fg'] = '#808080'
        self['font'] = Font(family='OpenSans', size=30)



class FormEntry(tk.Entry):
    def __init__(self, master):
        super().__init__(master)
        self['bd'] = 0
        self['bg'] = '#333333'
        self['fg'] = '#999999'
        self['font'] = Font(family='OpenSans', size=20)
        self['justify'] = tk.CENTER
        self['insertbackground'] = '#dbdbdb'


class PasswordEntry(tk.Entry):
    def __init__(self, master):
        super().__init__(master)
        self['bd'] = 0
        self['bg'] = '#333333'
        self['fg'] = '#999999'
        self['font'] = Font(family='OpenSans', size=20)
        self['justify'] = tk.CENTER
        self['show'] = '•'
        self['insertbackground'] = '#dbdbdb'


class InfoLabel(tk.Label):
    def __init__(self, master, text):
        super().__init__(master)
        self['text'] = text
        self['bg'] = '#121212'
        self['fg'] = '#808080'
        self['font'] = Font(family='OpenSans', size=15)


class PasswordLabel(tk.Label):
    def __init__(self, master, text):
        super().__init__(master)
        self['text'] = '•' * len(text)
        self['bg'] = '#121212'
        self['fg'] = '#808080'
        self['font'] = Font(family='OpenSans', size=15)


# WIDGETS FOR:
# Home

class SideBar(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self['bg'] = '#242424'
        self['width'] = 200


class SidebarButton(tk.Button):
    def __init__(self, master, img_path, command):
        super().__init__(master)
        img = tools.create_image(img_path)

        self['bd'] = 0
        self['bg'] = '#242424'
        self['activebackground'] = '#242424'
        self['image'] = img
        self.image = img
        self['relief'] = tk.FLAT
        self['command'] = command


class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self['bg'] = '#121212'
    

class CardFrame(tk.Frame):
    BG = '#808080'
    FG = '#242424'

    def __init__(self, master, card):
        super().__init__(master)
        self['bg'] = CardFrame.BG
        self['height'] = 45
        
        self.TitleLabel(self, card.title).pack(side=tk.TOP, anchor='w', padx=(5, 0))
        self.TitleLabel(self, f'Language: {card.language}').pack(side=tk.TOP, anchor='w', padx=(5, 0))


    class TitleLabel(tk.Label):
        def __init__(self, wrapper, title):
            super().__init__(wrapper)
            self['text'] = title
            self['bg'] = CardFrame.BG
            self['fg'] = CardFrame.FG
            self['font'] = Font(family='Arial', size=10)
        


class LanguageLabel(tk.Label):
    BG = '#121212'
    FG = '#808080'

    def __init__(self,master, language):
        super().__init__(master)
        self['bg'] = LanguageLabel.BG
        self['fg'] = LanguageLabel.FG
        self['text'] = language
        self['font'] = Font(family='Arial', size=12)


class LanguageEntry(tk.Entry):
    BG = '#121212'
    FG = '#808080'

    def __init__(self,master, language):
        super().__init__(master)
        self['bd'] = 0
        self['bg'] = LanguageLabel.BG
        self['fg'] = LanguageLabel.FG
        self['text'] = language
        self['font'] = Font(family='Arial', size=12)
        self['insertbackground'] = '#dbdbdb'


class TitleLabel(tk.Label):
    BG = '#121212'
    FG = '#808080'

    def __init__(self, master, title):
        super().__init__(master)
        self['bg'] = TitleLabel.BG
        self['fg'] = TitleLabel.FG
        self['text'] = title
        self['font'] = Font(family='Arial', size=20)


class TitleEntry(tk.Entry):
    BG = '#121212'
    FG = '#808080'

    def __init__(self, master, title):
        super().__init__(master)
        self['bd'] = 0
        self['bg'] = TitleLabel.BG
        self['fg'] = TitleLabel.FG
        self['text'] = title
        self['font'] = Font(family='Arial', size=20)
        self['insertbackground'] = '#dbdbdb'


class CodeText(tk.Text):
    def __init__(self, master):
        super().__init__(master)
        # self['width'] = 100
        # self['height'] = 100
        self['bd'] = 0
        self['bg'] = '#171717' #171717
        self['fg'] = '#84ff2b'
        self['font'] = Font(family='consolas', size=16)
        self['insertbackground'] = '#dbdbdb'
        # self.insert(tk.END, code)


