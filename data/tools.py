from PIL import ImageTk, Image, ImageOps, ImageDraw

def round_image(img, size):
    bigsize = (size[0] * 3, size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(size, Image.ANTIALIAS)

    rounded = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    rounded.putalpha(mask)

    return rounded


def create_image(path):
    file = Image.open(path)
    tkimage = ImageTk.PhotoImage(file)

    return tkimage


def create_resized_image(path, size, round=False):
    file = Image.open(path)

    if round:
        tkimage = ImageTk.PhotoImage(round_image(file.resize(size, Image.ANTIALIAS), size))
    else:
        tkimage = ImageTk.PhotoImage(file.resize(size))

    return tkimage


def save_to_file(file_name, content):
    with open(f'saves/{file_name}', 'at') as file:
        file.write(content)