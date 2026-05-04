from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont


class ChartWidget(QWidget):
    COLORS = [
        QColor('#0078d4'),
        QColor('#51cf66'),
        QColor('#ff6b6b'),
        QColor('#ffd43b'),
        QColor('#74c0fc'),
        QColor('#da77f2'),
        QColor('#ff922b'),
        QColor('#20c997')
    ]

    def __init__(self, chart_type='bar', parent=None):
        super().__init__(parent)
        self.chart_type = chart_type
        self.data = []
        self.title = ''
        self.setMinimumHeight(250)
        self.setMinimumWidth(300)

    def set_data(self, data, title=''):
        self.data = data
        self.title = title
        self.update()

    def paintEvent(self, event):
        if not self.data:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.chart_type == 'bar':
            self._drawBarChart(painter)
        elif self.chart_type == 'pie':
            self._drawPieChart(painter)
        elif self.chart_type == 'line':
            self._drawLineChart(painter)

        painter.end()

    def _drawBarChart(self, painter):
        rect = self.rect()
        margin = 50
        chart_rect = QRectF(margin, margin + 20, rect.width() - 2 * margin, rect.height() - 2 * margin - 20)

        if self.title:
            painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
            painter.setPen(QColor('#d4d4d4'))
            painter.drawText(QRectF(0, 5, rect.width(), 30), Qt.AlignmentFlag.AlignCenter, self.title)

        if not self.data:
            return

        max_value = max(d.get('value', 0) for d in self.data) or 1
        bar_width = chart_rect.width() / len(self.data) * 0.7
        spacing = chart_rect.width() / len(self.data) * 0.3

        painter.setPen(QColor('#666'))
        painter.drawLine(int(chart_rect.left()), int(chart_rect.bottom()),
                        int(chart_rect.right()), int(chart_rect.bottom()))

        for i, item in enumerate(self.data):
            value = item.get('value', 0)
            label = item.get('label', '')
            color = self.COLORS[i % len(self.COLORS)]

            bar_height = (value / max_value) * chart_rect.height() * 0.9
            x = chart_rect.left() + i * (bar_width + spacing) + spacing / 2
            y = chart_rect.bottom() - bar_height

            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(x, y, bar_width, bar_height), 3, 3)

            painter.setPen(QColor('#d4d4d4'))
            painter.setFont(QFont('Arial', 8))
            painter.drawText(QRectF(x, chart_rect.bottom() + 5, bar_width, 20),
                           Qt.AlignmentFlag.AlignCenter, label[:8])

            painter.drawText(QRectF(x, y - 20, bar_width, 20),
                           Qt.AlignmentFlag.AlignCenter, str(value))

    def _drawPieChart(self, painter):
        rect = self.rect()
        margin = 60
        size = min(rect.width(), rect.height()) - 2 * margin
        center_x = rect.width() / 2
        center_y = rect.height() / 2 + 10
        radius = size / 2

        if self.title:
            painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
            painter.setPen(QColor('#d4d4d4'))
            painter.drawText(QRectF(0, 5, rect.width(), 30), Qt.AlignmentFlag.AlignCenter, self.title)

        if not self.data:
            return

        total = sum(d.get('value', 0) for d in self.data) or 1
        start_angle = 0

        for i, item in enumerate(self.data):
            value = item.get('value', 0)
            label = item.get('label', '')
            color = self.COLORS[i % len(self.COLORS)]

            span_angle = int((value / total) * 360 * 16)

            painter.setBrush(QBrush(color))
            painter.setPen(QPen(QColor('#1e1e1e'), 2))
            painter.drawPie(int(center_x - radius), int(center_y - radius),
                          int(size), int(size), int(start_angle), span_angle)

            angle = (start_angle + span_angle / 2) / 16 * 3.14159 / 180
            label_x = center_x + (radius + 30) * __import__('math').cos(angle)
            label_y = center_y - (radius + 30) * __import__('math').sin(angle)

            painter.setPen(QColor('#d4d4d4'))
            painter.setFont(QFont('Arial', 9))
            percent = int(value / total * 100)
            painter.drawText(QRectF(label_x - 40, label_y - 10, 80, 20),
                           Qt.AlignmentFlag.AlignCenter, f'{label}\n{percent}%')

            start_angle += span_angle

    def _drawLineChart(self, painter):
        rect = self.rect()
        margin = 50
        chart_rect = QRectF(margin, margin + 20, rect.width() - 2 * margin, rect.height() - 2 * margin - 20)

        if self.title:
            painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
            painter.setPen(QColor('#d4d4d4'))
            painter.drawText(QRectF(0, 5, rect.width(), 30), Qt.AlignmentFlag.AlignCenter, self.title)

        if not self.data or len(self.data) < 2:
            return

        max_value = max(d.get('value', 0) for d in self.data) or 1

        painter.setPen(QColor('#666'))
        painter.drawLine(int(chart_rect.left()), int(chart_rect.bottom()),
                        int(chart_rect.right()), int(chart_rect.bottom()))
        painter.drawLine(int(chart_rect.left()), int(chart_rect.top()),
                        int(chart_rect.left()), int(chart_rect.bottom()))

        points = []
        for i, item in enumerate(self.data):
            value = item.get('value', 0)
            x = chart_rect.left() + (i / (len(self.data) - 1)) * chart_rect.width()
            y = chart_rect.bottom() - (value / max_value) * chart_rect.height() * 0.9
            points.append((x, y, item.get('label', ''), value))

        pen = QPen(self.COLORS[0], 2)
        painter.setPen(pen)

        for i in range(len(points) - 1):
            painter.drawLine(int(points[i][0]), int(points[i][1]),
                           int(points[i+1][0]), int(points[i+1][1]))

        painter.setBrush(QBrush(self.COLORS[0]))
        painter.setPen(Qt.PenStyle.NoPen)
        for point in points:
            painter.drawEllipse(int(point[0]) - 4, int(point[1]) - 4, 8, 8)

        painter.setPen(QColor('#d4d4d4'))
        painter.setFont(QFont('Arial', 8))
        for point in points:
            painter.drawText(QRectF(point[0] - 30, chart_rect.bottom() + 5, 60, 20),
                           Qt.AlignmentFlag.AlignCenter, point[2][:6])
            painter.drawText(QRectF(point[0] - 20, point[1] - 20, 40, 15),
                           Qt.AlignmentFlag.AlignCenter, str(point[3]))
