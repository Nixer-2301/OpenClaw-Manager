from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QComboBox, QLineEdit,
    QLabel, QCheckBox, QHeaderView, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont

from core.log_manager import LogManager
from utils.translator import tr


class LogTab(QWidget):
    def __init__(self):
        super().__init__()
        self.log_manager = LogManager()
        self.current_file = None
        self._initUI()
        self._loadLogFiles()

    def _initUI(self):
        layout = QVBoxLayout(self)

        toolbar_layout = QHBoxLayout()

        self.file_combo = QComboBox()
        self.file_combo.currentTextChanged.connect(self._onFileChanged)
        toolbar_layout.addWidget(QLabel(tr('log.file') + ':'))
        toolbar_layout.addWidget(self.file_combo)

        self.level_combo = QComboBox()
        self.level_combo.addItems(['ALL', 'INFO', 'WARN', 'ERROR', 'DEBUG'])
        self.level_combo.currentTextChanged.connect(self._onFilterChanged)
        toolbar_layout.addWidget(QLabel(tr('log.level') + ':'))
        toolbar_layout.addWidget(self.level_combo)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(tr('log.search') + '...')
        self.search_input.textChanged.connect(self._onFilterChanged)
        toolbar_layout.addWidget(self.search_input)

        self.refresh_btn = QPushButton(tr('action.refresh'))
        self.refresh_btn.clicked.connect(self._loadLogContent)
        toolbar_layout.addWidget(self.refresh_btn)

        self.auto_refresh_cb = QCheckBox(tr('log.autoRefresh'))
        self.auto_refresh_cb.stateChanged.connect(self._onAutoRefreshChanged)
        toolbar_layout.addWidget(self.auto_refresh_cb)

        layout.addLayout(toolbar_layout)

        stats_group = QGroupBox('Log Statistics')
        stats_layout = QHBoxLayout(stats_group)

        self.total_label = QLabel('Total: 0')
        self.info_label = QLabel('INFO: 0')
        self.warn_label = QLabel('WARN: 0')
        self.error_label = QLabel('ERROR: 0')

        self.info_label.setStyleSheet('color: #51cf66;')
        self.warn_label.setStyleSheet('color: #ffd43b;')
        self.error_label.setStyleSheet('color: #ff6b6b;')

        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.info_label)
        stats_layout.addWidget(self.warn_label)
        stats_layout.addWidget(self.error_label)
        stats_layout.addStretch()

        layout.addWidget(stats_group)

        self.log_table = QTableWidget()
        self.log_table.setColumnCount(3)
        self.log_table.setHorizontalHeaderLabels([
            tr('log.timestamp'), tr('log.level'), tr('log.message')
        ])
        self.log_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.log_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.log_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.log_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.log_table.setAlternatingRowColors(True)
        self.log_table.setFont(QFont('Consolas', 9))

        layout.addWidget(self.log_table)

        self.status_label = QLabel(tr('status.ready'))
        layout.addWidget(self.status_label)

        self.auto_refresh_timer = QTimer()
        self.auto_refresh_timer.timeout.connect(self._loadLogContent)

    def _loadLogFiles(self):
        self.file_combo.clear()
        log_files = self.log_manager.get_log_files()
        for log_file in log_files:
            self.file_combo.addItem(log_file['name'], log_file['path'])
        self.status_label.setText(f'{tr("status.loaded")}: {len(log_files)} log files')

    def _onFileChanged(self, file_name):
        if file_name:
            self.current_file = self.file_combo.currentData()
            self._loadLogContent()

    def _onFilterChanged(self):
        if self.current_file:
            self._loadLogContent()

    def _loadLogContent(self):
        if not self.current_file:
            return

        level_filter = self.level_combo.currentText()
        keyword = self.search_input.text().strip()

        lines = self.log_manager.read_log(self.current_file, level_filter, keyword)

        self.log_table.setRowCount(len(lines))
        for row, line in enumerate(lines):
            timestamp_item = QTableWidgetItem(line.get('timestamp', ''))
            self.log_table.setItem(row, 0, timestamp_item)

            level = line.get('level', '')
            level_item = QTableWidgetItem(level)
            if level == 'ERROR':
                level_item.setForeground(QColor('#ff6b6b'))
            elif level == 'WARN':
                level_item.setForeground(QColor('#ffd43b'))
            elif level == 'INFO':
                level_item.setForeground(QColor('#51cf66'))
            elif level == 'DEBUG':
                level_item.setForeground(QColor('#74c0fc'))
            self.log_table.setItem(row, 1, level_item)

            message_item = QTableWidgetItem(line.get('message', ''))
            self.log_table.setItem(row, 2, message_item)

        self.log_table.scrollToBottom()

        stats = self.log_manager.get_log_stats(self.current_file)
        self.total_label.setText(f'Total: {stats.get("TOTAL", 0)}')
        self.info_label.setText(f'INFO: {stats.get("INFO", 0)}')
        self.warn_label.setText(f'WARN: {stats.get("WARN", 0)}')
        self.error_label.setText(f'ERROR: {stats.get("ERROR", 0)}')

        self.status_label.setText(f'{tr("status.loaded")}: {len(lines)} lines')

    def _onAutoRefreshChanged(self, state):
        if state == 2:
            self.auto_refresh_timer.start(5000)
        else:
            self.auto_refresh_timer.stop()

    def refresh(self):
        self._loadLogFiles()
        if self.current_file:
            self._loadLogContent()
