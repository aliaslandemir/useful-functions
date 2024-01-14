import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import Tk

def select_file(title, filetypes):
    root = Tk()
    root.withdraw()  # Hide the Tkinter root window
    selected_file = filedialog.askopenfilename(title=title, filetypes=filetypes)
    return selected_file

# Select the Excel file using a GUI
excel_file = select_file("Select the Excel file", [("Excel files", "*.xlsx")])

# Read the Excel file
file1 = pd.read_excel(excel_file)

# Create a DataFrame
data = {'y_Actual':    file1.actual,
        'y_Predicted': file1.pred
        }

df = pd.DataFrame(data, columns=['y_Actual','y_Predicted'])
confusion_matrix = pd.crosstab(df['y_Actual'], df['y_Predicted'], rownames=['Actual'], colnames=['Predicted'], margins = True)

# Plotting the confusion matrix
plt.title("Confusion Matrix", fontsize =15)
sn.heatmap(confusion_matrix, annot=True, fmt='g')
plt.tight_layout()
plt.savefig('Conf.png', dpi=300)
plt.show()
