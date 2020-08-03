from PIL import ImageTk, Image
import tkinter as tk
import sys
import sqlite3

data = sys.argv[1:]

# print(args)

MainWindow = tk.Tk()
MainWindow.title('MyCodes')
MainWindow.state('zoomed')
# MainWindow.resizable(False, False)
MainWindow.configure(background='#121212')

def OpenCode(iden):

    TitleLabel = tk.Label(CentralSpace, text=iden)
    TitleLabel.pack()


def CodeList():

    for Item in range(0, 15):

        button = tk.Button(ListBar, text=str(Item), bg='#808080', activebackground='#999999', bd=0, command=lambda iden = Item: OpenCode(str(iden)))
        button.pack(padx=5, pady=1, fill=tk.BOTH)
        

def MainView(argv1=1):

    global ListBar, CentralSpace

    SideBar = tk.Frame(MainWindow, width=250, bg='#242424', bd=0) #212121
    SideBar.pack(side=tk.LEFT, fill=tk.Y)

    TopBar = tk.Frame(MainWindow, height=30, bg='#242424', bd=0) #303030 262626
    TopBar.pack(side=tk.TOP, fill=tk.X)

    CentralSpace = tk.Frame(MainWindow, bg='#121212', bd=0)
    CentralSpace.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    ProfileBar = tk.Frame(SideBar, height=70, width=250, bg='#303030', bd=0)
    ProfileBar.pack(side=tk.TOP, fill=tk.X)
    ProfileBar.pack_propagate(0)

    ProfileFrame = tk.Frame(ProfileBar, bg='#303030')
    ProfileFrame.pack(side=tk.LEFT, padx=10)

    IconFile = Image.open(data[2])
    IconImage = ImageTk.PhotoImage(IconFile.resize((60, 60), Image.ANTIALIAS))
    ProfileButton = tk.Button(ProfileFrame, image=IconImage, bg='#303030', activebackground='#303030', bd=0)
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