import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtCore import Qt, QPoint
from PaintApp.py.paint import Ui_MainWindow

class MainApp(QMainWindow):
    def __init__(self):
        #test
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())

        #Canvas configuration
        self.canvas_size = 100
        self.zoom_factor = 10
    

        self.canvas = QPixmap(self.canvas_size, self.canvas_size)
        self.canvas.fill(Qt.white)

        #Label configuration 
        self.label_canvas = QLabel(self.ui.centralwidget)
        self.update_canvas_dipslay()

        #add the canvas to the layout
        self.ui.verticalLayout = QVBoxLayout(self.ui.centralwidget)
        self.ui.verticalLayout.addWidget(self.ui.horizontalLayoutWidget)
        self.ui.verticalLayout.addWidget(self.label_canvas)

        #Drawing state
        self.drawing = False
        self.activate_tool = None #Pencil or eraser

        #Connect the pencil button
        self.ui.Pencil.setCheckable(True)
        self.ui.Pencil.clicked.connect(self.activate_pencil)

        #connect the eraser button
        self.ui.Eraser.setCheckable(True)
        self.ui.Eraser.clicked.connect(self.activate_eraser)

    def update_canvas_dipslay(self):
        """Update the canvas display based on the zoom factor"""
        zoomed_canvas = self.canvas.scaled(
            int(self.canvas_size * self.zoom_factor),
            int(self.canvas_size * self.zoom_factor),
            Qt.IgnoreAspectRatio
        )
        self.label_canvas.setPixmap(zoomed_canvas)
        self.label_canvas.setFixedSize(int(self.canvas_size * self.zoom_factor), int(self.canvas_size * self.zoom_factor))
        self.adjustSize()

    def wheelEvent(self, event):
       delta = event.angleDelta().y() / 120
       new_zoom = self.zoom_factor + delta
       if 1 <= new_zoom <= 50:
            self.zoom_factor = int(new_zoom)
            self.update_canvas_dipslay()

    def activate_eraser(self):
        """Activate the eraser"""
        if self.ui.Eraser.isChecked():
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
            self.ui.Eraser.setChecked(False) #Desactivate the eraser
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
        local_pos = self.label_canvas.mapFromGlobal(event.globalPos())
        x = int(local_pos.x() // self.zoom_factor)
        y = int(local_pos.y() // self.zoom_factor)

        if 0 <= x < self.canvas_size and 0 <= y < self.canvas_size:
            painter = QPainter(self.canvas)
            if self.activate_tool == "Pencil":
                painter.drawPoint(x, y)
                painter.setPen(QColor(Qt.black))
            elif self.activate_tool == "eraser":
                painter.setPen(QColor(Qt.white))
                painter.drawPoint(x, y)                
            painter.end()
            self.label_canvas.setPixmap(self.canvas)    

            zoomed_canvas = self.canvas.scaled(self.canvas_size * self.zoom_factor, self.canvas_size * self.zoom_factor, Qt.IgnoreAspectRatio)
            self.label_canvas.setPixmap(zoomed_canvas)
                    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())