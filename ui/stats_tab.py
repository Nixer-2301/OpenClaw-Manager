from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QComboBox, QPushButton, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from core.stats_manager import StatsManager
from ui.widgets.chart_widget import ChartWidget
from utils.translator import tr


class StatsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.stats_manager = StatsManager()
        self._initUI()
        self._loadStats()

    def _initUI(self):
        layout = QVBoxLayout(self)

        overview_group = QGroupBox(tr('stats.overview'))
        overview_layout = QHBoxLayout(overview_group)

        self.sessions_card = self._createStatCard(tr('stats.sessions'), '0')
        self.skills_card = self._createStatCard(tr('stats.skills'), '0')
        self.models_card = self._createStatCard(tr('stats.models'), '0')

        overview_layout.addWidget(self.sessions_card)
        overview_layout.addWidget(self.skills_card)
        overview_layout.addWidget(self.models_card)
        overview_layout.addStretch()

        layout.addWidget(overview_group)

        toolbar_layout = QHBoxLayout()

        self.date_range_combo = QComboBox()
        self.date_range_combo.addItems([
            tr('stats.last7days'),
            tr('stats.last30days'),
            tr('stats.last90days'),
            tr('stats.all')
        ])
        self.date_range_combo.currentIndexChanged.connect(self._loadChart)
        toolbar_layout.addWidget(QLabel(tr('stats.dateRange') + ':'))
        toolbar_layout.addWidget(self.date_range_combo)

        toolbar_layout.addStretch()

        self.refresh_btn = QPushButton(tr('action.refresh'))
        self.refresh_btn.clicked.connect(self._loadStats)
        toolbar_layout.addWidget(self.refresh_btn)

        self.export_btn = QPushButton(tr('action.export'))
        self.export_btn.clicked.connect(self._onExport)
        toolbar_layout.addWidget(self.export_btn)

        layout.addLayout(toolbar_layout)

        chart_group = QGroupBox('每日会话趋势')
        chart_layout = QVBoxLayout(chart_group)

        self.daily_chart = ChartWidget('line')
        self.daily_chart.setMinimumHeight(300)
        chart_layout.addWidget(self.daily_chart)

        layout.addWidget(chart_group)

        data_group = QGroupBox('每日数据')
        data_layout = QVBoxLayout(data_group)

        self.daily_table = QTableWidget()
        self.daily_table.setColumnCount(2)
        self.daily_table.setHorizontalHeaderLabels(['Date', 'Sessions'])
        self.daily_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.daily_table.setAlternatingRowColors(True)
        data_layout.addWidget(self.daily_table)

        layout.addWidget(data_group)

        self.status_label = QLabel(tr('status.ready'))
        layout.addWidget(self.status_label)

    def _createStatCard(self, title, value):
        card = QGroupBox()
        layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setStyleSheet('color: gray; font-size: 12px;')
        layout.addWidget(title_label)

        value_label = QLabel(value)
        value_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        value_label.setStyleSheet('color: #0078d4;')
        layout.addWidget(value_label)

        card.setFixedWidth(200)
        card._value_label = value_label

        return card

    def _loadStats(self):
        overview = self.stats_manager.get_overview()

        self.sessions_card._value_label.setText(str(overview.get('sessions', 0)))
        self.skills_card._value_label.setText(str(overview.get('user_skills', 0) + overview.get('system_skills', 0)))
        self.models_card._value_label.setText(str(overview.get('models', 0)))

        self._loadChart()
        self._loadTable()

        self.status_label.setText(tr('status.loaded'))

    def _loadChart(self):
        range_index = self.date_range_combo.currentIndex()
        days_map = {0: 7, 1: 30, 2: 90, 3: 365}
        days = days_map.get(range_index, 7)

        daily_stats = self.stats_manager.get_daily_session_stats(days)
        daily_data = [{'label': date, 'value': count} for date, count in daily_stats.items()]
        self.daily_chart.set_data(daily_data, '每日会话趋势')

    def _loadTable(self):
        range_index = self.date_range_combo.currentIndex()
        days_map = {0: 7, 1: 30, 2: 90, 3: 365}
        days = days_map.get(range_index, 7)

        daily_stats = self.stats_manager.get_daily_session_stats(days)
        self.daily_table.setRowCount(len(daily_stats))
        for row, (date, count) in enumerate(daily_stats.items()):
            self.daily_table.setItem(row, 0, QTableWidgetItem(date))
            count_item = QTableWidgetItem(str(count))
            count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.daily_table.setItem(row, 1, count_item)

    def _onExport(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, tr('action.export'),
            'openclaw_stats.json',
            'JSON files (*.json)'
        )

        if file_path:
            success = self.stats_manager.export_stats(file_path)
            if success:
                QMessageBox.information(self, tr('dialog.success'), f'Stats exported to: {file_path}')
            else:
                QMessageBox.critical(self, tr('dialog.error'), 'Failed to export stats')

    def refresh(self):
        self._loadStats()
