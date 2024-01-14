from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from tkinter import filedialog
from tkinter import Tk

def select_image():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename()
    return file_path

def show_image(title, img):
    plt.figure(title)
    plt.imshow(img, cmap='gray' if len(img.shape) == 2 else None)
    plt.show()

# Main workflow
img_path = select_image()
img = Image.open(img_path)
img = np.array(img)

show_image('Original', img)

# Convert to grayscale
if len(img.shape) == 3:
    gray = np.mean(img, axis=2).astype(np.uint8)  # Simple average to convert to grayscale
    show_image('Grayscale', gray)
else:
    gray = img

# The rest of your processing steps...
# Note: PIL and Matplotlib have limitations compared to OpenCV for advanced operations.

# Example: Simple thresholding (replace with Otsu's method if needed)
threshold_value = 128  # Example threshold value
thresh = (gray > threshold_value) * 255
show_image('Thresholding', thresh)

# Example: Histogram of the intensities in the grayscale image
plt.hist(gray.ravel(), 256)
plt.show()

