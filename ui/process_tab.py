from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QPushButton, QTextEdit, QFormLayout,
    QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

from core.process_manager import ProcessManager


class ProcessTab(QWidget):
    def __init__(self):
        super().__init__()
        self.process_manager = ProcessManager()
        self._initUI()
        self._updateStatus()

    def _initUI(self):
        layout = QVBoxLayout(self)

        control_layout = QHBoxLayout()

        self.start_btn = QPushButton('启动')
        self.start_btn.clicked.connect(self._onStart)
        control_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton('停止')
        self.stop_btn.clicked.connect(self._onStop)
        control_layout.addWidget(self.stop_btn)

        self.restart_btn = QPushButton('重启')
        self.restart_btn.clicked.connect(self._onRestart)
        control_layout.addWidget(self.restart_btn)

        self.refresh_btn = QPushButton('刷新')
        self.refresh_btn.clicked.connect(self._updateStatus)
        control_layout.addWidget(self.refresh_btn)

        control_layout.addStretch()

        self.auto_refresh_cb = QCheckBox('自动刷新')
        self.auto_refresh_cb.stateChanged.connect(self._onAutoRefreshChanged)
        control_layout.addWidget(self.auto_refresh_cb)

        layout.addLayout(control_layout)

        status_group = QGroupBox('状态概览')
        status_layout = QFormLayout(status_group)

        self.status_label = QLabel('未知')
        self.status_label.setStyleSheet('font-weight: bold;')
        status_layout.addRow('状态:', self.status_label)

        self.pid_label = QLabel('-')
        status_layout.addRow('PID:', self.pid_label)

        self.uptime_label = QLabel('-')
        status_layout.addRow('运行时间:', self.uptime_label)

        layout.addWidget(status_group)

        config_group = QGroupBox('配置信息')
        config_layout = QFormLayout(config_group)

        self.port_label = QLabel('-')
        config_layout.addRow('端口:', self.port_label)

        self.bind_label = QLabel('-')
        config_layout.addRow('绑定:', self.bind_label)

        self.auth_label = QLabel('-')
        config_layout.addRow('认证:', self.auth_label)

        self.mode_label = QLabel('-')
        config_layout.addRow('模式:', self.mode_label)

        layout.addWidget(config_group)

        log_group = QGroupBox('进程日志')
        log_layout = QVBoxLayout(log_group)

        log_toolbar = QHBoxLayout()

        self.refresh_log_btn = QPushButton('刷新日志')
        self.refresh_log_btn.clicked.connect(self._refreshLogs)
        log_toolbar.addWidget(self.refresh_log_btn)

        self.clear_log_btn = QPushButton('清除')
        self.clear_log_btn.clicked.connect(lambda: self.log_text.clear())
        log_toolbar.addWidget(self.clear_log_btn)

        log_toolbar.addStretch()

        log_layout.addLayout(log_toolbar)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont('Consolas', 9))
        self.log_text.setMaximumHeight(300)
        log_layout.addWidget(self.log_text)

        layout.addWidget(log_group)

        self.status_bar = QLabel('就绪')
        layout.addWidget(self.status_bar)

        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._updateStatus)

    def _updateStatus(self):
        status = self.process_manager.get_status()
        running = status.get('running', False)

        if running:
            self.status_label.setText('运行中')
            self.status_label.setStyleSheet('color: #51cf66; font-weight: bold;')
            self.pid_label.setText(str(status.get('pid', '-')))
            self.uptime_label.setText(status.get('uptime', '-'))
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.restart_btn.setEnabled(True)
        else:
            self.status_label.setText('已停止')
            self.status_label.setStyleSheet('color: #ff6b6b; font-weight: bold;')
            self.pid_label.setText('-')
            self.uptime_label.setText('-')
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.restart_btn.setEnabled(False)

        config = self.process_manager.get_config()
        self.port_label.setText(str(config.get('port', '-')))
        self.bind_label.setText(config.get('bind', '-'))
        self.auth_label.setText(config.get('auth_mode', '-'))
        self.mode_label.setText(config.get('mode', '-'))

        self.status_bar.setText(f'状态已更新: {status.get("running", False)}')

    def _refreshLogs(self):
        logs = self.process_manager.get_logs(200)
        self.log_text.clear()
        for line in logs:
            self.log_text.append(line.strip())
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    def _onStart(self):
        result = self.process_manager.start()
        if result['success']:
            QMessageBox.information(self, '成功', result['message'])
            self._updateStatus()
        else:
            QMessageBox.critical(self, '错误', result['message'])

    def _onStop(self):
        reply = QMessageBox.question(
            self, '确认停止',
            '确定要停止Openclaw进程吗？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            result = self.process_manager.stop()
            if result['success']:
                QMessageBox.information(self, '成功', result['message'])
                self._updateStatus()
            else:
                QMessageBox.critical(self, '错误', result['message'])

    def _onRestart(self):
        reply = QMessageBox.question(
            self, '确认重启',
            '确定要重启Openclaw进程吗？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            result = self.process_manager.restart()
            if result['success']:
                QMessageBox.information(self, '成功', result['message'])
                self._updateStatus()
            else:
                QMessageBox.critical(self, '错误', result['message'])

    def _onAutoRefreshChanged(self, state):
        if state == 2:
            self.refresh_timer.start(5000)
        else:
            self.refresh_timer.stop()

    def refresh(self):
        self._updateStatus()
        self._refreshLogs()
