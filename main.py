import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtCore import Qt, QPoint
from PaintApp.py.paint import Ui_Qdrawer

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Qdrawer()
        self.ui.setupUi(self)

        #Canvas initialization
        self.canvas_size = 25
        self.pixel_size = 25
        self.canvas = QPixmap(self.canvas_size * self.pixel_size, self.canvas_size * self.pixel_size)
        self.canvas.fill(Qt.white)

        #Central widget and layout
        self.label_canvas = QLabel(self)
        self.label_canvas.setPixmap(self.canvas)

        #center the canvas
        self.label_canvas.setGeometry(50, 100, self.canvas_size * self.pixel_size, self.canvas_size * self.pixel_size)

        #Drawing state
        self.drawing = False
        self.activate_tool = None #Pencil or eraser

        #Connect the pencil button
        self.ui.Pencil.setCheckable(True)
        self.ui.Pencil.clicked.connect(self.activate_pencil)

        #connect the eraser button
        self.ui.eraser.setCheckable(True)
        self.ui.eraser.clicked.connect(self.activate_eraser)

    def activate_eraser(self):
        """Activate the eraser"""
        if self.ui.eraser.isChecked():
            print("Eraser activated")
            self.activate_tool = "eraser"
            self.ui.Pencil.setChecked(False) #Desactivate the pencil
        else: 
            print("Eraser deactivated")
            self.activate_tool = None

        
    def activate_pencil(self):
        """Activate the pencil"""
        if self.ui.Pencil.isChecked():
            print("Pencil activated")
            self.activate_tool = "Pencil"
            self.ui.eraser.setChecked(False) #Desactivate the eraser
        else:
            print("Pencil deactivated")
            self.activate_tool = None 

    def mouseMoveEvent(self, event):
        """Continue drawing or erasing while mouse is moving"""
        if self.drawing and self.label_canvas.underMouse():
            self.modify_pixel(event)       

    def mousePressEvent(self, event):
        """Mouse button pressed"""
        if self.activate_tool and self.label_canvas.underMouse():
            self.drawing = True
            self.modify_pixel(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def modify_pixel(self, event):
        """Modify a pixel on the canvas  draw or erase"""
        x = (event.x() - self.label_canvas.x()) // self.pixel_size
        y = (event.y() - self.label_canvas.y()) // self.pixel_size

        if 0 <= x < self.canvas_size and 0 <= y < self.canvas_size:
            painter = QPainter(self.canvas)
            if self.activate_tool == "Pencil":
                painter.fillRect(x * self.pixel_size, y * self.pixel_size, self.pixel_size, self.pixel_size, QColor(0, 0, 0))
            elif self.activate_tool == "eraser":
                painter.fillRect(x * self.pixel_size, y * self.pixel_size, self.pixel_size, self.pixel_size, QColor(255, 255, 255))
            painter.end()
            self.label_canvas.setPixmap(self.canvas)    

                    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())