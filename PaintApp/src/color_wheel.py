# PaintApp/src/color_wheel.py

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QConicalGradient, QRadialGradient, QBrush
from PyQt5.QtCore import Qt, QPointF, QRectF
import math

class ColorWheel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_color = QColor(255, 255, 255)  # Couleur par défaut

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        #Dimensions and center of the wheel
        rect = QRectF(0, 0, self.width(), self.height())
        center = QPointF(self.width() / 2, self.height() / 2)
        radius = min(self.width(), self.height()) / 2

        conical_gradient = QConicalGradient(center, 0)
        for i in range(0, 360, 10) :
            color = QColor()
            color.setHsv(i, 255, 255)
            conical_gradient.setColorAt(i / 360, color)

        painter.setBrush(QBrush(conical_gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(rect)

        radial_gradient = QRadialGradient(center, radius)
        radial_gradient.setColorAt(0, QColor(255, 255, 255))
        radial_gradient.setColorAt(1, QColor(255, 255, 255, 0))

        painter.setBrush(QBrush(radial_gradient))
        painter.drawEllipse(rect)    



    def mousePressEvent(self, event):
        """Détecter la couleur sélectionnée en cliquant sur la roue."""
        x, y = event.x() - self.width() / 2, event.y() - self.height() / 2
        angle = math.degrees(math.atan2(-y, x)) % 360
        distance = math.sqrt(x**2 + y**2) / (min(self.width(), self.height()) / 2)
        distance = min(max(distance, 0), 1) 

        self.selected_color.setHsv(int(angle), int(255 * distance), 255)
        print(f"Couleur sélectionnée : {self.selected_color.name()}")
