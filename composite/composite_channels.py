# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 22:33:31 2024

@author: aad
"""

import sys
import numpy as np
import imageio.v2 as imageio
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QFileDialog, QMessageBox, QGroupBox)
from PyQt5.QtCore import Qt, QRect  # Corrected import for QRect
from PyQt5.QtGui import QImage, QPixmap, QPainter, QFont, QColor


class ImageMergerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.original_images = [None, None, None]  # Store the original images
        self.thresholded_images = [None, None, None]  # Store images after thresholding
        self.initUI()

    def initUI(self):
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

        # Left Side Layout for Load Buttons and Threshold Sliders
        loadGroup = QGroupBox("Load and Adjust Images")
        self.leftLayout = QVBoxLayout()
        loadGroup.setLayout(self.leftLayout)
        self.loadButtons = []
        self.sliders = []
        self.colorNames = ['Red', 'Green', 'Blue']
        for i, color in enumerate(self.colorNames):
            btn = QPushButton(f'Load {color} Image')
            btn.clicked.connect(lambda checked, idx=i: self.loadImage(idx))
            self.leftLayout.addWidget(btn)
            self.loadButtons.append(btn)

            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(65535)
            slider.valueChanged.connect(lambda value, idx=i: self.adjustThreshold(value, idx))
            self.leftLayout.addWidget(slider)
            self.sliders.append(slider)
        self.mainLayout.addWidget(loadGroup)

        # Middle Layout for Displaying Images
        self.imageDisplayLayout = QVBoxLayout()
        self.imageLabels = [QLabel() for _ in range(3)]
        for label in self.imageLabels:
            self.imageDisplayLayout.addWidget(label)
        imageDisplayGroup = QGroupBox("Image Previews")
        imageDisplayGroup.setLayout(self.imageDisplayLayout)
        self.mainLayout.addWidget(imageDisplayGroup)

        # Right Side for Merge Button, Annotations, and Result Display
        self.rightLayout = QVBoxLayout()
        actionGroup = QGroupBox("Actions and Result")
        actionGroup.setLayout(self.rightLayout)
        
        self.mergeButton = QPushButton('Merge Images')
        self.mergeButton.clicked.connect(self.mergeImages)
        self.rightLayout.addWidget(self.mergeButton)
        
        self.addAnnotationsButton = QPushButton('Add Scale Bar and Colorbars', self)
        self.addAnnotationsButton.clicked.connect(self.addAnnotations)
        self.rightLayout.addWidget(self.addAnnotationsButton)

        self.resultLabel = QLabel()
        self.rightLayout.addWidget(self.resultLabel)
        
        self.saveButton = QPushButton('Save Merged Image', self)
        self.saveButton.clicked.connect(self.saveMergedImage)
        self.rightLayout.addWidget(self.saveButton)
        
        self.mainLayout.addWidget(actionGroup)
        
        self.setWindowTitle('Image Merger with Threshold Adjustment')
        self.setGeometry(100, 100, 1200, 400)



    def loadImage(self, index):
        path, _ = QFileDialog.getOpenFileName(self, f'Select {self.colorNames[index]} Image', '', 'Images (*.png *.jpg *.bmp *.tif)')
        if path:
            # Load with imageio to handle 16-bit depth correctly
            self.original_images[index] = imageio.imread(path)
            self.displayImage(index)

    def displayImage(self, index):
        if self.original_images[index] is not None:
            img = QImage(self.original_images[index].data, self.original_images[index].shape[1], self.original_images[index].shape[0], QImage.Format_Grayscale16)
            pixmap = QPixmap.fromImage(img).scaled(256, 256, Qt.KeepAspectRatio)
            self.imageLabels[index].setPixmap(pixmap)

    def adjustThreshold(self, value, index):
        if self.original_images[index] is not None:
            # Apply threshold
            thresholded_image = self.original_images[index].copy()
            thresholded_image[thresholded_image < value] = 0
            self.thresholded_images[index] = thresholded_image
            
            # Ensure the array is contiguous
            thresholded_image = np.ascontiguousarray(thresholded_image)
    
            # Create QImage from the contiguous array
            img = QImage(thresholded_image.data, thresholded_image.shape[1], thresholded_image.shape[0], thresholded_image.strides[0], QImage.Format_Grayscale16)
            pixmap = QPixmap.fromImage(img).scaled(256, 256, Qt.KeepAspectRatio)
            self.imageLabels[index].setPixmap(pixmap)


    def mergeImages(self):
        if not all(img is not None for img in self.thresholded_images):
            QMessageBox.information(self, "Incomplete Data", "Please load and set threshold for all three images before merging.")
            return
        # Assuming all images are the same size, create an empty array for the RGB image
        height, width = self.thresholded_images[0].shape
        merged_image = np.zeros((height, width, 3), dtype=np.uint16)
        for i in range(3):
            merged_image[..., i] = self.thresholded_images[i] / np.max(self.thresholded_images[i]) * 65535
        merged_image = merged_image.astype(np.uint16)
        img = QImage(merged_image.data, merged_image.shape[1], merged_image.shape[0], merged_image.strides[0], QImage.Format_RGB16)
        self.mergedQImage = QImage(merged_image.data, merged_image.shape[1], merged_image.shape[0], merged_image.strides[0], QImage.Format_RGB16)  # Store the QImage
        pixmap = QPixmap.fromImage(self.mergedQImage).scaled(256, 256, Qt.KeepAspectRatio)  # Use the QImage for QPixmap creation
        self.resultLabel.setPixmap(pixmap)


    def addAnnotations(self):
        if self.resultLabel.pixmap() is None:
            QMessageBox.warning(self, "Warning", "Merge images first before adding annotations.")
            return
        
        # Assume the pixmap size reflects the merged image size
        pixmap = self.resultLabel.pixmap()
        painter = QPainter(pixmap)
        
        # Set painter for white text and lines
        painter.setPen(Qt.white)
        
        # Draw Scale Bar - 10 micrometers represented
        scaleBarLengthPixels = int(100 / 2.20)  # 100 micrometers / pixel size in micrometers
        bottomRightX = pixmap.width() - 15  # Adjust as needed
        bottomRightY = pixmap.height() - 15
        painter.drawLine(bottomRightX - scaleBarLengthPixels, bottomRightY, bottomRightX, bottomRightY)
        painter.drawText(bottomRightX - scaleBarLengthPixels, bottomRightY + 15, "100 µm")
        
        # Draw Colorbars - example for three fluorophores
        colorNames = ['Red', 'Green', 'Blue']
        colors = [Qt.red, Qt.green, Qt.blue]
        for i, (colorName, color) in enumerate(zip(colorNames, colors)):
            painter.setPen(color)
            painter.drawText(20, 10 * (i + 1), colorName)
        
        painter.end()
        self.resultLabel.setPixmap(pixmap)
        
        
    def saveMergedImage(self):
        if not hasattr(self, 'mergedQImage'):
            QMessageBox.warning(self, "Warning", "No merged image to save.")
            return
        
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Image (*.png);;JPEG Image (*.jpg);;All Files (*)")
        if filePath:
            self.mergedQImage.save(filePath)  # Save the QImage directly



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageMergerApp()
    ex.show()
    sys.exit(app.exec_())
