from PIL import Image
import glob
import os
from tkinter import filedialog
from tkinter import Tk

def select_folder(title):
    root = Tk()
    root.withdraw()  # Hide the Tkinter root window
    selected_folder = filedialog.askdirectory(title=title)
    return selected_folder

# Select source and destination folders using a GUI
source_folder = select_folder("Select the source folder")
out_dir = select_folder("Select the destination folder")

cnt = 0
for img in glob.glob(os.path.join(source_folder, '*'), recursive=True):
    Image.open(img).save(os.path.join(out_dir, f'{cnt}.png'))
    cnt += 1
