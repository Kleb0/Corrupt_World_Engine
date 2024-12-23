from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtCore import Qt



class DrawingCanvas(QFrame):
    def __init__(self, parent=None):
        super(DrawingCanvas, self).__init__(parent)
        self.canvas = QPixmap(self.width(), self.height())
        self.canvas.fill(Qt.white)
        self.drawing = False
        self.activate_tool = None  # Pencil or eraser
        self.pen_color = QColor(Qt.black)


    def set_tool(self, tool):
        """Set the active tool"""
        self.activate_tool = tool

    def mousePressEvent(self, event):
        if self.activate_tool and event.button() == Qt.LeftButton:
            self.drawing = True
            self.modify_pixel(event)

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.modify_pixel(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def modify_pixel(self, event):
        """Modify a pixel on the canvas"""
        x = event.pos().x()
        y = event.pos().y()

        if 0 <= x < self.canvas.width() and 0 <= y < self.canvas.height():
            painter = QPainter(self.canvas)
            if self.activate_tool == "pencil":
                painter.setPen(self.pen_color)
                painter.drawPoint(x, y)
            elif self.activate_tool == "eraser":
                painter.setPen(QColor(Qt.white))
                painter.drawPoint(x, y)
            painter.end()
            self.update()

    def resizeEvent(self, event):
        """Handle resizing of the drawing area"""
        new_canvas = QPixmap(self.width(), self.height())
        new_canvas.fill(Qt.white)
        painter = QPainter(new_canvas)
        painter.drawPixmap(0, 0, self.canvas)  # Copy the old canvas content
        painter.end()
        self.canvas = new_canvas
        super(DrawingCanvas, self).resizeEvent(event)

    def paintEvent(self, event):
        """Override paintEvent to draw the canvas"""
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.canvas)
        painter.end()
