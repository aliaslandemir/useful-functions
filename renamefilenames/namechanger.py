import os
from tkinter import filedialog
from tkinter import Tk

def select_directory(title):
    root = Tk()
    root.withdraw()  # Hide the Tkinter root window
    selected_directory = filedialog.askdirectory(title=title)
    return selected_directory

def rename_recursively(path):
    if os.path.isdir(path):
        content = os.listdir(path)
        for _file in content:
            full_path = os.path.join(path, _file)
            rename_recursively(full_path)
    else:
        new_path = path.replace('binary', 'fluorescence')
        os.rename(path, new_path)

# Select the directory using a GUI
dir_path = select_directory("Select the Directory")

rename_recursively(dir_path)
