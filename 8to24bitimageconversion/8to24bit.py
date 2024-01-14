import os
from tkinter import filedialog
from tkinter import Tk
from PIL import Image

def select_folder(title):
    root = Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory(title=title)  # Show the folder selection dialog
    return folder_path

def turnto24(path, newpath):
    files = os.listdir(path)
    files = sorted(files)
    
    for f in files:
        imgpath = os.path.join(path, f)
        img = Image.open(imgpath)

        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Save the image in the new directory
        file_name, file_extension = os.path.splitext(f)
        dst = os.path.join(os.path.abspath(newpath), file_name + '.jpg')
        img.save(dst)

# Select source and destination folders
source_folder = select_folder("Select the source folder")
destination_folder = select_folder("Select the destination folder")

turnto24(source_folder, destination_folder)
