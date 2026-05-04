from PyQt6.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter, QLinearGradient


class SplashScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap(500, 300)
        pixmap.fill(QColor('#1e1e1e'))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        gradient = QLinearGradient(0, 0, 500, 300)
        gradient.setColorAt(0.0, QColor('#1e1e1e'))
        gradient.setColorAt(0.5, QColor('#2d2d2d'))
        gradient.setColorAt(1.0, QColor('#1e1e1e'))
        painter.fillRect(0, 0, 500, 300, gradient)

        painter.setPen(QColor('#0078d4'))
        font = QFont('Arial', 36, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(0, 80, 500, 60, Qt.AlignmentFlag.AlignCenter, 'Openclaw')

        painter.setPen(QColor('#d4d4d4'))
        font = QFont('Arial', 18, QFont.Weight.Normal)
        painter.setFont(font)
        painter.drawText(0, 140, 500, 40, Qt.AlignmentFlag.AlignCenter, 'Manager')

        painter.setPen(QColor('#666666'))
        font = QFont('Arial', 10)
        painter.setFont(font)
        painter.drawText(0, 220, 500, 30, Qt.AlignmentFlag.AlignCenter, 'Loading...')

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor('#0078d4'))
        painter.drawRoundedRect(150, 260, 200, 4, 2, 2)

        painter.end()

        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)

    def show_and_close(self, duration=1500):
        self.show()
        QTimer.singleShot(duration, self.close)
