# PaintApp/src/color_wheel.py

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPointF, QRectF
import math

class ColorWheel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)  # Taille fixe pour la roue des couleurs
        self.selected_color = QColor(255, 255, 255)  # Couleur par défaut

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dessiner la roue des couleurs
        rect = QRectF(0, 0, self.width(), self.height())
        for i in range(360):  # Diviser en 360 sections pour chaque degré
            color = QColor()
            color.setHsv(i, 255, 255)  # HSV pour générer les couleurs
            painter.setPen(QPen(color, 2))
            painter.drawArc(rect, i * 16, 16)  # Chaque arc couvre 1 degré

    def mousePressEvent(self, event):
        """Détecter la couleur sélectionnée en cliquant sur la roue."""
        x, y = event.x() - self.width() / 2, event.y() - self.height() / 2
        angle = math.degrees(math.atan2(-y, x)) % 360
        self.selected_color.setHsv(int(angle), 255, 255)
        print(f"Couleur sélectionnée : {self.selected_color.name()}")
