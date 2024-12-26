import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPixmap, QColor # type: ignore
from PyQt5.QtCore import Qt, QPoint
from PaintApp.py.paint import Ui_MainWindow
from PaintApp.src.drawing_canvas import DrawingCanvas


class MainApp(QMainWindow):
    def __init__(self):
        #test
        super(MainApp, self).__init__()        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.drawing_canvas = DrawingCanvas(self.ui.DrawingFrame)

        self.adjust_drawing_canvas()

        #Connect the buttons
        self.ui.Pencil.setCheckable(True)
        self.ui.Pencil.clicked.connect(self.activate_pencil)
        self.ui.Eraser.setCheckable(True)
        self.ui.Eraser.clicked.connect(self.activate_eraser)

    def adjust_drawing_canvas(self):
        """Adjust the drawing canvas"""
        self.drawing_canvas.setGeometry(0, 0, self.ui.DrawingFrame.width(), self.ui.DrawingFrame.height())
        self.drawing_canvas.update()

    def resizeEvent(self, event):
        self.adjust_drawing_canvas()
        super(MainApp, self).resizeEvent(event)    

    def activate_pencil(self):
        """Activate the pencil"""
        if self.ui.Pencil.isChecked():
            self.drawing_canvas.set_tool("pencil")
            self.ui.Eraser.setChecked(False)
        else:
            self.drawing_canvas.set_tool(None)

    def activate_eraser(self):
        """Activate the eraser"""
        if self.ui.Eraser.isChecked():
            self.drawing_canvas.set_tool("eraser")
            self.ui.Pencil.setChecked(False)
        else:
            self.drawing_canvas.set_tool(None)             


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())