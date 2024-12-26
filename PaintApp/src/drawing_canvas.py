from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtCore import Qt

class DrawingCanvas(QFrame):
    def __init__(self, parent=None):
        super(DrawingCanvas, self).__init__(parent)
        self.grid_size = 25
        self.scale_factor = 25
        self.min_scale_factor = 5
        self.max_scale_factor = 100
        self.canvas = QPixmap(self.grid_size, self.grid_size)
        self.canvas.fill(Qt.blue)
        self.drawing = False
        self.activate_tool = None
        self.pen_color = QColor(Qt.black)
        self.parent().setStyleSheet("border: none;")

    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        if angle > 0: # Zoom in
            self.scale_factor = min(self.scale_factor + 5, self.max_scale_factor)
        elif angle < 0: # Zoom out
            self.scale_factor = max(self.scale_factor - 5, self.min_scale_factor)
        self.update()


    def resizeEvent(self, event):
        content_width = self.parent().width()
        content_height = self.parent().height()

        self.scale_factor = min(content_width // self.grid_size, content_height // self.grid_size)

        self.canvas = QPixmap(self.grid_size, self.grid_size)
        self.canvas.fill(Qt.white)
        self.setGeometry(0, 0, content_width, content_height)
        self.update()
        super(DrawingCanvas, self).resizeEvent(event)

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
        x = (event.pos().x() - self.lineWidth()) // self.scale_factor
        y = (event.pos().y() - self.lineWidth()) // self.scale_factor

        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            painter = QPainter(self.canvas)
            if self.activate_tool == "pencil":
                painter.setPen(self.pen_color)
                painter.drawPoint(x, y)
            elif self.activate_tool == "eraser":
                painter.setPen(QColor(Qt.white))
                painter.drawPoint(x, y)
            painter.end()
            self.update()

    def paintEvent(self, event):
        """Override paintEvent to draw the canvas"""
        painter = QPainter(self)
        # painter.drawPixmap(0, 0, self.canvas)
        for x in range(self.grid_size):
            for y in range (self.grid_size):
                color = self.canvas.toImage().pixelColor(x, y)
                painter.fillRect(x * self.scale_factor, y * self.scale_factor, self.scale_factor, self.scale_factor, color)
        painter.end()

   
