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
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        #Add the pencil button
        self.pencil_button = QPushButton("Pencil", self)
        self.pencil_button.setCheckable(True)
        self.pencil_button.clicked.connect(self.activate_pencil)
        layout.addWidget(self.pencil_button)

        #Add the canvas Qlabel
        self.label_canvas = QLabel(self)    
        self.label_canvas.setPixmap(self.canvas)
        layout.addWidget(self.label_canvas)

        #Drawing state
        self.drawing = False
        self.pencil_active = False

        
    def activate_pencil(self):
        """Activate the pencil"""
        if self.pencil_button.isChecked():
            print("Pencil activated")
            self.pencil_active = True
        else:
            print("Pencil deactivated")
            self.pencil_active = False    

    def mousePressEvent(self, event):
        """Mouse button pressed"""
        if self.pencil_active and self.label_canvas.underMouse():
            self.drawing = True
            self.draw_Pixel(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def draw_Pixel(self, event):
        """Draw a pixel"""
        x = (event.x() - self.label_canvas.x()) // self.pixel_size
        y = (event.y() - self.label_canvas.y()) // self.pixel_size

        if 0 <= x < self.canvas_size and 0 <= y < self.canvas_size:
            painter = QPainter(self.canvas)
            painter.setPen(QColor (0, 0, 0))
            painter.drawRect(x * self.pixel_size, y * self.pixel_size, self.pixel_size, self.pixel_size)
            painter.end()
            self.label_canvas.setPixmap(self.canvas)                  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())