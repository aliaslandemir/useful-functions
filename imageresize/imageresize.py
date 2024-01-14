from PIL import Image
import os
from tkinter import filedialog, simpledialog, Tk

def select_directory(title):
    root = Tk()
    root.withdraw()  # Hide the Tkinter root window
    selected_directory = filedialog.askdirectory(title=title)
    return selected_directory

def get_resize_dimensions():
    root = Tk()
    root.withdraw()  # Hide the Tkinter root window
    width = simpledialog.askinteger("Input", "Enter the width:", parent=root, minvalue=1, maxvalue=10000)
    height = simpledialog.askinteger("Input", "Enter the height:", parent=root, minvalue=1, maxvalue=10000)
    return width, height

def resize(directory, dimensions):
    for item in os.listdir(directory):
        file_path = os.path.join(directory, item)
        if os.path.isfile(file_path):
            im = Image.open(file_path)
            f, e = os.path.splitext(file_path)
            imResize = im.resize(dimensions, Image.ANTIALIAS)
            imResize.save(f + '.jpg', 'JPEG', quality=90)

# Select the directory using a GUI
path = select_directory("Select the Directory Containing Images")

# Get resize dimensions from user
width, height = get_resize_dimensions()

# Perform resizing
resize(path, (width, height))
