from PIL import ImageTk, Image

def create_image(path):
    file = Image.open(path)
    tkimage = ImageTk.PhotoImage(file)

    return tkimage


def create_resized_image(path, size):
    file = Image.open(path)
    tkimage = ImageTk.PhotoImage(file.resize(size))

    return tkimage


def save_to_file(file_name, content):
    with open(f'saves/{file_name}', 'at') as file:
        file.write(content)